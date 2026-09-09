# Tool adapters: a small contract an agent can use

Theo describes a video-attachment gap and his upload skill around [05:52–06:48](https://www.youtube.com/watch?v=xmGY276gEFY&t=352s). The observed screen contains a skill name and trigger, the environment-variable name `FILE_HOST_TOKEN`, and an HTTP PUT command to `files.tslop.org` using an upload-token header. The shown instructions specify reading the public URL from the response body; the PUT request path includes a filename. No token value, server code or successful invocation is shown.

Treat the missing GitHub operation as Theo's reported experience at the time. Verify the current tool surface before concluding a new service is needed. The public service was not called during this research.

## Reuse an existing transport

Inspect the existing CLI, API, MCP tool and supported host capability. Establish the missing operation from the actual failed attempt or the user's requested capability. A thin script with structured output can be enough. Reuse authorized accounts, scoped secret delivery and evidence storage. Seek new authorization only for consequential external effects that the session does not already cover.

An illustrative contract might be:

```text
upload-asset <file>
  success: {"url":"https://example.invalid/asset","bytes":1234}
  failure: {"code":"TOO_LARGE","message":"...","limitBytes":...}
```

Specify actual configured size/type limits, authentication errors, retryable transport errors, and retention. Enforce boundaries in executable code where the adapter depends on them. These are design recommendations, not claims about Theo's implementation. Returning a URL does not authorize posting it to others.

## Document and verify the consumer path

The skill needs a task-specific trigger, exact supported invocation, expected outputs, useful errors and the existing credential-loader name. Keep secret values out. Run the previously blocked operation through the intended agent route; verify that the file or response is usable there and that a realistic failure is intelligible. A one-off script needs proof at its actual script interface; a reusable agent adapter needs the in-agent result.

Keep output concise enough for the consumer while preserving access to complete evidence. For side-effectful work followed by structured output, preserve the completed work and session identity and repair extraction separately. A prompt saying extraction is read-only does not mechanically restrict its tools; inspect the actual host attachment before claiming that property.
