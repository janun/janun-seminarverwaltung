const gulp = require("gulp");
const postcss = require("gulp-postcss");
const terser = require('gulp-terser');
const browserify = require("browserify");
const source = require("vinyl-source-stream");
const buffer = require("vinyl-buffer");
const sourcemaps = require("gulp-sourcemaps");
const glob = require('glob');

const production = (process.env.NODE_ENV || "").trim() === 'production'

function styles() {
  return gulp
    .src("backend/static_src/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/styles"));
}

function scripts() {
  const files = glob.sync("backend/static_src/scripts/*.js");
  return browserify(files, { debug: !production })
    .transform("babelify")
    .bundle()
    .pipe(source("scripts.js"))
    .pipe(buffer())
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
      "backend/static_src/scripts/*.js",
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
