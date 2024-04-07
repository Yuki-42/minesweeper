// Requirements
const path = require("path");

// Create electron window
const { app, BrowserWindow } = require("electron");

function homeWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
        preload: path.join(__dirname, "preload.js"),
    },
  });

  win.loadFile("index.html").then(r => console.log("Loaded index.html"));
}

app.whenReady().then(homeWindow);

// Set OS specific conventions
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();  // Quit app when all windows are closed except on macOS
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) homeWindow();  // Create window when app is activated and no windows are open
});