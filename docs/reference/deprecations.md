# Deprecations

All deprecated backward-compatibility aliases have been removed. The API is
now exclusively `snake_case`.

If you are upgrading from an older version, replace any PascalCase method calls
with their `snake_case` equivalents (e.g. `EnableRobot()` → `enable_robot()`,
`MovJ()` → `mov_j()`). The full mapping is documented in the
[copilot-instructions](../../.github/copilot-instructions.md) protocol name
table under **Section 3b**.
