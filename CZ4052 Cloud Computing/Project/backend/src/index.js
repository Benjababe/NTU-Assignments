import express from "express";
import cors from "cors";
import routes from "./routes";
import { initDB } from "./db";
import { createImageFolder, logMiddleware, IMAGE_FOLDER } from "./etc";

initDB();
createImageFolder();

const app = express();
const port = process.env.PORT || 3001;

app.use(express.static("build"));
app.use("/images", express.static(IMAGE_FOLDER));
app.use(express.json({ limit: "20mb" }));
app.use(express.urlencoded({ limit: "20mb", extended: true }));
app.use(cors());
app.use(logMiddleware);
app.use(routes.objectRouter);
app.use(routes.objectVoteRouter);
app.use(routes.userRouter);

app.get("/", (req, res) => {
    res.send("EtcMap Server is Up!");
});

app.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});