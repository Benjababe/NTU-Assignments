import { pool } from "./db";


export const createEtcObjectImageTbl = async () => {
    const objectDDL = `
        CREATE TABLE IF NOT EXISTS "etc_object_image" (
            etc_object_image_id INT GENERATED ALWAYS AS IDENTITY,
            etc_object_id INT REFERENCES "etc_object"(etc_object_id),
            created_dt TIMESTAMP DEFAULT NOW(),
            path TEXT,
            PRIMARY KEY ("etc_object_image_id")
        );`;
    await pool.query(objectDDL, []);
}

/**
 * 
 * @param {number} etcObjectId Id of etc object to select
 */
export const selectEtcObjectImages = async (etcObjectId) => {
    const query = `
        SELECT path
        FROM "etc_object_image"
        WHERE etc_object_id=$1
    `;

    const data = await pool.query(query, [etcObjectId]);
    return data;
}

/**
 * 
 * @param {number} etcObjectId Id of etc object that was added
 * @param {Express.Multer.File} image Uploaded image
 */
export const insertEtcObjectImage = async (etcObjectId, image) => {
    const query = `
        INSERT INTO \"etc_object_image\" (etc_object_id, path) 
        VALUES ($1, $2)
    `;
    const values = [
        etcObjectId,
        `/images/${image.filename}`
    ];

    const data = await pool.query(query, values);
    return data;
};

