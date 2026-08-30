# PowerShell Bridge Documentation

The PowerShell process bridge allows you to execute PowerShell commands from your Electron renderer process through a utility process.

## Usage

From any renderer process, you can call PowerShell commands like this:

```typescript
// Execute a simple command
const result = await window.electronPowerShell.execute('Get-Date');
console.log(result);
// Output: { stdout: "Friday, August 29, 2026 3:15:42 PM", stderr: "", exitCode: 0 }

// Execute a command with output
const files = await window.electronPowerShell.execute('Get-ChildItem C:\\Users');
console.log(files.stdout);

// Error handling
try {
  const result = await window.electronPowerShell.execute('Get-Process NonExistent');
} catch (error) {
  console.error('PowerShell execution failed:', error.message);
}
```

## Response Structure

The `execute` function returns a `PowerShellResponse` object:

```typescript
interface PowerShellResponse {
  stdout: string;      // Command output
  stderr: string;      // Error output
  exitCode: number;    // Exit code (0 = success)
}
```

## Architecture

- **Main Process** (`main.ts`): Manages the utility process and IPC handlers
- **Utility Process** (`powershell-utility.ts`): Spawns and communicates with PowerShell
- **Preload Script** (`preload.ts`): Exposes the API to the renderer process
- **Type Definitions** (`types.d.ts`): TypeScript type definitions for the API

## Features

- Asynchronous PowerShell command execution
- 30-second timeout per command
- Automatic process recovery if terminated
- Type-safe API with TypeScript support
- Isolated utility process for safe execution

## Example

```typescript
async function runPowerShellCommand() {
  try {
    const result = await window.electronPowerShell.execute(
      'Get-Service | Select-Object -First 5'
    );
    
    if (result.exitCode === 0) {
      console.log('Services:', result.stdout);
    } else {
      console.error('Command failed:', result.stderr);
    }
  } catch (error) {
    console.error('Execution error:', error);
  }
}
```
