// Illustrative database client. This demo never connects to anything.
export const db = {
  query(_sql) {
    throw new Error("not a real database");
  },
};
