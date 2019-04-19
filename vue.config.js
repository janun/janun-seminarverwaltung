const path = require("path");

// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
  assetsDir: "static",

  devServer: {
    proxy: {
      "/api*": {
        target: "http://localhost:8000/"
      }
    }
  }
};
