const express = require("express");

const app = express();
const port = process.env.PORT || 3000;

app.get("/", (_req, res) => {
  res.json({ message: "supply chain security lab" });
});

app.get("/healthz", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(port, () => {
  console.log(`server listening on ${port}`);
});

