const path = require('path');
const stdLibBrowser = require('node-stdlib-browser');
const { NodeProtocolUrlPlugin } = require('node-stdlib-browser/helpers/webpack/plugin');
const webpack = require('webpack');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  resolve: {
    alias: stdLibBrowser
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  },
  plugins: [
    new NodeProtocolUrlPlugin(),
    new webpack.ProvidePlugin({
      process: stdLibBrowser.process,
      Buffer: [stdLibBrowser.buffer, 'Buffer']
    })
  ]
};
