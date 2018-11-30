// for image file uploads
var elems = document.querySelectorAll('[data-read-image]');
for (var i=0; i<elems.length; i++) {
  elems[i].addEventListener('change', function(event) {
    var input = event.target;
    var img_id = input.getAttribute('data-read-image');
    var img = document.getElementById(img_id);
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        img.setAttribute('src', e.target.result)
      }
      reader.readAsDataURL(input.files[0]);
    }
  });
}
