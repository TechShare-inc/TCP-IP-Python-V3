# Feedback Fields

`FeedbackDtype` is a NumPy structured dtype for the 1440-byte feedback packet.

Use `PROTOCOL_FIELD_MAP` when you need original protocol naming for selected
fields such as:

- `actual_tcp_force` → `actual_TCP_force`
- `tcp_speed_actual` → `TCP_speed_actual`
- `tcp_force` → `TCP_force`
