import argparse
import sys

from junit_xml import TestSuite, TestCase, to_xml_report_string  # type: ignore

from kicad2junit.erc import ErcReport  # type: ignore

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


def run():
    args = parser.parse_args()
    json_report: str = args.input.read()  # type: ignore

    r: ErcReport = ErcReport.schema().loads(json_report)  # type: ignore

    test_suites: list[TestSuite] = []
    for sheet in r.sheets:
        test_cases: dict[str, TestCase] = {}
        for violation in sheet.violations:
            tc = test_cases.get(
                violation.type,
                TestCase(violation.type, allow_multiple_subelements=True),
            )
            output = "\n".join([item.description for item in violation.items])
            if violation.severity == "ignore":
                tc.add_skipped_info(violation.description, output)
            elif violation.severity == "error":
                tc.add_error_info(violation.description, output)
            else:
                tc.add_failure_info(
                    violation.description, output, failure_type=violation.severity
                )
            test_cases[violation.type] = tc

        ts = TestSuite(
            sheet.path,
            list(test_cases.values()),
            timestamp=r.date,
            file=r.source,
            properties={"uuid_path": sheet.uuid_path},
        )
        test_suites.append(ts)

    # pretty printing is on by default but can be disabled using prettyprint=False
    xml = to_xml_report_string(test_suites)
    args.output.write(xml)
