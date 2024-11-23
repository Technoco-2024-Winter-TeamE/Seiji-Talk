import React from "react";
import ReactDOM from "react-dom/client";
import App from './App';
import "./assets/styles/global.css"; // グローバルCSS（必要に応じて）

// ReactアプリケーションをHTMLのルート要素にマウント
const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);