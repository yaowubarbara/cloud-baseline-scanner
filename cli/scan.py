### —— 调用 ScoutSuite 进行基线扫描

#!/usr/bin/env python3
"""
扫描 AWS 账户并输出 HTML & JSON 报告到 ./reports/
"""
import json, subprocess, datetime, pathlib, shutil

REPORT_DIR = pathlib.Path(__file__).parent.parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)

timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
json_path = REPORT_DIR / f"scoutsuite-{timestamp}.json"
html_path = REPORT_DIR / f"report-{timestamp}.html"

print("[*] Running ScoutSuite ...")
subprocess.run(["scout", "--report-dir", str(REPORT_DIR), "aws"], check=True)

# ScoutSuite 报告默认叫 scoutsuite-results/scoutsuite-report.js
raw_json = next((REPORT_DIR / "scoutsuite-report" ).glob("scoutsuite-results-*.js"))
shutil.move(raw_json, json_path)

print("[*] Generating simple HTML summary ...")
findings = json.loads(json_path.read_text())

high_count = sum(1 for f in findings["findings"].values() if f["severity"] == "high")

html_path.write_text(f"""
<h2>Scan summary ({timestamp})</h2>
<ul>
  <li>High severity findings: <b>{high_count}</b></li>
  <li>Full JSON: <a href="{json_path.name}">{json_path.name}</a></li>
</ul>
""")
print(f"[+] Report written to {html_path}")
