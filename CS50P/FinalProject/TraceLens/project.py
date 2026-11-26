import csv
from datetime import datetime
import ipaddress
import argparse
import json
from pathlib import Path


DEFAULT_THRESHOLD = 5
DEFAULT_WINDOW_MINUTES = 10

VALID_EVENT_TYPES = {
    "LOGIN_SUCCESS",
    "LOGIN_FAILED",
}

REQUIRED_FIELDS = (
    "timestamp",
    "source_ip",
    "username",
    "event_type",
)

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def main():
    """Runs the TraceLens"""
    parser = argparse.ArgumentParser(
        description="TraceLens - Local Security Analyzer"
    )

    parser.add_argument(
        "--input", 
        required=True,
        help = "Path to the CSV log file to analyze"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help = f"Failed login attempts required for an alert (default: {DEFAULT_THRESHOLD})"
    )

    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_WINDOW_MINUTES,
        help  = f"Detection window in minutes (default: {DEFAULT_WINDOW_MINUTES})"
    )

    parser.add_argument(
        "--output",
        help = "Optional path to save the JSON report"
    )

    args = parser.parse_args()

    if(args.threshold < 1 or args.window < 1):
        parser.error("--threshold and --window must be positive integer")

    try:
        logs = load_logs(args.input)
    except OSError as error:
        parser.error(f"Unable to read input file: {error}")

    alerts = detect_repeated_failures(logs, args.threshold, args.window)

    report = generate_report(logs, alerts)

    print_report(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w") as file:
            json.dump(report, file, indent=4, default=str)

        print(f"\nJSON report saved to: {output_path}")


def load_logs(file_path):
    """Open Logs from a CSV file and return it as a list of dictionaries."""
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        logs = list(reader)
        return logs


def parse_timestamp(timestamp):
    """Parse a timestamp into a datetime object"""
    try:
        return datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    except (ValueError, TypeError):
        return None


def validate_event(event):
    """Checks wheather a log contain valid data or not"""

    for field in REQUIRED_FIELDS:
        if (not event.get(field) or not event[field].strip()):
            return False
        
    if(parse_timestamp(event["timestamp"]) is None):
        return False

    try:
        ipaddress.ip_address(event["source_ip"])
    except ValueError:
        return False

    if (event["event_type"] not in VALID_EVENT_TYPES):
        return False

    return True


def detect_repeated_failures(logs, threshold = DEFAULT_THRESHOLD, window_minutes = DEFAULT_WINDOW_MINUTES):
    """Detect repeated failures 5 in a row within a 10 minutes window from the same IP & same user
    and check for subsequent logins
    """

    valid_logs = [
        event for event in logs if validate_event(event)
    ]

    successful_logs = {}

    grouped_logs = {}

    for event in valid_logs:
        key = (event["source_ip"], event["username"])

        if event["event_type"] == "LOGIN_SUCCESS":
            successful_logs.setdefault(key, []).append(event)

        elif event["event_type"] == "LOGIN_FAILED":
            grouped_logs.setdefault(key, []).append(event)


    alerts = []

    for (source_ip, username), events in grouped_logs.items():

        events.sort(key = lambda event: parse_timestamp(event["timestamp"]))

        start = 0

        while (start < len(events)):

            window_start = parse_timestamp(events[start]["timestamp"])
            window_end = window_start
            count = 0
            end = start

            for current in range(start, len(events)):
                current_time = parse_timestamp(events[current]["timestamp"])

                elapsed = (current_time - window_start).total_seconds()

                if elapsed > window_minutes * 60:
                    break

                count += 1
                window_end = current_time
                end = current

            if count >= threshold:
                subsequent_successes = [
                    parse_timestamp(event["timestamp"])
                    for event in successful_logs.get(
                        (source_ip, username), []
                    )
                    if parse_timestamp(event["timestamp"]) > window_end
                ]

                successful_login_time = (
                    min(subsequent_successes)
                    if subsequent_successes
                    else None
                )

                alerts.append({
                    "source_ip": source_ip,
                    "username": username,
                    "failed_attempts": count,
                    "window_start": window_start,
                    "window_end": window_end,
                    "alert_type": "REPEATED_LOGIN_FAILURES",
                    "successful_login_after_failures": (
                        successful_login_time is not None
                    ),
                    "successful_login_time": successful_login_time
                })

                start = end + 1

            else:
                start += 1

    return alerts


def generate_report(logs, alerts):
    """Generate a structured security report from logs and alerts"""

    valid_logs = [
        event for event in logs if validate_event(event)
    ]

    invalid_count = len(logs) - len(valid_logs)

    successful_logins = sum(
        1 for event in valid_logs if event["event_type"] == "LOGIN_SUCCESS"
    )

    failed_logins = sum(
        1 for event in valid_logs if event["event_type"] == "LOGIN_FAILED"
    )

    report = {
        "summary": {
            "total_events": len(logs),
            "valid_events": len(valid_logs),
            "invalid_events": invalid_count,
            "successful_logins": successful_logins,
            "failed_logins": failed_logins,
            "total_alerts": len(alerts) 
        },
        "alerts": alerts
    }

    return report


def print_report(report):
    """Print the report in the terminal"""
    summary = report["summary"]

    print("\n========== TRACELENS SECURITY REPORT ==========")
    print("\nSummary")
    print(f"Total events:       {summary["total_events"]}")
    print(f"Valid events:       {summary["valid_events"]}")
    print(f"Invalid events:     {summary["invalid_events"]}")
    print(f"Successful logins:  {summary["successful_logins"]}")
    print(f"Failed logins:      {summary["failed_logins"]}")
    print(f"Total alerts:       {summary["total_alerts"]}")

    print("\nSECURITY ALERTS")

    if not report["alerts"]:
        print("No suspicious activity detected.")
    else:
        for number, alert in enumerate(report["alerts"], start=1):
            print(f"\nAlert #{number}")
            print(f"Type:       {alert["alert_type"]}")
            print(f"Source IP:  {alert["source_ip"]}")
            print(f"Username:   {alert["username"]}")
            print(f"Failures:   {alert["failed_attempts"]}")
            print(f"Window:     {alert["window_start"]} to {alert["window_end"]}")

            print("Successful login afterward: ", alert["successful_login_after_failures"])

            if alert["successful_login_time"]:
                print(f"Successful login time: {alert['successful_login_time']}")

    print("\n===============================================")


if __name__ == "__main__":
    main()