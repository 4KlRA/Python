# TraceLens

TraceLens is a local-first security log analyzer built with Python. It analyzes CSV-based authentication logs to identify suspicious login activity, particularly repeated failed login attempts that may indicate brute-force attempts or unauthorized access.

The project was developed as a CS50P final project to apply Python programming concepts such as file handling, data validation, functions, exception handling, command-line interfaces, testing, and data processing.

## Features

- **CSV Log Processing:** Loads authentication logs from CSV files.
- **Data Validation:** Validates timestamps, IP addresses, required fields, and event types.
- **Repeated Failure Detection:** Detects multiple failed login attempts associated with the same IP address and username within a configurable time window.
- **Successful Login Context:** Identifies whether a successful login occurred after a detected sequence of failures.
- **Configurable Detection:** Allows users to customize the failure threshold and detection time window.
- **Security Reporting:** Generates summaries containing total events, valid and invalid events, successful and failed logins, and detected alerts.
- **JSON Export:** Exports reports to JSON files for further analysis.
- **Local Processing:** Analyzes files locally without external services or AI integrations.

## Installation

Requirements:

- Python 3.10 or later
- pip

Clone the repository and navigate to the TraceLens directory:

```bash
git clone https://github.com/4KlRA/Python.git
cd Python/CS50P/FinalProject/TraceLens
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run TraceLens using a CSV log file:

```bash
python project.py --input samples/sample_logs.csv
```

Customize the detection threshold and time window:

```bash
python project.py --input samples/sample_logs.csv --threshold 5 --window 10
```

Export the analysis report as JSON:

```bash
python project.py --input samples/sample_logs.csv --output reports/report.json
```

View available command-line options:

```bash
python project.py --help
```

## Detection Logic

TraceLens groups failed login events by source IP address and username. Events are sorted chronologically and evaluated within a configurable time window.

By default, five failed login attempts from the same IP address and username within ten minutes trigger an alert. The detection threshold and time window can be modified through command-line arguments.

The analyzer also checks for a subsequent successful login associated with the same IP address and username. This additional context may help prioritize suspicious activity for further investigation.

Alerts indicate potentially suspicious behavior and are not definitive evidence of an attack.

## Project Structure

- `project.py` – Main application, validation, detection, reporting, and CLI.
- `test_project.py` – Automated tests for core functions and CLI behavior.
- `samples/` – Sample and invalid CSV datasets.
- `reports/` – Directory for generated reports.
- `requirements.txt` – Project dependencies.
- `.gitignore` – Excludes generated files and unnecessary local artifacts.

## Limitations

TraceLens is a lightweight educational security analysis tool. It is not a SIEM, antivirus, intrusion prevention system, or replacement for professional security monitoring.

It currently supports CSV authentication logs with a predefined schema and login event types. It does not monitor systems in real time, block users or IP addresses, investigate network traffic, or confirm whether an attack occurred. Detection depends on the quality and completeness of the input logs.

All analysis is performed locally. The tool is intended for defensive security analysis and educational use.