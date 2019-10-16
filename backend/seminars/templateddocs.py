# fork of https://github.com/alexmorozov/templated-docs
# changed to support django 2 and work without libreoffice on the server
import os
import os.path
import mimetypes
import re
from tempfile import NamedTemporaryFile
import zipfile

from django.template import Template
from django.template.exceptions import TemplateDoesNotExist
from django.template import Context, engines
from django.utils.encoding import smart_bytes, smart_str
from django.http import HttpResponse


IMAGES_CONTEXT_KEY = "_templated_docs_imgs"


class FileResponse(HttpResponse):
    """
    One-time HTTP response with a generated file. DELETES A FILE AFTERWARDS!
    """

    def __init__(self, actual_file, visible_name, *args, delete=True, **kwargs):
        super(FileResponse, self).__init__(*args, **kwargs)
        self["Content-type"] = mimetypes.guess_type(actual_file)[0]
        self["Content-disposition"] = "attachment; filename=%s" % visible_name
        with open(actual_file, "rb") as f:
            self.content = f.read()
        self["Content-length"] = len(self.content)
        if delete:
            os.unlink(actual_file)


def _get_template_loaders():
    """
    Get all available template loaders for the Django engine.
    """
    loaders = []

    for loader_name in engines["django"].engine.loaders:
        loader = engines["django"].engine.find_template_loader(loader_name)
        if loader is not None and hasattr(loader, "get_template_sources"):
            loaders.append(loader)
    return tuple(loaders)


def fix_inline_tags(content):
    """
    Replace broken entities within Django template constructs.

    MS Word likes to replace some entities just in case, and we end up with
    broken Django constructs. To remedy that, we find all the Django tags and
    variables and fix entities inside them.
    """

    def repl(match):
        text = match.group(0)
        text = text.replace("<text:s/>", " ")
        text = text.replace("&apos;", "'")
        text = text.replace("&quot;", '"')
        return re.sub(r"<[^>]+>", "", text)

    django_tag_re = r"(\{[\{\%].+?[\%\}]\})"
    return re.sub(django_tag_re, repl, content)


def find_template_file(template_name):
    """
    Return a full path to the specified template file.

    The key difference from the stock `find_template` is that we don't try to
    load a template in memory, because we'll deal with it ourselves.
    """
    for loader in _get_template_loaders():
        for origin in loader.get_template_sources(template_name):
            path = getattr(origin, "name", origin)  # Django <1.9 compatibility
            if os.path.exists(path):
                return path
    raise TemplateDoesNotExist(template_name)


def fill_template(template_name, context, output_format="odt"):
    """
    Fill a document with data

    Returns an absolute path to the generated file.
    """

    if not isinstance(context, Context):
        context = Context(context)

    context["output_format"] = output_format

    source_file = find_template_file(template_name)
    source_extension = os.path.splitext(source_file)[1]
    source = zipfile.ZipFile(source_file, "r")

    dest_file = NamedTemporaryFile(delete=False, suffix=source_extension)
    dest = zipfile.ZipFile(dest_file, "w")

    manifest_data = ""
    for name in source.namelist():
        data = source.read(name)
        if name.endswith(".xml"):
            data = smart_str(data)

        if any(name.endswith(file) for file in ("content.xml", "styles.xml")):
            template = Template(fix_inline_tags(data))
            data = template.render(context)
        elif name == "META-INF/manifest.xml":
            manifest_data = data[:-20]  # Cut off the closing </manifest> tag
            continue  # We will append it at the very end
        dest.writestr(name, smart_bytes(data))

    for _, image in context.dicts[0].get(IMAGES_CONTEXT_KEY, {}).items():
        filename = os.path.basename(image.name)
        extension = os.path.splitext(filename)[1][1:]
        manifest_data += (
            f"<manifest:file-entry"
            f'manifest:media-type="image/{extension}"'
            f'manifest:full-path="Pictures/{filename}"/>\n'
        )
        image.open()
        dest.writestr(f"Pictures/{filename}", image.read())
        image.close()

    manifest_data += "</manifest:manifest>"
    dest.writestr("META-INF/manifest.xml", manifest_data)

    source.close()
    dest.close()

    return dest_file.name
