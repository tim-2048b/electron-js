# File Recorder - Drag & Drop Documentation

The file recorder feature allows users to drag and drop text files onto a designated drop zone in your Electron app. The system automatically records file paths and metadata.

## Features

- **Drag & Drop Support**: Users can drag text files directly onto the drop zone
- **File Path Recording**: Automatically captures and displays file paths
- **Visual Feedback**: Drop zone highlights on drag over
- **File Management**: Remove recorded files with a single click
- **Persistent Display**: Recorded files are displayed with timestamps
- **Type-Safe API**: Full TypeScript support

## Usage

### From the Renderer Process

```typescript
// The file recording is automatic when users drag files
// Access recorded files programmatically:
const files = await window.electronFileRecorder.getRecordedFiles();
console.log(files);

// Manually record a file:
await window.electronFileRecorder.recordFile({
  id: 'unique-id',
  path: 'C:\\Users\\path\\to\\file.txt',
  name: 'file.txt',
  timestamp: new Date().toLocaleString(),
});
```

## File Object Structure

```typescript
interface RecordedFile {
  id: string;              // Unique identifier
  path: string;            // Full file path
  name: string;            // File name only
  timestamp: string;       // When it was recorded
  size?: number;           // Optional: file size in bytes
}
```

## UI Behavior

1. **Normal State**: Shows "Drag & Drop Files Here" message
2. **Drag Over**: Drop zone highlights with blue background
3. **Drop**: File is recorded and added to the list
4. **Recorded List**: Shows:
   - File name (bold)
   - Full file path (monospace font)
   - Timestamp of when it was added
   - Remove button for each file

## Supported File Types

Currently configured to accept:
- `.txt` files (text/plain MIME type)
- Any file ending with `.txt`

To extend to other file types, modify the `drop` event handler in `renderer.ts`:

```typescript
if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
  addFile(file.path);
}
```

## IPC Handlers

### `file-recorder:record`

Records or updates a file in the main process.

```typescript
await window.electronFileRecorder.recordFile(file);
```

**Parameters**: `RecordedFile` object  
**Returns**: The recorded file object

### `file-recorder:get-files`

Retrieves all recorded files from the main process.

```typescript
const files = await window.electronFileRecorder.getRecordedFiles();
```

**Returns**: Array of `RecordedFile` objects

## Architecture

- **Renderer** (`renderer.ts`): Handles drag-and-drop UI and maintains local file state
- **Preload** (`preload.ts`): Exposes IPC bridge to renderer
- **Main** (`main.ts`): Manages persistent file storage via IPC handlers
- **Styles** (`index.css`): Drop zone and file list styling
- **Types** (`types.d.ts`): TypeScript interfaces for type safety

## Future Enhancements

You can extend this feature to include:

- File size tracking
- File modification dates
- File content preview
- Filtering and searching
- Export recorded files list
- Integration with PowerShell bridge to process files
- Persistence to disk (localStorage or database)
- File metadata extraction
