# Documentation Standard Specification

> **Purpose**: This document defines the standard specification for building documentation sites using VitePress (SSG) and Sphinx (Python API Reference). It is designed to be structured for both humans and AI agents to understand and maintain.
>
> **Tech Stack**:
>
> - **Site Generation**: VitePress (Node.js)
> - **API Reference**: Sphinx (Python) + `sphinx-markdown-builder`
> - **Configuration**: `pyproject.toml` (Python), `package.json` (Node.js)

## Diátaxis Framework Overview

This standard categorizes documentation into four distinct types based on the user's immediate needs.

| **Type**         | **Orientation** | **Role**                                                                    | **Analogy**                 |
| ---------------- | --------------- | --------------------------------------------------------------------------- | --------------------------- |
| **Tutorial**     | Learning        | Acquiring skills through guided exercises under the author's direction.     | Teaching a child to cook    |
| **How-to Guide** | Goal            | Procedures for completing specific, real-world tasks.                       | A recipe in a cookbook       |
| **Reference**    | Information     | Accurate and concise descriptions of technical facts.                       | Nutrition facts label       |
| **Explanation**  | Understanding   | Deepening understanding through background, design rationale, and discussion. | An article on culinary history  |

## Five Principles of Documentation

1. **Audience-first**: Define the reader for each page. Do not mix "Education" for beginners with "Facts" for professionals.
2. **Progressive Disclosure**: Layer information from L1 (Home) → L2 (Getting Started) → L3 (Tutorials/How-to) → L4 (Reference).
3. **Example-driven**: Code samples must be runnable as-is (copy-and-paste) assuming the environment is set up.
4. **Single Source of Truth**: Auto-generate API references from source code docstrings. Use hand-written docs for "Why" (rationale) and "How" (procedures).
5. **AI/LLM Friendly**: Use structured headings, tables, and metadata so AI agents can accurately parse the context.

## Mapping Diátaxis to Site Structure

| **Site Section**    | **Primary Diátaxis Type** | **Content**                                                                  |
| ------------------- | ------------------------- | ---------------------------------------------------------------------------- |
| **Home**            | N/A                       | Tagline, minimal code example                                                |
| **Getting Started** | Mixed (Tagged)            | Installation (How-to), Quick Start (Tutorial), Architecture (Explanation)    |
| **Tutorials**       | Tutorial                  | Learning lessons organized by major workflows                                |
| **How-to Guides**   | How-to                    | Procedures for specific tasks (e.g., "How to configure auth")               |
| **Reference**       | Reference                 | Sphinx-generated API docs, Glossary, Config lists                            |
| **Explanation**     | Explanation               | Design decisions, architecture deep-dives, history                           |

## Directory Structure

```text
.
├── docs/                 # VitePress Source
│   ├── index.md          # Home page
│   ├── getting-started/  # Onboarding (installation, basic concepts)
│   ├── tutorial/         # Tutorials
│   ├── how-to/           # How-to guides
│   ├── explanation/      # Explanations
│   └── reference/
│       ├── index.md      # Reference overview
│       └── api/          # Markdown synced from Sphinx
├── sphinx/               # Sphinx config (conf.py, index.rst)
├── scripts/              # Sync scripts (build-docs.sh)
├── pyproject.toml        # Python dependencies (Sphinx, napoleon, etc.)
└── package.json          # Node.js dependencies (VitePress)
```

## Toolchain Configuration

### Sphinx (Python)

- **Style**: Use Google Style docstrings via `napoleon`.
- **Type Hints**: Set `autodoc_typehints = "description"`.
- **Output**: Use `sphinx-markdown-builder` to generate Markdown for VitePress.

### VitePress (Node.js)

- **Sidebar**: Grouped according to the Diátaxis categories.
- **Links**: Always use relative paths (`[Link](../how-to/page.md)`) for internal cross-references.

## Writing Procedures by Type

### Writing a Tutorial

1. Focus on one workflow and do not mix others.
2. Use first-person plural ("We") to guide the user (e.g., "Let's connect to the API").
3. Include "Expected Output" for every significant step.
4. Minimize explanation — link to "Explanation" pages if deeper context is needed.

### Writing a How-to Guide

1. Start titles with "How to...".
2. Use the imperative mood (e.g., "Configure the credentials").
3. Assume competence; skip basic concept explanations.
4. Clearly state conditional paths (e.g., "If X, then do Y").

### Writing an Explanation

1. Start titles with "About..." or "[Concept] Explained".
2. Describe background, design trade-offs, and comparisons with alternatives.
3. Do not include step-by-step procedures or API parameter lists.

## Maintenance Flow for API Changes

When the API changes, execute this checklist:

1. **Update Docstrings**: Reflect changes in parameters, types, and descriptions in the code.
2. **Run Auto-generation**: Execute `scripts/build-docs.sh` to update `docs/reference/api/`.
3. **Revise Related Docs**:
   - `Reference`: Update summary tables.
   - `How-to`: Fix procedures using the updated API.
   - `Changelog`: Record the changes.
4. **Verify Cross-references**: Check for broken links.

## Tutorial Template

````markdown
# [Title]

In this tutorial, you will experience the process of [Goal].

## Step 1 — [Action]

```python
# Code example
```

**Expected Output:**

> The output should look like this
````

## How-to Guide Template

````markdown
# How to [Task]

Ensure that [Prerequisites] are completed before starting.

## 1. [Step Name]

```python
# Procedure steps
```

::: tip
[Helpful hints or warnings]
:::
````

## Final Checklist (DSS Checklist)

- [ ] Is the Diátaxis type (Tutorial, How-to, Reference, Explanation) clearly identified for every page?
- [ ] Are tutorials free of long-winded explanations?
- [ ] Do all code samples have language tags (`` ```python ``) and are they runnable?
- [ ] Have auto-generated Sphinx files been kept free of manual edits?
- [ ] Does the VitePress build (`npm run docs:build`) complete without warnings?