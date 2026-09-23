// Run with React, React DOM, and esbuild installed in the provided directory:
// node scripts/build_todo_preview.mjs /path/to/build-directory/node_modules
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
const modules = resolve(process.argv[2] || 'node_modules');
const require = createRequire(resolve(modules, '../package.json'));
const { build } = require('esbuild');
for (const variant of ['', '_tables', '_api']) {
await build({
  stdin: {
    contents: `import React from "react"; import {createRoot} from "react-dom/client"; import App from "./project_examples/${"react" + variant}/src/App.jsx"; createRoot(document.getElementById("root")).render(<App />);`,
    resolveDir: process.cwd(),
    loader: 'jsx',
  },
  nodePaths: [modules],
  bundle: true,
  minify: true,
  jsx: 'automatic',
  define: {'process.env.NODE_ENV': '"production"'},
  outfile: `static/todo-react${variant.replace('_', '-')}/app.js`,
  legalComments: 'eof',
});

}
