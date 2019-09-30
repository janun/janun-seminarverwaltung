const gulp = require("gulp");

function styles() {
  const postcss = require("gulp-postcss");
  return gulp
    .src("backend/static/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/css"));
}

function watch() {
  gulp.watch(
    [
      "backend/templates/**/*.html",
      "backend/static/styles/*.css",
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
