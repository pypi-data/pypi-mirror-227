import argparse
import sys

from junit_xml import TestSuite, TestCase, to_xml_report_string  # type: ignore

from kicad2junit.erc import ErcReport
from kicad2junit.pro import KicadProject  # type: ignore

parser = argparse.ArgumentParser(description="Convert KiCad ERC report to JUnit")
parser.add_argument(
    "input",
    nargs="?",
    type=argparse.FileType("r"),
    default=sys.stdin,
    help="JSON ERC report",
)
parser.add_argument(
    "output",
    nargs="?",
    type=argparse.FileType("w"),
    default=sys.stdout,
    help="JUnit XML output",
)
parser.add_argument(
    "--project",
    nargs="?",
    type=argparse.FileType("r"),
    help="Kicad project file",
)
parser.add_argument("--project-dir", default="", help="Kicad project directory")
parser.add_argument(
    "--warn-error", action="store_true", help="Treat warnings as errors"
)


def run():
    args = parser.parse_args()
    json_report: str = args.input.read()  # type: ignore

    r: ErcReport = ErcReport.schema().loads(json_report)  # type: ignore

    num_errors = 0
    num_warnings = 0

    test_suites: list[TestSuite] = []
    rules = {}
    exclusions = {}
    if args.project is not None:
        project = KicadProject.from_json(args.project.read())
        rules = project.erc.rule_severities
        exclusions = project.erc.get_erc_exclusions()

    for sheet in r.sheets:
        test_cases: dict[str, TestCase] = {}

        for violation in sheet.violations:
            tc = test_cases.get(
                violation.type,
                TestCase(
                    violation.type,
                    allow_multiple_subelements=True,
                    file=args.project_dir + r.source,
                ),
            )
            output = (
                violation.description
                + "\n"
                + "\n".join([item.description for item in violation.items])
            )
            if violation.severity == "ignore":
                tc.add_skipped_info(violation.description, output)
            elif any(item.uuid in exclusions for item in violation.items):
                tc.add_skipped_info(
                    violation.description, f"Excluded {violation.severity}\n" + output
                )
            else:
                tc.add_failure_info(
                    violation.description, output, failure_type=violation.severity
                )

                # Count errors
                if violation.severity == "error":
                    num_errors += 1
                elif violation.severity == "warning":
                    num_warnings += 1

            test_cases[violation.type] = tc

        # Add passed/ignored test from project
        for violation_type, state in rules.items():
            if violation_type not in test_cases:
                tc = TestCase(
                    violation_type,
                    allow_multiple_subelements=True,
                    file=args.project_dir + r.source,
                )

                if state == "ignore":
                    tc.add_skipped_info("Ignored", "Ignored")

                test_cases[violation_type] = tc

        ts = TestSuite(
            sheet.path,
            list(test_cases.values()),
            timestamp=r.date,
            file=args.project_dir + r.source,
            properties={"uuid_path": sheet.uuid_path},
        )
        test_suites.append(ts)

    # pretty printing is on by default but can be disabled using prettyprint=False
    xml = to_xml_report_string(test_suites)
    args.output.write(xml)

    print(f"Finished with {num_errors} errors, {num_warnings} warnings")

    # Add warning count to errors if treated as such
    if args.warn_error:
        num_errors += num_warnings

    exit(1 if num_errors > 0 else None)
