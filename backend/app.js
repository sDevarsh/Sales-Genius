const bodyParser = require("body-parser");
const cors = require("cors");
const express = require("express");
const multer = require("multer");
const sqlite3 = require("sqlite3");
const { spawn } = require("child_process");
const app = express();
const port = 3000;
app.use(cors());
const pythonScriptPath = "final_project.py";
const db = new sqlite3.Database("database.db");
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
app.use(express.static("public"));

app.use(bodyParser.json());

app.post("/upload", upload.single("csvFile"), (req, res) => {
  const csvFile = req.file;

  if (!csvFile) {
    return res.status(400).send("No CSV file uploaded.");
  }
  db.run("Delete from files2", (err) => {
    db.run(
      "INSERT INTO files2 (csvFile) VALUES (?)",
      [csvFile.buffer],
      (err) => {
        if (err) {
          console.error("Error inserting CSV file:", err);
          return res
            .status(500)
            .send("Error inserting CSV file into the database.");
        } else {
          const stringArray = ["devarsh", "ram"];
          const pythonProcess = spawn("python", [
            "final_project.py",
            stringArray,
          ]);
          pythonProcess.stdout.on("data", (data) => {
            console.log(`Python stdout: ${data}`);
          });
          pythonProcess.on("close", (code) => {
            const query = `SELECT * FROM images`;

            db.all(query, [], (err, rows) => {
              if (err) {
                return res.status(500).json({ error: err.message });
              }
              if (rows.length === 0) {
                return res.status(404).json({ error: "No images found" });
              }
              // const imageBuffer = Buffer.from(rows[0].image_data); // Assuming image data is stored as base64
              // res.contentType("image/png");
              res.send(rows);
            });
          });
        }
        // res.send("CSV file has been uploaded and saved.");
      }
    );
  });
});

// API endpoint to receive an array of strings
app.get("/receive-strings", (req, res) => {});
// app.post("/get-images", (req, res) => {
//   const stringArray = req.body;
//   db.run("Select * From images", [stringArray], (err) => {
//     if (err) {
//       console.error("Error inserting CSV file:", err);
//       return res
//         .status(500)
//         .send("Error inserting CSV file into the database.");
//     }

//     res.send(stringArray);
//   });
//   res.status(200).send(stringArray);
// });

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
