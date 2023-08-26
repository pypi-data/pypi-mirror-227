import argparse
import sys

from junit_xml import TestSuite, TestCase, to_xml_report_string  # type: ignore

from kicad2junit.drc import DrcReport
from kicad2junit.pro import KicadProject  # type: ignore

parser = argparse.ArgumentParser(description="Convert KiCad DRC report to JUnit")
parser.add_argument(
    "input",
    nargs="?",
    type=argparse.FileType("r"),
    default=sys.stdin,
    help="JSON DRC report",
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


def run():
    args = parser.parse_args()
    json_report: str = args.input.read()  # type: ignore

    r: DrcReport = DrcReport.schema().loads(json_report)  # type: ignore

    violations = [*r.violations, *r.unconnected_items, *r.schematic_parity]

    rules = {}
    if args.project is not None:
        rules = KicadProject.from_json(
            args.project.read()
        ).board.design_settings.rule_severities

    test_cases: dict[str, TestCase] = {}
    for violation in violations:
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
        else:
            tc.add_failure_info(
                violation.description, output, failure_type=violation.severity
            )
        test_cases[violation.type] = tc

    for violation_type, state in rules.items():
        if violation_type not in test_cases:
            tc = TestCase(
                violation_type,
                allow_multiple_subelements=True,
                file=args.project_dir + r.source,
            )

            if state == "ignore":
                tc.add_skipped_info("Ignored")

            test_cases[violation_type] = tc

    ts = TestSuite(
        "pcb",
        list(test_cases.values()),
        timestamp=r.date,
        file=args.project_dir + r.source,
    )

    # pretty printing is on by default but can be disabled using prettyprint=False
    xml = to_xml_report_string([ts])
    args.output.write(xml)
