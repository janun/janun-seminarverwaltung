const gulp = require("gulp");

exports.styles = function () {
  // BUG: if other files than base.css changed,
  //      compiles but does not actually change output
  const postcss = require("gulp-postcss");
  return gulp
    .src("backend/static/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/css"));
};

exports.watch = function () {
  gulp.watch(
    [
      "backend/templates/**/*.html",
      "backend/static/styles/*.css",
      "backend/**/*.py"
    ],
    gulp.parallel("styles")
  );
};

exports.default = exports.styles;