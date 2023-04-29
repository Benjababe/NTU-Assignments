import fs from "node:fs";

import { calculateReputationScore } from "../db";

export const IMAGE_FOLDER = "images";
export const HTTP_LOG_FILE = "httplog";

const REP_SCORE_THRESHOLD = 5;

/**
 * 
 * Retrieves the user's trustworthy-ness
 * @param {number} userId 
 * @returns {Promise<boolean>}
 */
export const runEtcReputation = async (userId) => {
    const repScore = await calculateReputationScore(userId);
    return (repScore >= 5);
};

export const createImageFolder = () => {
    if (!fs.existsSync(IMAGE_FOLDER))
        fs.mkdirSync(IMAGE_FOLDER);
};

export const logMiddleware = (req, res, next) => {
    const logStr = `${req.method} ${req.originalUrl}`;
    console.log(logStr);
    fs.appendFile(HTTP_LOG_FILE, logStr + "\n", (err) => {
        if (err) throw err;
    });
    next();
};