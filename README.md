# Legacy DBF Data Toolkit

A small Python proof-of-concept for inspecting, validating, and exporting legacy DBF data.

The goal is to demonstrate a practical modernization path for systems that still depend on Visual FoxPro / DBF storage without changing an existing production application.

## Features

- Read DBF tables
- Inspect schema and field metadata
- Validate required fields and simple business rules
- Export records to CSV or JSON
- Produce a validation summary
- Structured logging
- Configuration-driven validation rules
- Unit tests for core validation logic

## Why this project

Legacy FoxPro applications often contain valuable business logic but can be difficult to integrate with modern services. This toolkit shows how DBF data can be inspected and validated independently, creating a possible stepping stone toward APIs, reporting services, or staged migration.

## Privacy

This repository is a standalone proof-of-concept and does not contain proprietary source code, production data, credentials, or employer-confidential information.
