# diagnostic
This repository is designed to systematically check and fix system issues as they come up.

# Diagnostic Core (`diagnostic-core`)

A zero-trust, standalone diagnostic and environment auditing module designed for `PMR-Pubclications` architectures. 

## Features
- **Deterministic Transparency:** Real-time, timestamped logging (`[PASS]`, `[WARN]`, `[CRITICAL]`, `[ACTIVE]`) for auditors and engineers.
- **Dynamic Path Resolution:** Inspects execution boundaries and sibling repositories relative to runtime location without hardcoded paths.
- **Cryptographic Asset Auditing:** Verifies identity certificates, private keys, and Root CAs before systems bind to network sockets.

## Integration
Include as a header-only interface library in your CMake project:
```cmake
add_subdirectory(diagnostic-core)
target_link_libraries(your_target PRIVATE DiagnosticCore)


## Consumption in Other Projects
To include `diagnostic-core` in your project's CMake build:

1. Add it as a submodule or subdirectory:
   ```cmake
   add_subdirectory(path/to/diagnostic-core)

