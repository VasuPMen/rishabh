import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "@ui5/webcomponents-react/dist/Assets.js";
import "@ui5/webcomponents/dist/Assets.js";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
