import { pool } from "./db";
import { insertEtcObjectImage } from "./etcobjectimage";
import format from "pg-format";

export const createEtcObjectTbl = async () => {
    const objectDDL = `
        CREATE TABLE IF NOT EXISTS "etc_object" (
            etc_object_id INT GENERATED ALWAYS AS IDENTITY,
            created_dt TIMESTAMP DEFAULT NOW(),
            user_id INT REFERENCES "user"(user_id),
            name VARCHAR(100) NOT NULL DEFAULT '',
            type VARCHAR(100) NOT NULL,
            lat DOUBLE PRECISION NOT NULL,
            lng DOUBLE PRECISION NOT NULL,
            level VARCHAR(100) NOT NULL,
            comments TEXT,
            status INT NOT NULL DEFAULT 0,
            PRIMARY KEY ("etc_object_id")
        );`;
    await pool.query(objectDDL, []);
}

/**
 * Retrieves all Etc Objects of a map type and are approved
 * @param {string} mapType 
 * @returns 
 */
export const selectEtcObjects = async (mapType) => {
    const query = `
        SELECT eo.etc_object_id AS "id", eo.name, eo.type, 
            eo.lat, eo.lng, eo.level, eo.comments, eo.user_id,
            u.username AS user,
            COALESCE(
                array_agg(eoi.path)
                FILTER (WHERE eoi.path IS NOT NULL),
                '{}'
            ) AS paths
        FROM "etc_object" AS eo
        LEFT JOIN "user" AS u ON (u.user_id=eo.user_id)
        LEFT JOIN "etc_object_image" AS eoi ON (eoi.etc_object_id=eo.etc_object_id)
        WHERE type=$1
            AND status=1
        GROUP BY eo.etc_object_id, u.username
    `;
    const data = await pool.query(query, [mapType]);
    return data;
};


/**
 * 
 * @param {number} userId Id of user who submitted the etc object
 * @param {boolean} trusted Flag whether user is trusted from EtcReputation algorithm
 * @param {Object} etcObject Etc object to insert into map
 * @param {Express.Multer.File[]} images Images uploaded with the Etc object
 */
export const insertEtcObject = async (userId, trusted, etcObject, images) => {
    const status = (trusted) ? 1 : 0;
    const query = `
        INSERT INTO \"etc_object\" (user_id, type, lat, lng, level, comments, status) 
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING etc_object_id`;
    const values = [
        userId,
        etcObject.type,
        etcObject.lat,
        etcObject.lng,
        etcObject.level,
        etcObject.comments,
        status
    ];

    const { rows } = await pool.query(query, values);

    const insertedId = rows[0]["etc_object_id"];
    images.forEach((image) => {
        insertEtcObjectImage(insertedId, image);
    });

    return rows[0];
};


/**
 * 
 * @param {number} userId Id of user who submitted the etc object
 * @param {boolean} trusted Flag whether user is trusted from EtcReputation algorithm
 * @param {Object} etcObject Etc objects to insert into map
 */
export const insertEtcObjectBulk = async (userId, trusted, mapType, etcObjects) => {
    const status = (trusted) ? 1 : 0;
    const query = `
            INSERT INTO "etc_object" (user_id, type, lat, lng, level, comments, status)
            VALUES %L`;
    const values = etcObjects.map(obj => [userId, mapType, obj.lat, obj.lng, obj.level, obj.comments, status]);
    const fmtQuery = format(query, values);

    const { rows } = await pool.query(fmtQuery);
    return rows;
};


/**
 * 
 * @param {number} userId Id of user who submitted the delete request
 * @param {number} etcObjectId Id of Etc object to be deleted
 */
export const deleteEtcObject = async (userId, etcObjectId) => {
    const sQuery = `SELECT user_id FROM "etc_object" WHERE etc_object_id=$1`;
    const { rows } = await pool.query(sQuery, [etcObjectId]);
    const objUserId = rows[0]["user_id"];

    if (objUserId !== userId)
        throw { detail: "User did not submit the object!" };

    const dQuery = `
        UPDATE "etc_object"
        SET status=-1
        WHERE etc_object_id=$1
    `;
    await pool.query(dQuery, [etcObjectId]);
}