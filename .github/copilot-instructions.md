# GitHub Copilot Instructions for Helmpy

## Python Command Execution

**ALWAYS use `uv run` for Python commands in this project.**

This project uses `uv` for dependency management and virtual environment handling. All Python commands must be prefixed with `uv run`.

### Examples:

✅ **CORRECT:**
- `uv run python script.py`


❌ **INCORRECT:**
- `python script.py`
- `pytest tests/`
- `python -m vantage_cli.main`
- `vantage --help`
- `coverage run`
- `mypy .`
- `black .`
- `ruff check`

### Just Commands (Primary Development Workflow):

**Testing:**
- `just unit` - Run unit tests with coverage (80% threshold)
- `just integration` - Run integration tests  
- `just coverage-all` - Run full test suite with combined coverage

**Code Quality:**
- `just typecheck` - Run static type checker (pyright)
- `just lint` - Check code against style standards (codespell + ruff)
- `just fmt` - Apply coding style standards (ruff format + fix)

**Documentation:**
- `just docs-dev` - Start Docusaurus development server
- `just docs-dev-port [port]` - Start dev server on specific port
- `just docs-build` - Build documentation for production
- `just docs-serve` - Serve built documentation
- `just docs-clean` - Clean documentation build artifacts
- `just docs-help` - Show documentation commands

**Development:**
- `just lock` - Regenerate uv.lock file

### Installation Commands:
- Install dependencies: `uv sync`
- Add new dependency: `uv add package-name`
- Add dev dependency: `uv add --dev package-name`
- Regenerate lock: `just lock`

## Project Structure

This is a Python CLI application using:
- `uv` for dependency management
- `pytest` for testing
- `just` for task automation
- `Helmpy` as the main package
- `docusaurus` for documentation
- `examples/` directory for usage patterns
## Testing Patterns

When writing tests, ensure:
1. Use `uv run pytest` to execute tests
2. Place tests in the `tests/` directory
3. Use fixtures for setup/teardown


## Test Patterns

When working with tests, ensure:
1. MockConsole includes all necessary Rich console methods
3. All async functions are properly awaited in tests
4. Function signatures match current implementation

## Never Forget

**EVERY Python command MUST start with `uv run`** - this is critical for proper dependency resolution and virtual environment isolation in this project.