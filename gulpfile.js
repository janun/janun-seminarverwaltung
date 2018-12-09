const { series, parallel, src, dest, watch } = require('gulp');
const spawn = require('child_process').spawn;
const browserSync = require('browser-sync').create();
const reload = browserSync.reload;
const packageJson = require('./package.json');
const sass = require('gulp-sass');
const sassGlob = require('gulp-sass-glob');
const autoprefixer = require('gulp-autoprefixer');
const cssnano = require('gulp-cssnano');
const rename = require('gulp-rename');
const plumber = require('gulp-plumber');
const pixrem = require('gulp-pixrem');
const uglify = require('gulp-uglify');
const imagemin = require('gulp-imagemin');
const concat = require("gulp-concat");


var pathsConfig = function (appName) {
  this.app = "./" + (appName || packageJson.name);
  var vendorsRoot = 'node_modules/';
  return {
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    sass: this.app + '/static/sass',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: this.app + '/static/js',
    nodeModules: vendorsRoot
  }
};
var paths = pathsConfig();


const styles = function(cb) {
  return src(paths.sass + '/project.scss')
    .pipe(sassGlob())
    .pipe(sass({includePaths: [paths.sass, paths.nodeModules]}).on('error', sass.logError))
    .pipe(plumber())
    .pipe(autoprefixer())
    .pipe(pixrem())
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano())
    .pipe(dest(paths.css));
};

const scripts = function(cb) {
  return src([paths.js + '/**/*.js', '!**/*.min.js'])
    .pipe(concat("project.min.js"))
    .pipe(plumber())
    .pipe(uglify())
    .pipe(dest(paths.js));
};

const imgCompression = function(cb) {
  return src(paths.images + '/*')
    .pipe(imagemin())
    .pipe(dest(paths.images));
};

const runServer = function(cb) {
  const cmd = spawn('python', ['manage.py', 'runserver'], {stdio: 'inherit'});
  cmd.on('close', code => {
    console.log('runServer exited with code ' + code);
    cb(code);
  });
};

const sync = function(cb) {
  browserSync.init(
    [paths.css + "/*.css", paths.js + "*.js", paths.templates + '*.html'], {
      proxy:  "localhost:8000"
  });
  cb();
};

watch([paths.sass + '/*.scss', paths.sass + '/_*.scss'], styles);
watch([paths.js + '/**/*.js', '!**/*.min.js'], scripts).on("change", reload);
watch(paths.templates + '/**/*.html').on("change", reload);

exports.default = series(
  parallel(styles, scripts, imgCompression),
  parallel(runServer, sync)
)
