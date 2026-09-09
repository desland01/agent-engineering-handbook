// Final configuration: the restriction is enabled.
// Uses only ESLint's built-in `no-restricted-imports` core rule
// (https://eslint.org/docs/latest/rules/no-restricted-imports).
// UI code must go through the typed API layer; database clients are off limits there.
export default [
  {
    ignores: ["node_modules/**"],
  },
  {
    files: ["src/ui/**/*.js"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["**/db", "**/db/**", "@db/*"],
              message:
                "UI code must not import the database directly. Use the API layer in src/api instead.",
            },
          ],
        },
      ],
    },
  },
];
