"""
Advanced PML analysis utilities
"""

from procmon_parser import ProcmonLogsReader
from collections import Counter
import csv
from pathlib import Path


class PMLAnalyzer:
    """Analyze Process Monitor events from PML files."""

    def __init__(self, pml_path: str):
        self.pml_path = pml_path
        with open(pml_path, 'rb') as f:
            reader = ProcmonLogsReader(f)
            self.events = list(reader.events())

    def summary_stats(self) -> dict:
        """Get summary statistics."""
        processes = Counter(e.process_name for e in self.events)
        operations = Counter(e.operation for e in self.events)
        results = Counter(e.result for e in self.events)

        return {
            'total_events': len(self.events),
            'unique_processes': len(processes),
            'unique_operations': len(operations),
            'top_processes': processes.most_common(10),
            'top_operations': operations.most_common(10),
            'result_distribution': dict(results),
        }

    def get_events_by_process(self, process_name: str):
        """Get all events for a specific process."""
        return [e for e in self.events if process_name.lower() in e.process_name.lower()]

    def get_file_operations(self, path_filter: str = None):
        """Get file system operations."""
        file_ops = [e for e in self.events if e.operation in ('CreateFile', 'ReadFile', 'WriteFile', 'DeleteFile', 'QueryOpen', 'SetFileInformation')]

        if path_filter:
            file_ops = [e for e in file_ops if path_filter.lower() in (e.path or '').lower()]

        return file_ops

    def get_registry_operations(self):
        """Get registry operations."""
        return [e for e in self.events if 'Reg' in e.operation]

    def get_network_operations(self):
        """Get network operations."""
        return [e for e in self.events if any(op in e.operation for op in ['Send', 'Receive', 'Connect', 'TCP'])]

    def export_to_csv(self, output_path: str, events=None):
        """Export events to CSV file."""
        if events is None:
            events = self.events

        if not events:
            print("No events to export")
            return

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = ['time', 'process_name', 'process_id', 'operation', 'path', 'result', 'detail']

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(fieldnames)
                for event in events:
                    writer.writerow([
                        event.time,
                        event.process_name,
                        event.process_id,
                        event.operation,
                        event.path,
                        event.result,
                        event.detail or ''
                    ])

            print(f"Exported {len(events)} events to {output_path}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def print_summary(self):
        """Print summary statistics."""
        stats = self.summary_stats()

        print("=" * 70)
        print("PML FILE ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"Total Events: {stats['total_events']}")
        print(f"Unique Processes: {stats['unique_processes']}")
        print(f"Unique Operations: {stats['unique_operations']}")

        print("\nTop 10 Processes:")
        for proc, count in stats['top_processes']:
            print(f"  {proc}: {count}")

        print("\nTop 10 Operations:")
        for op, count in stats['top_operations']:
            print(f"  {op}: {count}")

        print("\nResult Distribution:")
        for result, count in stats['result_distribution'].items():
            print(f"  {result}: {count}")

        print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze_pml.py <pml_file> [--csv output.csv] [--process <name>]")
        sys.exit(1)

    pml_file = sys.argv[1]
    analyzer = PMLAnalyzer(pml_file)

    if "--csv" in sys.argv:
        idx = sys.argv.index("--csv")
        output_file = sys.argv[idx + 1]
        analyzer.export_to_csv(output_file)

    if "--process" in sys.argv:
        idx = sys.argv.index("--process")
        process_name = sys.argv[idx + 1]
        proc_events = analyzer.get_events_by_process(process_name)
        print(f"\nFound {len(proc_events)} events for {process_name}")
        if proc_events:
            analyzer.export_to_csv(f"output_{process_name}.csv", proc_events)
    else:
        analyzer.print_summary()
