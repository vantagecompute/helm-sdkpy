# helm-sdkpy Documentation

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Documentation Structure

The documentation is organized as follows:

- `docs/` - Main documentation content (markdown files)
  - `index.md` - Homepage/Overview
  - `installation.md` - Installation guide
  - `usage.md` - Usage examples
  - `api-reference.md` - Hand-written API reference
  - `architecture.md` - SDK architecture documentation
  - `troubleshooting.md` - Common issues and solutions
  - `api/` - Auto-generated API documentation from SDK source
- `scripts/` - Build scripts
  - `generate-api-docs.py` - Generates API docs from Python docstrings

## Installation

```bash
yarn install
```

Or using npm:

```bash
npm install
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### With Just

From the project root:

```bash
just docs-dev
```

## Generate API Documentation

Before building for production, generate API documentation from the SDK source:

```bash
yarn generate-api-docs
```

Or using just:

```bash
just docs-generate-api
```

This script reads the Python SDK source code and generates markdown documentation from docstrings.

## Build

```bash
yarn build
```

This automatically generates API docs and builds static content into the `build` directory.

Using just from project root:

```bash
just docs-build
```

## Serve Built Site

```bash
yarn serve
```

Or:

```bash
just docs-serve
```

## Clean Build Artifacts

```bash
just docs-clean
```

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Documentation Features

### Auto-Generated API Docs

The SDK methods and data models documentation is automatically generated from Python docstrings using the `generate-api-docs.py` script. This ensures the documentation stays in sync with the code.

### Mermaid Diagrams

The documentation supports Mermaid diagrams for visualizing architecture and workflows.

### LLM-Friendly Content

Using `docusaurus-plugin-llms`, the documentation is automatically processed into LLM-friendly formats (llms.txt) for AI tools and assistants.
