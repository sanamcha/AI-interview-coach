# React To-Do preview

Generated from `project_examples/react/src/App.jsx` and its CSS. Rebuild after
changing the tutorial source:

```sh
npm install --prefix /tmp/interview-preview-build react@19.2.0 react-dom@19.2.0 esbuild@0.25.12
node scripts/build_todo_preview.mjs /tmp/interview-preview-build/node_modules
```

The committed bundle lets the Flask app serve a real React preview without Node
or a CDN at runtime. React and React DOM license notices are retained in app.js.
