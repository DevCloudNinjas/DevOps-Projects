import * as matter from 'gray-matter';

export async function fetchMetadata() {
  let bootcampMetadata = null;
  try {
    const response = await fetch(window.location.origin + "/docs/README.md");
    const text = await response.text();
    bootcampMetadata = matter(text).data;

  } catch (error) {
    console.log(error);
  } finally {
    return bootcampMetadata;
  }
}

(function () {
  var stripFrontMatter = function (hook, _vm) {
    // Invoked on each page load before new markdown is transformed to HTML.
    // Supports asynchronous tasks (see beforeEach documentation for details).
    hook.beforeEach(function (markdown) {
      const { data, content } = matter(markdown);

      return content;
    });
  };

  // Add plugin to docsify's plugin array
  $docsify = $docsify || {};
  $docsify.plugins = [].concat(stripFrontMatter, $docsify.plugins || []);
})();
