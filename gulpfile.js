const gulp = require("gulp");

gulp.task("styles", function() {
  const postcss = require("gulp-postcss");
  return gulp
    .src("backend/static/styles/base.css")
    .pipe(postcss())
    .pipe(gulp.dest("backend/static/css"));
});

gulp.task("watch", function() {
  gulp.watch(
    [
      "backend/templates/**/*.html",
      "backend/static/styles/*.css",
      "backend/**/*.py"
    ],
    gulp.parallel("styles")
  );
});

gulp.task("default", gulp.parallel("styles"));
