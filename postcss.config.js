const purgecss = require("@fullhuman/postcss-purgecss")({
  content: ["./backend/templates/**/*.html"],
  defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
  whitelist: ["button", "input", "optgroup", "select", "textarea"]
});

module.exports = {
  plugins: [
    require("tailwindcss"),
    require("autoprefixer"),
    purgecss,
    require("cssnano")
  ]
};
