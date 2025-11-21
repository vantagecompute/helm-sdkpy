uv := require("uv")

project_dir := justfile_directory()
src_dir := project_dir / "helmpy"
tests_dir := project_dir / "tests"

export PY_COLORS := "1"
export PYTHONBREAKPOINT := "pdb.set_trace"
export PYTHONPATH := project_dir / "helmpy"

uv_run := "uv run --frozen"

[private]
default:
    @just help

# Regenerate uv.lock
[group("dev")]
lock:
    uv lock

# Create a development environment
[group("dev")]
env: lock
    uv sync --extra dev

# Upgrade uv.lock with the latest dependencies
[group("dev")]
upgrade:
    uv lock --upgrade

# Apply coding style standards to code
[group("lint")]
fmt: lock
    {{uv_run}} ruff format {{src_dir}} {{tests_dir}}
    {{uv_run}} ruff check --fix {{src_dir}} {{tests_dir}}

# Check code against coding style standards
[group("lint")]
lint: lock
    {{uv_run}} codespell {{src_dir}}
    {{uv_run}} ruff check {{src_dir}}

# Run static type checker on code
[group("lint")]
typecheck: lock
    {{uv_run}} pyright

# Build the native Go library using Docker (proper/recommended way)
[group("dev")]
build-lib:
    #!/usr/bin/env bash
    set -e
    echo "==> Building native library using Docker"
    docker build --target go-build --tag helmpy-lib-builder .
    docker create --name helmpy-lib-extract helmpy-lib-builder
    docker cp helmpy-lib-extract:/build/helmpy/_lib/. ./helmpy/_lib/
    docker rm helmpy-lib-extract
    echo "==> Library extracted to helmpy/_lib/"
    ls -lh helmpy/_lib/linux-amd64/

# Run unit tests with coverage
[group("test")]
unit: lock build-lib
    {{uv_run}} pytest {{tests_dir}} --cov={{src_dir}} --cov-report=term-missing

# Build helmpy wheel using Docker
build-wheel:
    ./scripts/build_wheel_docker.sh
