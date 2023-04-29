import bcrypt from "bcrypt";
import { Router } from "express";
import jwt from "jsonwebtoken";
import { register, calculateReputationScore, getUserCredentials } from "../db";

export const userRouter = Router();

const SALT_ROUNDS = 10;

userRouter.post("/api/register", async (req, res) => {
    const { username, password } = req.body;

    try {
        const salt = await bcrypt.genSalt(SALT_ROUNDS);
        const pwHash = await bcrypt.hash(password.trim(), salt);
        await register(username, pwHash, salt);
        res.json({ success: true });
    } catch (err) {
        res.json({ success: false, error: err.detail });
    }
});

userRouter.post("/api/login", async (req, res) => {
    const { username, password } = req.body;

    const handleError = (err) => {
        res.status(403).json({ success: false, error: err });
    }

    // on successful logins, send tokens to the user
    const handleLogin = (cmp, userId = "") => {
        if (!cmp)
            handleError("Incorrect username/password");
        else {
            const token = jwt.sign(
                { username: username, userId: userId },
                process.env.ACCESS_TOKEN_SECRET,
                { expiresIn: "30d" }
            );

            const user = {
                username: username,
                userId: userId,
                authToken: token
            };

            res.cookie("jwtLogin", token, { maxAge: 30 * 24 * 60 * 60 * 1000 });
            res.cookie("username", username, { maxAge: 30 * 24 * 60 * 60 * 1000 });
            res.json({ success: true, user: user });
        }
    }

    try {
        const data = await getUserCredentials(username);
        if (data.rowCount === 0) {
            handleError("Incorrect username/password");
            return;
        }

        const row = data.rows[0];
        const pwHash = row["password_hash"];
        const cmpRes = await bcrypt.compare(password.trim(), pwHash);
        handleLogin(cmpRes, row["user_id"]);
    } catch (err) {
        handleError(err.detail);
    }
});


userRouter.post("/api/reputation", async (req, res) => {
    try {
        const { userId } = req.body;
        const repScore = await calculateReputationScore(userId);
        res.json({ success: true, reputationScore: repScore });
    } catch (err) {
        res.json({ success: false, error: err.detail });
    }
});


/**
 * 
 * Reads the authorisation header for a JWT and returns the decoded form
 * @param {Request} req 
 * @returns {string}
 */
export const getDecodedToken = (req) => {
    const authorization = req.headers.authorization;
    if (!authorization || !authorization.startsWith("Bearer "))
        return null;
    const token = authorization.replace("Bearer ", "");
    const decodedToken = jwt.verify(token, process.env.ACCESS_TOKEN_SECRET);
    return decodedToken
};


export const authenticateUser = (req, res, next) => {
    let decodedToken;

    try {
        decodedToken = getDecodedToken(req);
    } catch (err) {
        if (err.name === "TokenExpiredError") {
            res.json({ success: false, error: "Session token has expired, please relogin" });
        }
    }

    if (decodedToken.userId) {
        req.decodedToken = decodedToken;
        next();
    }
    else
        res.status(403).send("Unauthorised");
}