import React from "react"
import ReactDOM from "react-dom/client"

#import "@fontsource/inter"

import "./index.css"

 import "./styles/globals.css"
 import "./styles/dashboard.css"
 import "./styles/graph.css"
 import "./styles/animations.css"

import App from "./App"

ReactDOM.createRoot(
  document.getElementById("root")!
).render(

  <React.StrictMode>
    <App />
  </React.StrictMode>
)
