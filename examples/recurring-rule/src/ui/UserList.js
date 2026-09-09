// The approved path: UI imports the API layer, not the database.
// Must stay clean (no findings) in both red and green runs.
import { getUser } from "../api/users.js";

export function renderUserList(id) {
  return getUser(id).name;
}
