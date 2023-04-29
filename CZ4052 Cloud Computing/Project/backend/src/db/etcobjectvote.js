import { pool } from "./db";
import { calculateReputationScore } from "./user";


export const createEtcObjectVoteTbl = async () => {
    const objectDDL = `
        CREATE TABLE IF NOT EXISTS "etc_object_vote" (
            etc_object_id INT NOT NULL,
            user_id INT REFERENCES "user"(user_id),
            created_dt TIMESTAMP DEFAULT NOW(),
            vote_val INT NOT NULL DEFAULT 0,
            PRIMARY KEY ("etc_object_id", "user_id")
        );`;
    await pool.query(objectDDL, []);
}


/**
 * 
 * @param {number} userId User to retrieve votes for
 */
export const selectEtcObjectVote = async (userId) => {
    const query = `
            SELECT eov.user_id, 
                SUM(vote_val) AS vote_tally
            FROM "etc_object_vote" AS eov
            JOIN "etc_object" AS eo ON (eo.etc_object_id=eov.etc_object_id)
            WHERE eo.user_id=$1
            GROUP BY eov.user_id;`;
    const data = await pool.query(query, [userId]);
    return data;
};


/**
 * 
 * @param {number} etcObjectId Id of etc object that was voted on
 * @param {number} userId Id of the user who voted
 * @param {number} voteVal Value of the vote. 1 for positive, -1 for negative.
 */
export const insertEtcObjectVote = async (etcObjectId, userId, voteVal) => {
    const query = `
        INSERT INTO \"etc_object_vote\" (etc_object_id, user_id, vote_val) 
        VALUES ($1, $2, $3)
        ON CONFLICT (etc_object_id, user_id) DO UPDATE SET
            vote_val=$3`;
    const values = [
        etcObjectId,
        userId,
        voteVal
    ];

    const data = await pool.query(query, values);
    await calculateReputationScore(-1, etcObjectId);
    return data;
};