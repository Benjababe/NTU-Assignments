import { pool } from "./db";

export const createUserTbl = async () => {
    const userDDL = `
        CREATE TABLE IF NOT EXISTS "user" (
            user_id INT GENERATED ALWAYS AS IDENTITY,
            username VARCHAR(20) NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            reputation_score FLOAT DEFAULT 10,
            PRIMARY KEY ("user_id")
        );`;
    await pool.query(userDDL, []);
}


/**
 * 
 * @param {String} username 
 * @param {String} pwHash 
 * @returns {Promise<Object>}
 */
export const register = async (username, pwHash, salt) => {
    const query = "INSERT INTO \"user\" (username, password_hash, salt) VALUES ($1, $2, $3)";
    const values = [username.trim(), pwHash, salt];

    const data = await pool.query(query, values);
    return data;
};

/**
 * 
 * Used for logging in, fetches the password hash and salt to be compared
 * @param {String} username 
 * @param {String} password 
 * @returns {Promise<Object>}
 */
export const getUserCredentials = async (username) => {
    const query = "SELECT user_id, password_hash, salt FROM \"user\" WHERE username=$1 LIMIT 1";
    const values = [username.trim()];

    const data = await pool.query(query, values);
    return data;
};


/**
 * 
 * @param {number} userId 
 * @returns {Promise<number>}
 */
export const getReputationScore = async (userId) => {
    const query = "SELECT reputation_score FROM \"user\" WHERE user_id=$1"
    const { rows } = await pool.query(query, [userId]);
    return rows[0]["reputation_score"];
}


/**
 * 
 * Calculates, Updates and Returns the reputation score for a given user.
 * Either provide a userId or an etcObjectId tied to the user.
 * @param {number} userId 
 * @param {number} etcObjectId
 * @returns {Promise<number>} Newly calculated reputation score
 */
export const calculateReputationScore = async (userId = -1, etcObjectId = -1) => {
    if (userId === -1 && etcObjectId !== -1) {
        const q1 = `SELECT user_id FROM etc_object WHERE etc_object_id=$1`;
        const { rows } = await pool.query(q1, [etcObjectId]);
        userId = rows[0]["user_id"];
    }

    const q2 = `
            WITH 
            user_votes AS (
                SELECT eov.user_id, 
                    SUM(eov.vote_val::double precision) AS voter_score
                FROM etc_object_vote eov
                JOIN etc_object eo ON eov.etc_object_id=eo.etc_object_id
                WHERE eo.user_id=$1
                GROUP BY eov.user_id
            ), 
            voter_reputation AS (
                SELECT DISTINCT u.user_id, u.reputation_score
                FROM "user" u
                JOIN etc_object_vote eov ON u.user_id=eov.user_id
            ), 
            votes_received AS (
                SELECT eo.user_id,
                    SUM(CASE WHEN vote_val=1 THEN 1 ELSE 0 END)::double precision AS pos_votes_received,
                    SUM(CASE WHEN vote_val=-1 THEN 1 ELSE 0 END)::double precision AS neg_votes_received
                FROM etc_object_vote eov
                JOIN etc_object eo ON eov.etc_object_id=eo.etc_object_id
                GROUP BY eo.user_id
            ),
            votes_given AS (
                SELECT eov.user_id, 
                    COUNT(*)::double precision AS votes_given
                FROM etc_object_vote eov
                JOIN etc_object eo ON eov.etc_object_id=eo.etc_object_id
                GROUP BY eov.user_id
            )
            SELECT COALESCE(
                SUM(
                    uv.voter_score * 
                    (CASE WHEN vrep.reputation_score < 0 THEN 1 / (0.2 - vrep.reputation_score) ELSE vrep.reputation_score END) * 
                    (GREATEST(vrec.pos_votes_received, 1) / GREATEST(vg.votes_given, 1))
                ),
                10
            ) AS new_reputation_score
            FROM user_votes uv
            JOIN voter_reputation vrep ON uv.user_id=vrep.user_id
            LEFT JOIN votes_received vrec ON uv.user_id=vrec.user_id
            LEFT JOIN votes_given vg ON uv.user_id=vg.user_id
    `;
    const { rows } = await pool.query(q2, [userId]);


    const q3 = `UPDATE "user" SET reputation_score=$1 WHERE user_id=$2`;
    await pool.query(q3, [rows[0]["new_reputation_score"], userId]);

    return rows[0]["new_reputation_score"];
}