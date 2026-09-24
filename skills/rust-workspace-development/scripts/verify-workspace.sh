#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
powershell -Command "& 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat'; cargo check --workspace"
