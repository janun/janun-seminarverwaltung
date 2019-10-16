const gulp = require("gulp");

function styles() {
  const postcss = require("gulp-postcss");
  return gulp
    .src("backend/static_src/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/styles"));
}

function watch() {
  gulp.watch(
    [
      "backend/templates/**/*.html",
      "backend/static_src/styles/*.css",
      "backend/**/*.py"
    ],
    styles
  );
}

module.exports = {
  styles,
  watch,
  default: styles
};
