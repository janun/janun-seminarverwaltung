const purgecss = require("@fullhuman/postcss-purgecss")({
  content: ["./public/index.html", "./src/**/*.html", "./src/**/*.vue"],
  extractors: [
    {
      extractor: class {
        static extract(content) {
          return content.match(/[A-Za-z0-9-_:/]+/g) || [];
        }
      },

      // Specify all of the extensions of your template files
      extensions: ["html", "vue", "jsx" /* etc. */]
    }
  ]
});

module.exports = {
  plugins: [
    require("tailwindcss"),
    require("autoprefixer"),
    ...(process.env.NODE_ENV === "production" ? [purgecss] : [])
  ]
};
