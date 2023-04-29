import { Router } from "express";
import { insertEtcObjectVote } from "../db";
import { authenticateUser } from "./user";

export const objectVoteRouter = Router();

// user votes for an existing Etc object
objectVoteRouter.post("/api/objectVote", authenticateUser, async (req, res) => {
    const { etcObjectId, voteVal } = req.body;
    const userId = req.decodedToken.userId;

    try {
        await insertEtcObjectVote(etcObjectId, userId, voteVal);
        res.json({ success: true, voteVal: voteVal });
    } catch (e) {
        res.json({ success: false });
    }
});