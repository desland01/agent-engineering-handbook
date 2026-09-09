// Approved data access path: the API layer is allowed to reach the database.
import { db } from "../db/client.js";

export function getUser(id) {
  return db.query(`select * from users where id = ${id}`);
}
