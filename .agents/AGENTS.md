# Workspace Rules & Behavioral Guardrails

### SVG Generation Guardrails for GitHub README Embeds
When generating SVG assets intended for GitHub README display:
1. Always escape bare ampersands in `<text>` elements as `&amp;`.
2. Use XML attributes (`rx="10"`, `ry="10"`) instead of CSS properties (`rx: 10px;`) for shape presentation.
3. Ensure base element visibility does not depend on hidden `opacity: 0` animation wrappers.
