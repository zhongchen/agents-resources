---
title: opencode v2 loads v1 plugins but silently never calls their hooks
summary: opencode 2.x needs { id, setup(ctx) } and ctx.tool.hook; v1 hooks and the server property never run
tags: [opencode, config]
date: 2026-10-12
confidence: confirmed
---

**Problem:** A plugin written for opencode v1 (`export const MyPlugin =
async () => ({ "tool.execute.before": async (input, output) => {...} })`),
or a v2 default export that puts the v1 function in a `server` property,
loads in opencode 2.x without any error, but its hooks never fire.

**Cause:** The 2.x plugin loader only decodes `export default { id, setup }`
(or `{ id, effect }`) from the module. Everything else, including a `server`
property, is ignored: v1 implementations do not run in v2. Hook names also
change: `tool.execute.before` becomes
`ctx.tool.hook("execute.before", (event) => {...})` with one mutable `event`
(`event.tool`, `event.input`), not separate `(input, output)` arguments. The
public plugins doc page still shows the v1 API; current v2 docs live under
/build/plugins in the anomalyco/opencode repo (services/www).

**Fix / Fact:** Port the plugin to v2:

```js
export default {
  id: "my-plugin",
  async setup(ctx) {
    await ctx.tool.hook("execute.before", async (event) => {
      if (event.tool === "shell") {
        event.input.command = /* rewritten */
      }
    })
  },
}
```

The bash tool is named `shell` in v2; its input is `{ command, workdir }`.
`setup` may return a cleanup function. The v1-to-v2 hook mapping table is in
services/www/src/docs/content/build/plugins/migrate-v1.mdx in that repo.

**Applies to:** opencode >= 2.0, any plugin written against the v1 plugin
API (`@opencode-ai/plugin`, `tool.execute.before`-style hooks).
