# 10: Codebase navigation and tooling

How-to: find where to change code in an unfamiliar codebase, and wrap external tools so
their failures are safe. Adapted from `docs/code-map.md`, `tools/dep_graph.py`,
`tools/decompctx.py`, and `tools/download_tool.py` in the Melee for Mac snapshot
(`t3dotgg/melee4mac`, head `a276aeb70f9879204d891d967f1c9442523568e1`). Companion guide:
[09-verification-contracts.md](09-verification-contracts.md).

## Part A — finding the right code

1. **Start from behavior, not from files.** Melee's code map is a table of tasks →
   entry file → named functions → deeper guide ([docs/code-map.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code-map.md)). Before
   grepping, write one sentence describing the behavior you need to touch; if you
   cannot, you are not ready to edit.
2. **Read the types before guessing names.** Melee keeps structure definitions in
   `types.h` per module and treats offset-named or address-named identifiers as clues,
   not placeholders to rename on a hunch: a matching executable does not establish that a newly chosen source name describes the behavior correctly
   ([docs/code-map.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code-map.md)). In any codebase: confirm a field's meaning from its
   reads and writes, not its name.
3. **Build a dependency view from real artifacts when source navigation is incomplete.** For callback-
   or table-driven code, a source grep misses connections. Melee compiles all units
   (`ninja all_source`), then derives file-level dependencies from object symbols with
   `tools/dep_graph.py --deps/--rdeps/--cycles/--chain`, cross-checking unit lists
   between `configure.py` and the generated build config and erroring on any mismatch
   ([tools/dep_graph.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/dep_graph.py); usage in [docs/code-map.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code-map.md)). The
   equivalent in most projects: `nm`, `objdump`, an LSP's references, or
   `compile_commands.json` for include paths.
4. **Generate a self-contained context for one unit of work.** `tools/decompctx.py`
   expands one source file plus its headers into a single context file with a
   dependency sidecar, so an agent or reviewer sees everything relevant without the
   whole tree (`tools/decompctx.py`; Ninja wires it per file in
   [docs/code/context-generation.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code/context-generation.md)). For your task: assemble the one file plus
   its headers/config, and record what you excluded.
5. **Know what your navigation output does not tell you.** Melee documents that its
   object graph is not a call graph and says nothing about callback timing
   ([docs/code-map.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code-map.md)), and that its context expander does not evaluate `#if`
   ([docs/code/context-generation.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/docs/code/context-generation.md)). State the equivalent limits of whatever
   view you produced.
6. **Write the map down for the next reader.** After resolving an unfamiliar area, add
   the entry: task → file → function → guide, as `docs/code-map.md` does. Ownership is
   documentation plus explicit scopes — Melee gives each parallel agent a worktree and
   an owned-file list ([AGENTS.md](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/AGENTS.md)).

## Part B — safe external-tool adapters

1. **One module per tool, with a URL/source table.** `tools/download_tool.py` maps six
   tool names to small per-tool URL functions handling OS/arch naming
   ([tools/download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/download_tool.py)). Keep per-tool quirks in one place.
2. **Download to a temp file in the destination directory, then atomic-replace.** The
   staged file is chmod'ed, size-checked against `Content-Length`, and swapped in with
   `Path.replace`; a `finally` unlink removes residue
   ([tools/download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/download_tool.py)). An interrupted download leaves the previous
   working tool intact — tested for both a short response and a mid-copy exception
   ([tools/tests/test_download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_download_tool.py)).
3. **Detect truncation explicitly.** Sized HTTP reads can reach EOF without an
   `IncompleteRead` error, so compare received bytes to `Content-Length` and raise with
   both numbers ([tools/download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/download_tool.py), note at
   [tools/tests/test_download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_download_tool.py)). The same applies to any partial file
   your tools produce: check the expected size or a footer before accepting it.
4. **Handle the environment failure you actually have, narrowly.** The certificate
   retry fires only on `CERTIFICATE_VERIFY_FAILED` and exits 1 with an install hint
   when the fallback package is missing ([tools/download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/download_tool.py)).
5. **Discover tool binaries through a fallback chain.** `find_nm_tool` prefers the
   project's bundled binary, then cross-toolchain, devkit, LLVM, and system `nm`, and
   raises a message naming the options ([tools/dep_graph.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/dep_graph.py)). Pin what you pin;
   fall back where fallback is safe.
6. **Test the failure cases, not just the happy path.** The download suite asserts the
   old tool survives each failure and that no temp files remain
   ([tools/tests/test_download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/tests/test_download_tool.py)). Your adapter is done when its worst day
   is a clean nonzero exit and unchanged state.

## Acceptance evidence

- For navigation: you can name the file and function you will change, the callers and relationships inspected, and what your view cannot show.
- For adapters: a test run showing a failed download leaves the previous tool byte-
  identical and the directory free of temp files. Note that Melee's guarantee covers
  single-file downloads only; its zip path extracts in place
  ([tools/download_tool.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/download_tool.py)) — a boundary worth checking in any adapter you copy.

## Troubleshooting

If a navigation tool reports nothing, build its inputs first — `dep_graph.py` stops
with "Run ninja all_source" when objects are missing ([tools/dep_graph.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/dep_graph.py)).
If a context or generated file is stale after a failure, Melee clears per-run state at
the start of each invocation and writes output atomically
([tools/decompctx.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/decompctx.py)); copy that order. If a check keeps passing when
it should fail, see guide 09 step 7: report what the environment could actually verify.
