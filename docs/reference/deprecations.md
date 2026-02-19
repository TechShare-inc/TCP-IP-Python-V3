# Deprecations

The package keeps PascalCase command aliases for backward compatibility.

- New code should use `snake_case` methods.
- Deprecated aliases emit `DeprecationWarning`.

Example:

- deprecated: `EnableRobot()`
- preferred: `enable_robot()`
