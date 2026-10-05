# PML Parser Setup

Process Monitor Log (PML) file parser using `procmon-parser` for analyzing Windows Process Monitor captures.

## Setup

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Create virtual environment** (already done):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Parsing

Parse and display events from a PML file:
```bash
python parse_pml.py <pml_file>
```

### Filter Events

Filter by process name:
```bash
python parse_pml.py <pml_file> --process explorer
```

Filter by operation:
```bash
python parse_pml.py <pml_file> --operation CreateFile
```

### Advanced Analysis

Generate summary statistics:
```bash
python analyze_pml.py <pml_file>
```

Export to CSV:
```bash
python analyze_pml.py <pml_file> --csv output.csv
```

Filter and export specific process:
```bash
python analyze_pml.py <pml_file> --process notepad --csv notepad_events.csv
```

## File Operations Analysis

To analyze file operations, use the PMLAnalyzer class:

```python
from analyze_pml import PMLAnalyzer

analyzer = PMLAnalyzer("your_file.pml")
file_ops = analyzer.get_file_operations()
print(f"Found {len(file_ops)} file operations")
```

## Registry Operations

To analyze registry operations:

```python
from analyze_pml import PMLAnalyzer

analyzer = PMLAnalyzer("your_file.pml")
reg_ops = analyzer.get_registry_operations()
print(f"Found {len(reg_ops)} registry operations")
```

## Common Event Fields

- **Time**: Event timestamp
- **Process**: Process name and PID
- **Operation**: Operation type (CreateFile, ReadFile, RegOpenKey, etc.)
- **Path**: File system or registry path
- **Result**: Operation result (Success, Access Denied, etc.)
- **Detail**: Operation details

## Tips

1. Large PML files (>500MB) may take time to parse
2. Filter events early to reduce memory usage
3. Export to CSV for analysis in Excel or other tools
4. Use process filtering to focus on specific applications

## Troubleshooting

- **Memory issues**: Parse and filter in smaller chunks
- **Encoding issues**: Some paths may use special characters
- **Missing fields**: Not all events have all fields; use `.get()` method

## References

- [procmon-parser GitHub](https://github.com/eronnen/procmon-parser)
- [Process Monitor Documentation](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon)
