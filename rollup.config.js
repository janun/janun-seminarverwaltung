import { terser } from 'rollup-plugin-terser';

module.exports = {
  input: 'backend/static_src/scripts/scripts.js',
  output: {
    file: 'backend/static/scripts/scripts.js',
    format: 'iife',
    plugins: [terser()]
  }
}