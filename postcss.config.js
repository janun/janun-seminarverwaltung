const purgecss = require("@fullhuman/postcss-purgecss")({
  content: ["./backend/templates/**/*.html", "./backend/**/*.py"],
  defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
  whitelist: ["button", "input", "optgroup", "select", "textarea"]
});

module.exports = {
  plugins: [
    require("postcss-import"),
    require("tailwindcss"),
    require("autoprefixer"),
    purgecss,
    require("cssnano")
  ]
};
