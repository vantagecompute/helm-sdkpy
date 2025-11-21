#!/usr/bin/env python3
"""Generate API documentation from helmpy docstrings."""

import inspect
import json
import sys
from pathlib import Path

# Add helmpy to path
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

# Import after adding to path
from helmpy import Configuration  # noqa: E402
from helmpy.actions import Install, Upgrade, Uninstall, List, Status, Rollback, GetValues, History  # noqa: E402
from helmpy.chart import Pull, Show, Test, Lint, Package  # noqa: E402
from helmpy.repo import RepoAdd, RepoRemove, RepoList, RepoUpdate  # noqa: E402
from helmpy import exceptions  # noqa: E402


def get_signature(obj):
    """Get function signature as string."""
    try:
        return str(inspect.signature(obj))
    except (ValueError, TypeError):
        return "()"


def format_docstring(doc):
    """Format docstring to convert Python interactive code to proper markdown."""
    if not doc:
        return ""

    lines = doc.split("\n")
    result = []
    in_code_block = False
    code_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect start of Python interactive code (>>> possibly with leading spaces)
        if stripped.startswith(">>>"):
            if not in_code_block:
                in_code_block = True
                result.append("")
                result.append("```python")
            # Remove leading whitespace for code block content
            code_lines.append(stripped)
            i += 1

            # Continue collecting code lines (..., >>>, or empty lines within code)
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                if next_stripped.startswith(">>>") or next_stripped.startswith("..."):
                    code_lines.append(next_stripped)
                    i += 1
                elif in_code_block and next_stripped == "":
                    code_lines.append("")
                    i += 1
                else:
                    # End of code block
                    result.extend(code_lines)
                    result.append("```")
                    result.append("")
                    in_code_block = False
                    code_lines = []
                    break
        else:
            result.append(line)
            i += 1

    # Close any remaining code block
    if in_code_block and code_lines:
        result.extend(code_lines)
        result.append("```")

    return "\n".join(result)


def format_class_docs(cls, class_name):
    """Generate markdown documentation for a class."""
    lines = []
    lines.append(f"## {class_name}\n")

    # Class docstring
    doc = inspect.getdoc(cls)
    if doc:
        formatted_doc = format_docstring(doc)
        lines.append(f"{formatted_doc}\n")

    # Properties
    props = [
        (n, o)
        for n, o in inspect.getmembers(cls)
        if isinstance(inspect.getattr_static(cls, n, None), property) and not n.startswith("_")
    ]

    if props:
        lines.append("### Properties\n")
        for name, obj in props:
            lines.append(f"#### `{name}`\n")
            prop_doc = inspect.getdoc(obj)
            if prop_doc:
                formatted_prop_doc = format_docstring(prop_doc)
                lines.append(f"{formatted_prop_doc}\n")

    # Methods
    methods = [
        (n, o)
        for n, o in inspect.getmembers(cls, predicate=inspect.isfunction)
        if not n.startswith("_") or n in ["__enter__", "__exit__"]
    ]

    if methods:
        lines.append("### Methods\n")
        for name, method in methods:
            sig = get_signature(method)
            lines.append(f"#### `{name}{sig}`\n")
            method_doc = inspect.getdoc(method)
            if method_doc:
                formatted_method_doc = format_docstring(method_doc)
                lines.append(f"{formatted_method_doc}\n")

    return "\n".join(lines)


def generate_actions_docs(output_dir):
    """Generate Helm Actions API documentation."""
    content = [
        "---",
        "sidebar_position: 1",
        "---",
        "",
        "# Actions API",
        "",
        "Core Helm actions for managing releases and deployments.",
        "",
        format_class_docs(Configuration, "Configuration"),
        "",
        format_class_docs(Install, "Install"),
        "",
        format_class_docs(Upgrade, "Upgrade"),
        "",
        format_class_docs(Uninstall, "Uninstall"),
        "",
        format_class_docs(List, "List"),
        "",
        format_class_docs(Status, "Status"),
        "",
        format_class_docs(Rollback, "Rollback"),
        "",
        format_class_docs(GetValues, "GetValues"),
        "",
        format_class_docs(History, "History"),
    ]

    with open(output_dir / "actions.md", "w") as f:
        f.write("\n".join(content))


def generate_chart_docs(output_dir):
    """Generate Chart API documentation."""
    content = [
        "---",
        "sidebar_position: 2",
        "---",
        "",
        "# Chart API",
        "",
        "Chart operations for managing Helm charts.",
        "",
        format_class_docs(Pull, "Pull"),
        "",
        format_class_docs(Show, "Show"),
        "",
        format_class_docs(Test, "Test"),
        "",
        format_class_docs(Lint, "Lint"),
        "",
        format_class_docs(Package, "Package"),
    ]

    with open(output_dir / "chart.md", "w") as f:
        f.write("\n".join(content))


def generate_repo_docs(output_dir):
    """Generate Repository API documentation."""
    content = [
        "---",
        "sidebar_position: 3",
        "---",
        "",
        "# Repository API",
        "",
        "Repository management operations for Helm chart repositories.",
        "",
        format_class_docs(RepoAdd, "RepoAdd"),
        "",
        format_class_docs(RepoRemove, "RepoRemove"),
        "",
        format_class_docs(RepoList, "RepoList"),
        "",
        format_class_docs(RepoUpdate, "RepoUpdate"),
    ]

    with open(output_dir / "repo.md", "w") as f:
        f.write("\n".join(content))


def generate_exceptions_docs(output_dir):
    """Generate exceptions documentation."""
    content = [
        "---",
        "sidebar_position: 4",
        "---",
        "",
        "# Exceptions",
        "",
        "## Exception Hierarchy",
        "",
        "```",
        "HelmError (base)",
        "├── InstallError",
        "├── UpgradeError",
        "├── UninstallError",
        "├── ReleaseError",
        "├── RollbackError",
        "├── ChartError",
        "└── HelmLibraryNotFound",
        "```",
        "",
    ]

    # Get all exception classes from the exceptions module
    exc_classes = [
        obj
        for name, obj in inspect.getmembers(exceptions)
        if inspect.isclass(obj) and issubclass(obj, Exception)
    ]

    for exc_cls in exc_classes:
        content.append(f"## `{exc_cls.__name__}`\n")
        doc = inspect.getdoc(exc_cls)
        if doc:
            formatted_doc = format_docstring(doc)
            content.append(f"{formatted_doc}\n")

    with open(output_dir / "exceptions.md", "w") as f:
        f.write("\n".join(content))


def main():
    """Generate all API documentation."""
    docs_dir = Path(__file__).parent.parent / "docs" / "api"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Create category config
    category_config = {
        "label": "API Reference",
        "position": 4,
        "link": {
            "type": "generated-index",
            "title": "helmpy API Reference",
            "description": "Complete API documentation for helmpy",
            "slug": "/api",
        },
    }

    with open(docs_dir / "_category_.json", "w") as f:
        json.dump(category_config, f, indent=2)

    print("Generating API documentation...")
    print("  - actions.md")
    generate_actions_docs(docs_dir)
    print("  - chart.md")
    generate_chart_docs(docs_dir)
    print("  - repo.md")
    generate_repo_docs(docs_dir)
    print("  - exceptions.md")
    generate_exceptions_docs(docs_dir)
    print(f"\nAPI documentation generated in {docs_dir}")


if __name__ == "__main__":
    main()
