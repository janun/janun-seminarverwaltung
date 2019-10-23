const gulp = require("gulp");
const postcss = require("gulp-postcss");
const concat = require("gulp-concat");
const uglify = require('gulp-uglify');


function styles() {
  return gulp
    .src("backend/static_src/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/styles"));
}

function scripts() {
  return gulp
    .src("backend/static_src/scripts/*.js")
    .pipe(concat("scripts.js"))
    .pipe(uglify())
    .pipe(gulp.dest("backend/static/scripts"));
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
  gulp.watch(
    [
      "backend/static_src/scripts/*.js",
    ],
    styles
  );
}

module.exports = {
  styles,
  scripts,
  watch,
  default: gulp.parallel(styles, scripts)
};
