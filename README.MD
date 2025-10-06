# JSON to MySQL Importer

A Python-based GUI application for SQL engineers to efficiently import JSON files into MySQL databases. This tool provides an intuitive interface for bulk importing JSON data with automatic schema inference, transaction safety, and progress tracking.

## 🎯 Purpose

This is an internal data conversion tool designed for importing pre-formatted JSON files into MySQL conversion servers. It automatically creates table structures based on JSON content and handles bulk imports with transaction safety.

## ✨ Features

- **User-Friendly GUI** - No command line knowledge required
- **Connection Testing** - Verify database credentials before importing
- **Automatic Schema Inference** - Tables are created automatically from JSON structure
- **Transaction Safety** - Each file import is atomic (all-or-nothing)
- **Progress Tracking** - Real-time progress bar and detailed status logging
- **Import Summary** - Clear reporting of successful and failed imports
- **Smart Data Type Mapping** - Automatically determines appropriate MySQL column types
- **Configuration Persistence** - Saves host and port settings between sessions
- **Auto-increment Primary Keys** - All tables get an `id` column automatically
- **Network Drive Support** - Works seamlessly with UNC paths and mapped drives

## 📋 Prerequisites

### For Running the Python Script
- Python 3.6 or higher
- MySQL Server access
- Required Python packages (see Installation section)

### For Running the Executable
- Windows operating system
- MySQL Server access
- No Python installation required

## 🚀 Installation

### Option 1: Running from Source (Recommended for Developers)

1. **Ensure Python is installed**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation by opening Command Prompt and typing: `python --version`

2. **Install required packages**
   ```bash
   pip install mysql-connector-python
   ```

3. **Download the script**
   - Save `JSONtoMySQL.py` to a folder on your computer

4. **Run the application**
   ```bash
   python JSONtoMySQL.py
   ```

### Option 2: Running the Executable (Easiest for End Users)

1. **Download** `JSONtoMySQL.exe` from the deployment folder
2. **Double-click** the executable to run
3. No Python installation needed!

> **Note:** The executable is larger (~50-100MB) but more convenient for users who don't have Python installed.

## 📖 Usage Guide

### Step 1: Launch the Application
- Double-click `JSONtoMySQL.exe` OR
- Run `python JSONtoMySQL.py` from command line

### Step 2: Enter Database Connection Details
1. **Host**: MySQL server hostname (default: db-gov-central.mgmt.cms.caseloadpro.com)
2. **Port**: MySQL port (default: 3306)
3. **Username**: Your MySQL username
4. **Password**: Your MySQL password
5. **Database**: Target database name

> The host and port will be saved for next time. Username, password, and database are never saved for security.

### Step 3: Test Connection
- Click **"Test Connection"** button
- Wait for confirmation message
- The import button will remain disabled until connection succeeds

### Step 4: Select JSON Files Directory
- Click **"Browse..."** button
- Navigate to the folder containing your JSON files
- This can be a local folder or network drive (UNC path like `\\server\share\folder`)

### Step 5: Execute Import
- Click **"Execute Import"** (enabled only after successful connection test and directory selection)
- Monitor progress in the progress bar and status window
- Review the import summary when complete

## 📁 JSON File Requirements

### File Format
- Files must have `.json` extension
- Each file should contain either:
  - A single JSON object: `{"key": "value", ...}`
  - An array of objects: `[{"key": "value"}, ...]`
- Empty files or empty arrays will be skipped with a warning

### Naming Convention
- **IMPORTANT**: The filename (without .json extension) becomes the table name
- Example: `customers.json` creates a table named `customers`
- Use valid MySQL table names (alphanumeric and underscores)

### Example JSON Structures

**Single Object** (creates 1-row table):
```json
{
    "customer_id": 1001,
    "name": "John Doe",
    "email": "john@example.com",
    "active": true
}
```

**Array of Objects** (creates multi-row table):
```json
[
    {
        "customer_id": 1001,
        "name": "John Doe",
        "active": true
    },
    {
        "customer_id": 1002,
        "name": "Jane Smith",
        "active": false
    }
]
```

**Mixed Fields** (tool handles varying fields across records):
```json
[
    {
        "id": 1,
        "name": "Product A",
        "price": 99.99
    },
    {
        "id": 2,
        "name": "Product B",
        "price": 149.99,
        "discount": 10
    }
]
```
The table will include all fields (id, name, price, discount) with NULL for missing values.

## 🔧 How It Works

### Table Creation Process

1. **Schema Analysis**: Scans ALL records in the JSON file to find every unique field
2. **Type Inference**: Determines the best MySQL data type for each field
3. **Table Creation**: 
   - **DROPS existing table if it exists** (this is intentional for conversion workflows)
   - Creates new table with inferred schema
   - Adds auto-increment `id` column as primary key

### Data Type Mapping

The tool intelligently maps JSON data types to MySQL types:

| JSON Type | MySQL Type | Condition |
|-----------|-----------|-----------|
| Nested object/array | JSON | For complex structures |
| String | TEXT | If length > 255 characters |
| String | VARCHAR(255) | If length ≤ 255 characters |
| Decimal number | DOUBLE | For any floating-point number |
| Large integer | BIGINT | If ≥ 2,147,483,648 |
| Integer | INT | If < 2,147,483,648 |
| Boolean | BOOLEAN | For true/false values |
| null | TEXT | Default for unknown types |

### Transaction Safety

Each JSON file import is wrapped in a database transaction:
- If import succeeds: Changes are committed
- If any error occurs: All changes are rolled back
- Guarantees: Each table is either fully imported or not created at all

## ⚠️ Important Behaviors

### Destructive Operations
**WARNING**: This tool **DROPS AND RECREATES** tables with matching names.

- Existing table named `customers`? It will be DROPPED
- This is intentional for data conversion workflows
- Always verify you're pointing to the correct conversion database
- Consider backing up important data before bulk imports

### Table Structure
Every created table includes:
- **id column**: BIGINT AUTO_INCREMENT PRIMARY KEY (always first column)
- **Data columns**: Derived from JSON fields in alphabetical order

### Error Handling
- Invalid JSON files are skipped (not imported)
- Empty files are skipped (not imported)
- Each file import is independent (one failure doesn't stop others)
- Detailed error messages appear in the status window

## 📊 Import Summary

After import completes, you'll see a summary showing:
- Total files processed
- Successfully imported files
- Failed imports (with filenames)
- Detailed log of all operations

Example:
```
============================================================
IMPORT SUMMARY
============================================================
Total files processed: 25
Successfully imported: 23
Failed imports: 2

Failed files:
  - corrupted_data.json
  - invalid_format.json
============================================================
```

## 🛠️ Troubleshooting

### "Connection Failed" Error
- Verify hostname and port are correct
- Check username and password
- Ensure database exists on the server
- Verify network connectivity to MySQL server
- Check firewall rules allow MySQL port (default 3306)

### "No JSON Files Found"
- Verify directory path is correct
- Ensure files have `.json` extension (not `.txt`)
- Check folder permissions

### "Invalid JSON Format" Errors
- Validate JSON syntax using online tools (jsonlint.com)
- Check for proper encoding (UTF-8)
- Look for special characters or encoding issues

### Import Button Disabled
- Must click "Test Connection" and receive success message first
- Must select a directory containing JSON files
- Both conditions must be met before import button enables

### Slow Performance
- Large JSON files take longer to process
- Network drives may be slower than local drives
- Progress bar shows current status
- Check MySQL server load and connection speed

## 🔐 Security Notes

- **Passwords are never saved** - entered fresh each session
- Only host and port are persisted in `importer_config.json`
- Connection credentials are validated before any operations
- All queries use parameterized statements (SQL injection safe)
- Recommended: Use read/write accounts, not root accounts

## 💾 Configuration File

The tool saves connection preferences in `importer_config.json` (same folder as executable/script):

```json
{
    "host": "db-gov-central.mgmt.cms.caseloadpro.com",
    "port": "3306"
}
```

You can manually edit this file if needed. The tool will create it automatically after the first successful connection test.

## 🐛 Known Limitations

- Table names must be valid MySQL identifiers
- Extremely large JSON files (>1GB) may cause memory issues
- Nested JSON structures are stored as JSON type (requires MySQL 5.7.8+)
- All tables are dropped and recreated (no append mode)
- Column names are case-sensitive based on JSON keys

## 📚 Best Practices

1. **Test First**: Always test with a small sample before bulk importing
2. **Verify Database**: Double-check you're connected to the correct conversion database
3. **Backup**: Consider backing up the target database before large imports
4. **Monitor**: Watch the status window for errors during import
5. **Network Paths**: When using UNC paths, ensure you have proper network permissions
6. **File Organization**: Keep JSON files organized in dedicated folders
7. **Naming**: Use clear, descriptive filenames as they become table names

## 🔄 Typical Workflow

1. Receive JSON files from data source
2. Place files in accessible directory (local or network drive)
3. Launch importer tool
4. Enter connection credentials
5. Test connection (verify correct database)
6. Select JSON directory
7. Review file count in status window
8. Execute import
9. Monitor progress bar
10. Review summary for any failures
11. Verify imported data in MySQL

## 🤝 Support

For issues or questions:
- Check this README first
- Review error messages in the status window
- Verify JSON file formats
- Contact your database administrator team

## 📝 Technical Details

### Technology Stack
- **Language**: Python 3.6+
- **GUI Framework**: tkinter (built into Python)
- **Database Driver**: mysql-connector-python
- **Threading**: For non-blocking UI operations

### Performance Characteristics
- Connection pooling: Not used (single connection)
- Transaction mode: Explicit commit/rollback per file
- Batch inserts: Uses `executemany()` for efficiency
- Memory usage: Loads entire JSON file into memory (consider for very large files)

### Development Notes
- The tool uses explicit transaction control (`autocommit=False`)
- Each file import is atomic (fully succeeds or fully fails)
- Type inference scans all records to accommodate varying field types
- Progress updates occur after each file completes

## 📜 Version History

### Version 2.0 (Current)
- Added connection testing with "Test Connection" button
- Improved transaction safety (explicit commit/rollback)
- Added progress bar for import operations
- Enhanced import summary with success/failure tracking
- Simplified connection management (removed pooling)
- Added configuration persistence for host/port
- Better type inference with extracted method
- Comprehensive error handling and logging
- Import button logic (disabled until prerequisites met)

### Version 1.0
- Initial release
- Basic JSON to MySQL import functionality
- GUI interface with tkinter
- Automatic schema inference

---

**Made for SQL Engineers by SQL Engineers** 🚀