# 🐞 Bug Hunter

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)

A **straightforward, no-nonsense Python CLI tool** that scans your codebase for *real, common Python bugs* and reports them clearly.

Bug Hunter doesn’t try to be clever. It doesn’t do magic. It just **hunts bugs**.

---

## ✨ Features

* 🔍 Scan Python files for common bug patterns
* 🧩 Modular rule-based architecture (easy to extend)
* 🚫 Supports ignore patterns via `.bughunterignore`
* 📦 Clean CLI interface
* 🧪 Fully tested with `pytest`

Currently implemented rules:

* **Mutable default arguments**
* **Bare `except:` blocks**

---

## 📦 Installation

### Option A: Install locally (recommended for development)

Clone the repository and install:

```bash
git clone https://github.com/duttapratim515/bug-hunter.git
cd bug-hunter
pip install .
```

### Option B: Editable install (for hacking on rules)

```bash
pip install -e .
```

> It’s recommended to use a virtual environment.

Clone the repository and install locally:

```bash
git clone https://github.com/duttapratim515/bug-hunter.git
cd bug-hunter
pip install .
```

> It’s recommended to use a virtual environment.

---

## 🚀 Usage

Bug Hunter is a **CLI-first tool**.

```bash
bug-hunter scan <path>
```

Run Bug Hunter from the command line:

```bash
bug-hunter scan <path>
```

Example:

```bash
bug-hunter scan .
```

Sample output:

```text
[BUG-001] HIGH   | test_bug.py:1  Mutable default argument detected
[BUG-002] MEDIUM | test_bug.py:4  Bare except detected
```

---

## 🚫 Ignoring Files

You can exclude files or directories using a `.bughunterignore` file.

Example:

```text
venv/
build/
experimental/
```

Patterns are matched relative to the project root.

---

## 🧠 Architecture Overview

```text
bug_hunter/
├── cli.py        # Command-line interface
├── scanner.py    # File scanning logic
├── models.py     # Bug / result models
├── utils.py      # Helpers & utilities
└── rules/        # Individual bug rules
    ├── base.py
    ├── bare_except.py
    └── mutable_default.py
```

Each rule:

* Implements a base rule interface
* Analyzes AST nodes
* Emits structured bug reports

---

## 🧪 Testing

Run the test suite with:

```bash
pytest
```

All rules and scanner behavior are covered by tests.

---

## 🛣️ Roadmap

Planned improvements:

* JSON output mode
* Recursive directory scanning options
* Additional bug rules
* Performance optimizations

---

## 📜 License

MIT License.

You are free to use, modify, and distribute this software.

MIT License.

---

## 👤 Author

Built by **Pratim Dutta** (`duttapratim515`).

This project was created as a learning exercise and a practical static analysis tool.

Built by **Pratim Dutta**.

This project was created as a learning exercise and a practical static analysis tool.

---

If you like tools that are **simple, honest, and effective**, Bug Hunter is for you.
