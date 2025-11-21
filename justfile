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

# Install Docusaurus dependencies
[group("docusaurus")]
docs-install:
    @echo "📦 Installing Docusaurus dependencies..."
    cd docusaurus && yarn install

# Start Docusaurus development server
[group("docusaurus")]
docs-dev: docs-install
    @echo "🚀 Starting Docusaurus development server..."
    cd docusaurus && yarn start

# Start Docusaurus development server on specific port
[group("docusaurus")]
docs-dev-port port="3000": docs-install
    @echo "🚀 Starting Docusaurus development server on port {{port}}..."
    cd docusaurus && yarn start --port {{port}}

# Build Docusaurus for production
[group("docusaurus")]
docs-build: docs-install
    @echo "🏗️ Generating API documentation from source..."
    {{uv_run}} python3 ./docusaurus/scripts/generate-api-docs.py
    @echo "🏗️ Building Docusaurus for production..."
    cd docusaurus && yarn build

# Generate API documentation from SDK source code
[group("docusaurus")]
docs-generate-api:
    @echo "📝 Generating API documentation from source..."
    {{uv_run}} python3 ./docusaurus/scripts/generate-api-docs.py

# Serve built Docusaurus site locally
[group("docusaurus")]
docs-serve: docs-build
    @echo "🌐 Serving built Docusaurus site..."
    cd docusaurus && yarn serve

# Clean Docusaurus build artifacts
[group("docusaurus")]
docs-clean:
    @echo "🧹 Cleaning Docusaurus build artifacts..."
    cd docusaurus && rm -rf build .docusaurus

# Show available documentation commands
[group("docusaurus")]
docs-help:
    @echo "📚 Docusaurus Commands:"
    @echo "  docs-install        - Install dependencies"
    @echo "  docs-dev            - Start development server"
    @echo "  docs-dev-port       - Start dev server on specific port"
    @echo "  docs-build          - Build for production (includes API docs generation)"
    @echo "  docs-generate-api   - Generate API docs from SDK source"
    @echo "  docs-serve          - Serve built site"
    @echo "  docs-clean          - Clean build artifacts"