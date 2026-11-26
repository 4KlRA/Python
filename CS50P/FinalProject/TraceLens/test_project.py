from project import main, load_logs
from project import parse_timestamp, validate_event
from project import detect_repeated_failures
from project import generate_report
import pytest
import json
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).parent
PROJECT_FILE = PROJECT_DIR / "project.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(PROJECT_FILE), *args],
        capture_output=True,
        text=True
    )


def test_main_is_callable():
    assert callable(main)


def test_load_logs(tmp_path):
    csv_file = tmp_path / "test_logs.csv"

    csv_file.write_text(
        "timestamp,source_ip,username,event_type\n"
        "2026-11-20 10:00:00,192.168.1.10,admin,LOGIN_FAILED\n",
        encoding="utf-8"
    )

    logs = load_logs(csv_file)

    assert len(logs) == 1
    assert logs[0]["source_ip"] == "192.168.1.10"
    assert logs[0]["username"] == "admin"
    assert logs[0]["event_type"] == "LOGIN_FAILED"


def test_parse_timestamp_valid():
    result = parse_timestamp("2026-11-20 10:00:00")

    assert result is not None
    assert result.year == 2026
    assert result.month == 11
    assert result.day == 20


def test_parse_timestamp_invalid():
    assert parse_timestamp("INVALID_TIMESTAMP") is None


def test_validate_event_valid():
    event = {
        "timestamp": "2026-11-20 10:00:00",
        "source_ip": "192.168.1.10",
        "username": "admin",
        "event_type": "LOGIN_FAILED"
    }

    assert validate_event(event) is True


def test_validate_event_invalid_ip():
    event = {
        "timestamp": "2026-11-20 10:00:00",
        "source_ip": "not-an-ip",
        "username": "admin",
        "event_type": "LOGIN_FAILED"
    }

    assert validate_event(event) is False


def test_validate_event_unknown_type():
    event = {
        "timestamp": "2026-11-20 10:00:00",
        "source_ip": "192.168.1.10",
        "username": "admin",
        "event_type": "UNKNOWN_EVENT"
    }

    assert validate_event(event) is False



def test_detect_repeated_failures():
    logs = []

    for minute in range(5):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.168.1.10"
    assert alerts[0]["username"] == "admin"
    assert alerts[0]["failed_attempts"] == 5


def test_no_alert_below_threshold():
    logs = []

    for minute in range(4):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    assert detect_repeated_failures(logs) == []


def test_no_alert_outside_time_window():
    logs = []

    timestamps = [
        "2026-11-20 10:00:00",
        "2026-11-20 10:03:00",
        "2026-11-20 10:06:00",
        "2026-11-20 10:09:00",
        "2026-11-20 10:12:00"
    ]

    for timestamp in timestamps:
        logs.append({
            "timestamp": timestamp,
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    assert detect_repeated_failures(logs) == []



def test_detect_multiple_source_ips():
    logs = []

    for ip in ["192.168.1.10", "192.168.1.20"]:
        for minute in range(5):
            logs.append({
                "timestamp": f"2026-11-20 10:0{minute}:00",
                "source_ip": ip,
                "username": "admin",
                "event_type": "LOGIN_FAILED"
            })

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 2
    assert {alert["source_ip"] for alert in alerts} == {
        "192.168.1.10",
        "192.168.1.20"
    }



def test_detect_multiple_usernames():
    logs = []

    for username in ["admin", "guest"]:
        for minute in range(3):
            logs.append({
                "timestamp": f"2026-11-20 10:0{minute}:00",
                "source_ip": "192.168.1.10",
                "username": username,
                "event_type": "LOGIN_FAILED"
            })

    assert detect_repeated_failures(logs) == []



def test_custom_detection_threshold():
    logs = []

    for minute in range(3):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    alerts = detect_repeated_failures(
        logs,
        threshold=3,
        window_minutes=5
    )

    assert len(alerts) == 1
    assert alerts[0]["failed_attempts"] == 3



def test_detection_at_exact_window_boundary():
    timestamps = [
        "2026-11-20 10:00:00",
        "2026-11-20 10:02:00",
        "2026-11-20 10:04:00",
        "2026-11-20 10:06:00",
        "2026-11-20 10:10:00"
    ]

    logs = [
        {
            "timestamp": timestamp,
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        }
        for timestamp in timestamps
    ]

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 1
    assert alerts[0]["failed_attempts"] == 5



def test_generate_report_summary():
    logs = [
        {
            "timestamp": "2026-11-20 10:00:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        },
        {
            "timestamp": "2026-11-20 10:01:00",
            "source_ip": "192.168.1.20",
            "username": "user1",
            "event_type": "LOGIN_SUCCESS"
        },
        {
            "timestamp": "INVALID_TIMESTAMP",
            "source_ip": "192.168.1.30",
            "username": "user2",
            "event_type": "LOGIN_FAILED"
        }
    ]

    alerts = []

    report = generate_report(logs, alerts)

    assert report["summary"]["total_events"] == 3
    assert report["summary"]["valid_events"] == 2
    assert report["summary"]["invalid_events"] == 1
    assert report["summary"]["successful_logins"] == 1
    assert report["summary"]["failed_logins"] == 1
    assert report["summary"]["total_alerts"] == 0


def test_generate_report_with_alerts():
    logs = [
        {
            "timestamp": "2026-11-20 10:00:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        }
    ]

    alerts = [
        {
            "source_ip": "192.168.1.10",
            "username": "admin",
            "failed_attempts": 5,
            "alert_type": "REPEATED_LOGIN_FAILURES"
        }
    ]

    report = generate_report(logs, alerts)

    assert report["summary"]["total_alerts"] == 1
    assert report["alerts"] == alerts



def test_successful_login_after_repeated_failures():
    logs = []

    for minute in range(5):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    logs.append({
        "timestamp": "2026-11-20 10:05:00",
        "source_ip": "192.168.1.10",
        "username": "admin",
        "event_type": "LOGIN_SUCCESS"
    })

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 1
    assert alerts[0]["successful_login_after_failures"] is True
    assert alerts[0]["successful_login_time"].minute == 5


def test_no_successful_login_after_repeated_failures():
    logs = []

    for minute in range(5):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 1
    assert alerts[0]["successful_login_after_failures"] is False
    assert alerts[0]["successful_login_time"] is None



def test_detect_multiple_separate_incidents():
    logs = []

    for minute in range(5):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    for minute in range(5):
        logs.append({
            "timestamp": f"2026-11-20 11:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 2


def test_no_duplicate_alerts_for_same_incident():
    logs = []

    for minute in range(7):
        logs.append({
            "timestamp": f"2026-11-20 10:0{minute}:00",
            "source_ip": "192.168.1.10",
            "username": "admin",
            "event_type": "LOGIN_FAILED"
        })

    alerts = detect_repeated_failures(logs)

    assert len(alerts) == 1



def test_cli_runs_successfully():
    result = run_cli(
        "--input", str(PROJECT_DIR / "samples" / "sample_logs.csv")
    )

    assert result.returncode == 0
    assert "TRACELENS SECURITY REPORT" in result.stdout
    assert "Total events:" in result.stdout


def test_cli_missing_file():
    result = run_cli(
        "--input", str(PROJECT_DIR / "samples" / "does_not_exist.csv")
    )

    assert result.returncode != 0
    assert "Unable to read input file" in result.stderr


def test_cli_invalid_threshold():
    result = run_cli(
        "--input", str(PROJECT_DIR / "samples" / "sample_logs.csv"),
        "--threshold", "0"
    )

    assert result.returncode != 0
    assert "must be positive" in result.stderr


def test_cli_generates_json_report(tmp_path):
    output_file = tmp_path / "nested" / "report.json"

    result = run_cli(
        "--input", str(PROJECT_DIR / "samples" / "sample_logs.csv"),
        "--output", str(output_file)
    )

    assert result.returncode == 0
    assert output_file.exists()

    report = json.loads(output_file.read_text(encoding="utf-8"))

    assert "summary" in report
    assert "alerts" in report
    assert report["summary"]["total_events"] > 0
