import * as pg from "pg";
import { createUserTbl } from "./user";
import { createEtcObjectTbl } from "./etcobject";
import { createEtcObjectVoteTbl } from "./etcobjectvote";

import dotenv from "dotenv"
import { createEtcObjectImageTbl } from "./etcobjectimage";
dotenv.config();

const { Pool } = pg.default;

let dbUsername = "postgres";
let dbPassword = "password";
let dbName = "etcmap";
let dbHost = "localhost";
let dbPort = "5432";

if (process.env.DBUSERNAME)
    dbUsername = process.env.DBUSERNAME.toString();
if (process.env.DBPASSWORD)
    dbPassword = process.env.DBPASSWORD.toString();
if (process.env.DBNAME)
    dbName = process.env.DBNAME.toString();
if (process.env.DBHOST)
    dbHost = process.env.DBHOST.toString();
if (process.env.DBPORT)
    dbPort = process.env.DBPORT.toString();

export const pool = new Pool({
    user: dbUsername,
    password: dbPassword,
    host: dbHost,
    port: dbPort,
    database: dbName,
});

/**
 * Initialises database with schemas if they don't already exist
 */
export const initDB = async () => {
    try {
        await createUserTbl();
        await createEtcObjectTbl();
        await createEtcObjectVoteTbl();
        await createEtcObjectImageTbl();
    } catch (e) {
        console.error("Error with initialising databases");
        console.error(e);
    }
};