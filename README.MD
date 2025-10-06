# JSONtoMySQL Importer

A Python-based GUI application that facilitates importing JSON files into MySQL databases. This tool provides an easy-to-use interface for bulk importing JSON data into MySQL tables with automatic schema inference.

## Features

- 🖼️ User-friendly graphical interface
- 📁 Bulk import of multiple JSON files
- 🔄 Automatic table schema inference
- 🏃‍♂️ Non-blocking imports with progress feedback
- 🔐 Secure database connection handling
- 📊 Smart data type mapping
- ⚡ Connection pooling support
- 🛡️ Error handling and validation
- 🆔 All tables have an auto-incrementing `id` primary key column

## Prerequisites

- Python 3.6 or higher
- MySQL Server
- Required Python packages:
  ```
  mysql-connector-python
  tkinter (usually comes with Python)
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```

2. Install required dependencies:
   ```bash
   pip install mysql-connector-python
   ```

## Usage

1. Run the application:
   ```bash
   python JSONtoMySQL.py
   ```

2. Fill in the database connection details:
   - Host (default: db-gov-central.mgmt.cms.caseloadpro.com)
   - Username
   - Password
   - Database name

3. Click "Browse..." to select a directory containing JSON files

4. Click "Execute Import" to start the import process

## JSON File Requirements

- Files must have `.json` extension
- Each file should contain either:
  - A single JSON object
  - An array of JSON objects
- Empty files will be skipped
- File name will be used as the table name

## Table Structure

- Every table created will have an `id` column of type `BIGINT AUTO_INCREMENT PRIMARY KEY` as the first column.
- All JSON fields are mapped to columns as described below.

## Data Type Mapping

| Python Type | MySQL Type    | Condition                |
|------------|---------------|--------------------------|
| bool       | BOOLEAN       |                         |
| int        | INT          | If < 2147483648         |
| int        | BIGINT       | If >= 2147483648        |
| float      | DOUBLE       |                         |
| str        | VARCHAR(255) | If length <= 255        |
| str        | TEXT         | If length > 255         |
| None       | TEXT         |                         |
| dict/list  | JSON         | For nested structures   |

## Technical Details

### Connection Management
- Uses MySQL connection pooling
- Pool size: 5 connections
- Connection timeout: 10 seconds
- Implements context manager pattern

### Error Handling
- Validates all input fields
- Handles database connection errors
- Manages JSON parsing errors
- Skips invalid or empty files
- Thread-safe operation

### Performance Features
- Multi-threaded operation
- Batch inserts for efficiency
- Connection pooling
- Non-blocking UI updates

## Example JSON Structure

```json
{
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "active": true,
    "scores": [85, 90, 95]
}
```

Or an array of objects:

```json
[
    {
        "id": 1,
        "name": "John Doe",
        "age": 30
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "age": 25
    }
]
```

## Error Messages

- "No JSON files found in the selected directory"
- "Skipping [filename] - File is empty or contains no data"
- "Skipping [filename] - Invalid JSON format"
- Various database connection error messages

## Best Practices

1. Backup your database before performing bulk imports
2. Test with small datasets first
3. Ensure sufficient database permissions
4. Monitor database resource usage during large imports
5. Verify data integrity after import

## Limitations

- Table names are derived from file names
- Existing tables with the same name will be dropped
- Every table will have an auto-incrementing `id` column as the primary key
- Maximum string length is 255 for VARCHAR fields
- Nested objects are stored as JSON strings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Specify your license here]

## Support

[Specify support contact or process]

## Acknowledgments

- Built with Python and mysql-connector-python
- Uses Tkinter for GUI implementation