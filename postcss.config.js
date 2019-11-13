const purgecss = require("@fullhuman/postcss-purgecss")({
  content: ["./backend/templates/**/*.html", "./backend/**/*.py", "./backend/**/*.js"],
  defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
  whitelist: ["button", "input", "optgroup", "select", "textarea", "asc", "desc", "linkwidget", "table-container"]
});

module.exports = {
  plugins: [
    require("postcss-import"),
    require("tailwindcss"),
    purgecss,
    require("autoprefixer"),
    require("cssnano")
  ]
};
