# Keep contracts consistent across the application

Use this when agents repeatedly invent mismatched data shapes between storage, APIs and the interface.

Theo describes the satisfaction of composing database tooling, RPC and typed UI calls at [13:49–14:17](https://www.youtube.com/watch?v=xmGY276gEFY&t=829s). He uses Prisma and tRPC as his example. The procedure below is an adaptation; the video does not demonstrate its implementation.

## Start with one important object

Pick a single object that crosses the application, such as a lead, order or message. Trace where it is stored, transformed, returned and displayed. Find manually copied interfaces and unchecked casts along that path.

Choose the existing authoritative contract. For an external API, that may be its schema and generated client. In a TypeScript application, it may be the server procedure's inferred output. TypeScript supports deriving types from existing values and types. [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html).

Avoid changing frameworks to copy the video's example. tRPC is one option for sharing inferred contracts across a TypeScript client and server. It catches certain mismatches at build time. [tRPC documentation](https://trpc.io/docs/).

## Connect the layers deliberately

1. Define the data that the UI actually needs. Keep private storage fields out of the public response.
2. Reuse or derive the client contract from that public response. Remove competing manual definitions for this object.
3. Validate untrusted input at runtime. Keep authentication and authorization at the server boundary.
4. Add the type-check command to the existing feedback path if it is missing.
5. Add a focused runtime check for a business rule the compiler cannot establish.

For example, changing a public `displayName` field to `name` should expose client code that still expects `displayName`. A lead created for company A must still be unavailable to company B, regardless of whether both responses share a valid type.

## Verify the intended benefit

In an isolated working copy, deliberately make an incompatible contract change and run the existing type check. Confirm it identifies the consumer that needs updating. Restore or complete the change and confirm the legitimate path passes.

Separately exercise the invalid-input and unauthorized-access cases at the real server boundary. A compiler success says nothing about a requester's permissions, stale deployed clients, or malformed network input.

For separately deployed clients, use additive changes or an explicit compatibility policy. Shared source types cannot make an old deployed client update itself.

## Keep it small

Apply this to the observed mismatch first. Expand only where duplicate contracts create demonstrated maintenance costs. Use readable domain names and a short boundary comment so the next agent can find the intended extension point.

Related: [knowledge placement](05-knowledge-and-instructions.md), [critical journey tests](02-critical-journey-tests.md).
