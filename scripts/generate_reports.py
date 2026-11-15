"""Run pytest and write reproducible test/coverage reports to docs/reports."""
import datetime
import pathlib
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "reports"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable, "-m", "pytest", "-v",
        "--junitxml", str(OUT / "junit.xml"),
        "--html", str(OUT / "test-report.html"), "--self-contained-html",
        "--cov=app", "--cov-report", f"xml:{OUT / 'coverage.xml'}",
        "--cov-report", f"html:{OUT / 'coverage-html'}",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    output = result.stdout + result.stderr
    (OUT / "pytest-output.txt").write_text(output, encoding="utf-8")
    print(output)
    if not (OUT / "junit.xml").exists() or not (OUT / "coverage.xml").exists():
        return result.returncode or 1

    suite_root = ET.parse(OUT / "junit.xml").getroot()
    suite = suite_root if suite_root.tag == "testsuite" else suite_root.find("testsuite")
    if suite is None:
        raise RuntimeError("No pytest testsuite found in JUnit output")
    total = int(suite.get("tests", 0))
    failures = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
    skipped = int(suite.get("skipped", 0))
    passed = total - failures - skipped
    coverage = float(ET.parse(OUT / "coverage.xml").getroot().get("line-rate", 0)) * 100
    summary = [
        "# Test execution summary", "",
        f"- Date: {datetime.datetime.now():%Y-%m-%d %H:%M}",
        f"- Python: {platform.python_version()} ({platform.system()})",
        f"- Executed: {total}; passed: {passed}; failed/errors: {failures}; skipped: {skipped}",
        f"- Pass rate: {(100 * passed / total) if total else 0:.1f}%",
        f"- Backend app line coverage: {coverage:.1f}%",
        f"- Result: {'PASS' if result.returncode == 0 else 'FAIL'}", "",
    ]
    (OUT / "summary.md").write_text("\n".join(summary), encoding="utf-8")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
