# Legacy DBF Data Toolkit

A small Python proof-of-concept for inspecting, validating, exporting, and incrementally modernizing legacy DBF data.

The goal is to demonstrate a practical modernization path for systems that still depend on Visual FoxPro / DBF storage without changing an existing production application.

## Features

- Read DBF tables
- Inspect schema and field metadata
- Validate required fields and simple business rules
- Export records to CSV or JSON
- Migrate DBF records into SQLite for modernization experiments
- Produce validation summaries
- Structured logging
- Configuration-driven validation rules
- Unit tests for core validation and migration logic

## Why this project

Legacy FoxPro applications often contain valuable business logic but can be difficult to integrate with modern services. This toolkit shows how DBF data can be inspected and validated independently, then moved into a relational database as a low-risk modernization step.

The SQLite migration helper is intentionally lightweight. It demonstrates how legacy DBF data can be copied into a modern relational format without requiring a full rewrite of the source application.

## Quick start

```bash
python -m venv .venv
pip install -r requirements.txt
```

Inspect a DBF schema:

```bash
python -m legacy_dbf_toolkit.cli inspect path/to/customers.dbf
```

Validate records:

```bash
python -m legacy_dbf_toolkit.cli validate path/to/customers.dbf --config config/example_rules.json
```

Export to CSV:

```bash
python -m legacy_dbf_toolkit.cli export path/to/customers.dbf --format csv --output output/customers.csv
```

Migrate a DBF table to SQLite:

```bash
python -m legacy_dbf_toolkit.cli migrate-sqlite path/to/customers.dbf --database output/legacy.db --table customers
```

## Modernization direction

A practical staged path could be:

1. Inspect and validate legacy DBF data.
2. Export or migrate selected tables into a relational store.
3. Compare migrated records against the legacy source.
4. Expose approved data through a small service/API.
5. Move business rules incrementally rather than rewriting the full system at once.

See `docs/modernization-notes.md` for more detail.

## Privacy

This repository is a standalone proof-of-concept and does not contain proprietary source code, production data, credentials, or employer-confidential information.
