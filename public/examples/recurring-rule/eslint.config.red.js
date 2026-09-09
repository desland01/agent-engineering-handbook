// "Red" configuration: identical project, but the restriction is absent.
// Running the lint with this config must PASS even though src/ui/UserCard.js
// imports the database client directly. That pass is the failure evidence:
// without the rule, the recurring mistake is invisible to every check.
export default [
  {
    ignores: ["node_modules/**"],
  },
  {
    files: ["src/ui/**/*.js"],
    rules: {},
  },
];
