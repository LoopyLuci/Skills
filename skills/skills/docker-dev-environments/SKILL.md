---
name: docker-dev-environments
description: "Docker build environments with MCP for AI agent control."
tags: [docker, devops, mcp, build-environments, ai-agents]
---

# Docker Development Environments with MCP Integration

## When to Use This Skill

Building reproducible Docker development environments that include:
- Build toolchains (compilers, linkers, SDKs)
- MCP server for AI agent control of build/test/lint workflows
- docker-compose orchestration for multiple services
- Build/test/lint shell scripts that run inside containers

This skill covers the integration layer between Docker, MCP servers, and build systems — not Docker basics or MCP protocol internals (see `mcp-server` skill for MCP details).

## Architecture Pattern

```
┌─────────────────────────────────────────────────────┐
│  docker-compose.yml                                  │
│  ├── base (Dockerfile)                               │
│  │   ├── Build toolchain (Clang/MSVC, CMake, Ninja) │
│  │   ├── SDK (Vulkan, CUDA, etc.)                   │
│  │   ├── MCP server (Python/Rust)                   │
│  │   └── Build/test/lint scripts                    │
│  ├── build service → build.sh                       │
│  ├── test service  → test.sh                        │
│  ├── lint service  → lint.sh                        │
│  ├── ci service    → full pipeline                  │
│  ├── mcp service   → MCP server (long-running)      │
│  └── shell service → interactive bash               │
└─────────────────────────────────────────────────────┘
```

## Dockerfile Construction

### Single-stage pattern (recommended for dev environments)

```dockerfile
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake ninja-build ccache \
    clang-17 clang++-17 clang-tools-17 \
    python3 python3-pip python3-venv \
    git curl jq

RUN python3 -m pip install --break-system-packages mcp
COPY docker/mcp_server.py /opt/mcp/server.py
COPY docker/docker-entrypoint.sh /opt/mcp/entrypoint.sh
COPY docker/build.sh /opt/scripts/build.sh
COPY docker/test.sh /opt/scripts/test.sh
COPY docker/lint.sh /opt/scripts/lint.sh
RUN chmod +x /opt/scripts/*.sh /opt/mcp/entrypoint.sh

ENV CC=clang-17 CXX=clang++-17
ENV PATH="/opt/scripts:${PATH}"
WORKDIR /workspace
ENTRYPOINT ["/opt/mcp/entrypoint.sh"]
```

### Key decisions

- **ccache**: Always include for rebuild speed. Set `CMAKE_C_COMPILER_LAUNCHER=ccache`.
- **compile_commands.json**: Generate in lint profile (`-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`).
- **Entrypoint routing**: Dispatches based on first argument (`mcp`, `build`, `test`, `ci`, `shell`).

## docker-compose.yml Pattern

```yaml
services:
  base:
    build: { context: ., dockerfile: docker/Dockerfile }
    image: myproject:latest
    volumes: [".:/workspace"]
    environment: [CC=clang-17, CXX=clang++-17]

  build:
    extends: base
    entrypoint: ["/opt/scripts/build.sh"]
    profiles: ["build"]

  test:
    extends: base
    entrypoint: ["/opt/scripts/test.sh"]
    profiles: ["test"]

  mcp:
    extends: base
    entrypoint: ["python3", "/opt/mcp/server.py"]
    command: ["--stdio"]
    stdin_open: true
    ports: ["8080:8080"]
    profiles: ["mcp"]

  shell:
    extends: base
    entrypoint: ["bash"]
    stdin_open: true
    tty: true
    profiles: ["shell"]
```

## MCP Server Tool Set

| Tool | Purpose | Returns |
|------|---------|---------|
| `build` | CMake configure + compile | artifacts list |
| `test` | CTest runner with filter | pass/fail counts |
| `lint` | clang-tidy/format/cppcheck | per-linter results |
| `analyze` | Parse report.json | telemetry summary |
| `file_list` | List source files | paths + sizes |
| `file_read` | Read file with line numbers | paginated content |
| `syntax_check` | Single-file compile check | errors/warnings |
| `status` | Environment info | compiler versions |

## Entrypoint Dispatch

```bash
case "${1:-}" in
    mcp)   exec python3 /opt/mcp/server.py --stdio ;;
    build) /opt/scripts/build.sh; exit $? ;;
    test)  /opt/scripts/test.sh; exit $? ;;
    lint)  /opt/scripts/lint.sh "${@:2}"; exit $? ;;
    ci)    /opt/scripts/build.sh && /opt/scripts/test.sh && /opt/scripts/lint.sh ;;
    shell) exec bash ;;
    *)     exec "$@" ;;
esac
```

## Common Pitfalls

- **Docker daemon not running** — On Windows, Docker Desktop WSL2 backend may fail. Check with `docker info` before building. Fall back to local MSVC build.
- **Docker Desktop requires admin** — On Windows, installation needs elevated privileges. Use `winget install Docker.DockerDesktop` in an admin shell.
- **Entrypoint vs command** — `entrypoint` is the executable, `command` is its arguments. Don't put arguments in `entrypoint`.
- **Volume mount permissions** — Linux containers may see different UID/GID. Use `--user` flag or fix permissions in Dockerfile.
- **MCP stdio buffering** — Python's `sys.stdout` is line-buffered by default. Use `sys.stdout.flush()` after each JSON-RPC response.
- **compile_commands.json not generated** — Add `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` to CMake configure for lint tools to work.

## Verification

1. `docker compose run build` produces `build_*/` directory with binaries
2. `docker compose run test` shows pass/fail counts
3. `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | docker compose run mcp` returns tool list
4. `docker compose run shell` gives interactive bash inside the container
5. All scripts pass `bash -n` syntax check
6. MCP server passes `python3 -c "import ast; ast.parse(open('mcp_server.py').read())"`

## Related References

- `references/docker-desktop-windows.md` — Installation and troubleshooting for Docker Desktop on Windows
- `references/docker-removal-windows.md` — Complete Docker removal guide for Windows (7-layer cleanup: engine, WSL2, registry, services, files, env vars, Windows features) with automated PowerShell tooling at `D:\Projects\DockerManager\`
- `references/python-mcp-server-pattern.md` — MCP server implementation patterns for Python
