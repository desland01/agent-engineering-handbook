// The recurring mistake this demo encodes: a UI file reaching past the API
// layer straight into the database. Must be rejected once the rule is enabled.
import { db } from "../db/client.js";

export function renderUserName(id) {
  const user = db.query(`select name from users where id = ${id}`);
  return user.name;
}
