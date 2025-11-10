# Milestone 3 – SoupReplacer Technical Brief

## Context
Milestone 2 introduced `SoupReplacer(og_tag, alt_tag)` so consumers could rename tags during parsing. Milestone 3 expands that API with optional transformer callables:

- `name_xformer(tag) -> str | None`
- `attrs_xformer(tag) -> Mapping | None`
- `xformer(tag) -> None`

The goal is to unburden application code from a second traversal when large documents require structural edits mid-parse.

## Evaluation
- **Developer ergonomics**
  - Pair-mode remains the fastest way to express a rename (`SoupReplacer("b", "blockquote")`). That simplicity is worth keeping because it covers the common “change this one tag everywhere” use case with zero extra ceremony.
  - Transformer-mode trades a modest increase in surface area for large wins: conditional renames, attribute normalization, and arbitrary mutations are now possible without re-walking the tree.
- **Performance characteristics**
  - Both modes operate during parsing, so they scale linearly with input size and avoid post-processing passes.
  - Transformer callbacks run per matched tag, so documentation should caution users to keep them lightweight—especially when parsing very large files.
- **API design**
  - The new keyword arguments compose cleanly; they are mutually independent and can be combined.
  - Implementation-wise we treat pair-mode as sugar that internally installs a `name_xformer`, meaning there is one code path to maintain.
  - Reset hooks were necessary to keep state per parse; this aligns with how `SoupStrainer` already integrates with `BeautifulSoup`.
- **Risks / Mitigations**
  - Callbacks can throw exceptions; we guard each transformer invocation and fall back to pre-transform names to avoid breaking parsing.
  - End-tag handling now tracks `(original_name, new_name)` pairs; tests cover nested renames and sibling layouts to prevent regressions.

## Side-by-Side Overview

| Aspect | Pair Mode | Transformer Mode |
| --- | --- | --- |
| Definition | `SoupReplacer("b", "blockquote")` | `SoupReplacer(name_xformer=..., attrs_xformer=..., xformer=...)` |
| Transformation scope | Tag name only | Name, attributes, entire `Tag` instance |
| Transformation style | Fixed mapping (pair) | Dynamic functions (callbacks) |
| When to use | Static renames | Conditional logic, attribute tweaks, cleanup |
| Ideal for | Quick rename, single-purpose adjustments | Content-aware processing workflows |
| Execution time | During parsing (avoids second traversal) | During parsing (same one-pass benefit) |

## Recommendation
Keep both entry points:
1. Pair-mode (`SoupReplacer("b", "blockquote")`) for quick renames.
2. Transformer-mode for advanced use cases.

Document the transformer hooks as the preferred extension mechanism. Encourage simple pure functions where possible (e.g., return new attribute dictionaries instead of mutating shared state) and highlight that callbacks run during parsing, so they should avoid heavy I/O or global side effects.

With these adjustments, SoupReplacer becomes a practical, composable extension point for BeautifulSoup without imposing extra cost on existing users.
