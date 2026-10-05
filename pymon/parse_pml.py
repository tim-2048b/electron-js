"""
PML Parser - Basic example for parsing Process Monitor log files
"""

from procmon_parser import ProcmonLogsReader
import argparse
from pathlib import Path


def parse_pml_file(pml_path: str) -> None:
    """Parse and display basic information from a PML file."""
    pml_file = Path(pml_path)

    if not pml_file.exists():
        print(f"Error: File not found: {pml_path}")
        return

    try:
        print(f"Parsing PML file: {pml_file.name}")
        print("-" * 60)

        with open(pml_path, 'rb') as f:
            reader = ProcmonLogsReader(f)
            events = list(reader.events())

        print(f"Total events: {len(events)}")
        print("\nFirst 10 events:")
        print("-" * 60)

        for i, event in enumerate(events[:10], 1):
            print(f"\nEvent {i}:")
            print(f"  Time: {event.time}")
            print(f"  Process: {event.process_name} (PID: {event.process_id})")
            print(f"  Operation: {event.operation}")
            print(f"  Path: {event.path}")
            print(f"  Result: {event.result}")
            if event.detail:
                print(f"  Detail: {event.detail}")

    except Exception as e:
        print(f"Error parsing PML file: {e}")


def filter_events(pml_path: str, process_name: str = None, operation: str = None) -> None:
    """Filter events by process name or operation."""
    try:
        with open(pml_path, 'rb') as f:
            reader = ProcmonLogsReader(f)
            events = list(reader.events())

        filtered = events

        if process_name:
            filtered = [e for e in filtered if process_name.lower() in e.process_name.lower()]
            print(f"Filtered by process: {process_name} ({len(filtered)} events)")

        if operation:
            filtered = [e for e in filtered if operation.lower() in e.operation.lower()]
            print(f"Filtered by operation: {operation} ({len(filtered)} events)")

        print("\nFiltered events:")
        print("-" * 60)
        for event in filtered[:20]:
            print(f"{event.time} | {event.process_name} | {event.operation} | {event.path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and analyze Process Monitor PML files")
    parser.add_argument("pml_file", help="Path to the PML file")
    parser.add_argument("--process", "-p", help="Filter by process name")
    parser.add_argument("--operation", "-o", help="Filter by operation type")

    args = parser.parse_args()

    if args.process or args.operation:
        filter_events(args.pml_file, args.process, args.operation)
    else:
        parse_pml_file(args.pml_file)
