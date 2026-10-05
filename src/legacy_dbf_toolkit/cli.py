import argparse, json, logging
from .config import load_rules
from .exporter import export_csv, export_json
from .logging_utils import configure_logging
from .reader import inspect_schema, read_dbf
from .sqlite_migrator import migrate_dbf_to_sqlite
from .validation import validate_records

LOG = logging.getLogger(__name__)

def build_parser():
    parser = argparse.ArgumentParser(description="Legacy DBF inspection and export toolkit")
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("dbf")

    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("dbf")
    validate_cmd.add_argument("--config", required=True)

    export_cmd = sub.add_parser("export")
    export_cmd.add_argument("dbf")
    export_cmd.add_argument("--format", choices=["csv", "json"], required=True)
    export_cmd.add_argument("--output", required=True)

    migrate_cmd = sub.add_parser("migrate-sqlite")
    migrate_cmd.add_argument("dbf")
    migrate_cmd.add_argument("--database", required=True)
    migrate_cmd.add_argument("--table")

    return parser

def main():
    args = build_parser().parse_args()
    configure_logging(args.verbose)

    if args.command == "inspect":
        print(json.dumps([f.__dict__ for f in inspect_schema(args.dbf)], indent=2))
        return 0

    if args.command == "validate":
        rules = load_rules(args.config)
        records = read_dbf(args.dbf)
        issues = validate_records(records, rules.get("required_fields"), rules.get("max_lengths"))
        print(json.dumps([i.__dict__ for i in issues], indent=2))
        LOG.info("Validated %s records; found %s issues", len(records), len(issues))
        return 1 if issues else 0

    if args.command == "migrate-sqlite":
        migrated = migrate_dbf_to_sqlite(args.dbf, args.database, args.table)
        LOG.info("Migrated %s records to %s", migrated, args.database)
        return 0

    records = read_dbf(args.dbf)
    export_csv(records, args.output) if args.format == "csv" else export_json(records, args.output)
    LOG.info("Exported %s records", len(records))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
