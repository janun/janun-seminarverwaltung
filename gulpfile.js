const gulp = require("gulp");
const postcss = require("gulp-postcss");
const terser = require('gulp-terser');
const sourcemaps = require("gulp-sourcemaps");
const concat = require("gulp-concat");

const production = (process.env.NODE_ENV || "").trim() === 'production'

function styles() {
  return gulp
    .src("backend/static_src/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/styles"));
}

function scripts() {
  return gulp.src([
    "backend/static_src/scripts/polyfills/*.js",
    "backend/static_src/scripts/*.js"
  ])
    .pipe(concat("scripts.js"))
    .pipe(sourcemaps.init({ loadMaps: !production }))
    .pipe(terser())
    .pipe(sourcemaps.write("./"))
    .pipe(gulp.dest("backend/static/scripts"));
}

function watch() {
  gulp.watch(
    [
      "backend/templates/**/*.html",
      "backend/static_src/styles/*.css",
      "backend/**/*.py",
      "tailwind.config.js",
      "postcss.config.js"
    ],
    styles
  );
  gulp.watch(
    [
      "backend/static_src/scripts/**/*.js",
    ],
    scripts
  );
}

module.exports = {
  styles,
  scripts,
  watch,
  default: gulp.parallel(styles, scripts)
};
