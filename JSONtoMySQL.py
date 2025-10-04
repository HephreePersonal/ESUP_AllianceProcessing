
import mysql.connector
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import threading

class JSONtoMySQL:
    def __init__(self, host, user, password, database, status_callback=None):
        self.status_callback = status_callback
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            pool_name="mypool",
            pool_size=5,
            connect_timeout=10
        )
        self.cursor = self.connection.cursor()
        self.log("Database connection established")
    
    def log(self, message):
        """Send status messages to callback if provided"""
        if self.status_callback:
            self.status_callback(message)
        print(message)
    
    def infer_column_type(self, value):
        """Infer MySQL column type from Python value"""
        if isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, int):
            if abs(value) < 2147483648:
                return "INT"  # Use smaller int when possible
            return "BIGINT"
        elif isinstance(value, float):
            return "DOUBLE"  # More precise than DECIMAL for floating points
        elif isinstance(value, str):
            if len(value) <= 255:
                return "VARCHAR(255)"  # Optimize for smaller strings
            return "TEXT"
        elif value is None:
            return "TEXT"
        return "JSON"  # Handle nested structures
    
    def create_table_from_json(self, table_name, json_data):
        """Create table structure based on first JSON record"""
        if not json_data:
            self.log(f"No data in {table_name}.json - skipping")
            return False
        
        first_record = json_data[0]
        columns = []
        
        for key, value in first_record.items():
            col_type = self.infer_column_type(value)
            columns.append(f"`{key}` {col_type}")
        
        drop_sql = f"DROP TABLE IF EXISTS `{table_name}`"
        self.cursor.execute(drop_sql)
        self.log(f"Dropped table {table_name} if it existed")
        
        create_sql = f"CREATE TABLE `{table_name}` ({', '.join(columns)})"
        self.cursor.execute(create_sql)
        self.connection.commit()
        self.log(f"Created table {table_name}")
        return True
    
    def insert_json_data(self, table_name, json_data):
        """Insert JSON records into table"""
        if not json_data:
            return
        
        columns = list(json_data[0].keys())
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join([f'`{col}`' for col in columns])
        
        insert_sql = f"INSERT INTO `{table_name}` ({column_names}) VALUES ({placeholders})"
        
        values = []
        for record in json_data:
            values.append(tuple(record.get(col) for col in columns))
        
        self.cursor.executemany(insert_sql, values)
        self.connection.commit()
        self.log(f"Inserted {len(values)} records into {table_name}")
    
    def import_json_file(self, json_file_path):
        """Import a single JSON file to MySQL table"""
        table_name = Path(json_file_path).stem
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Handle empty files or empty arrays
            if not json_data or (isinstance(json_data, list) and len(json_data) == 0):
                self.log(f"Skipping {json_file_path} - File is empty or contains no data")
                return
            
            # Convert single object to list for consistency
            if isinstance(json_data, dict):
                json_data = [json_data]
            
            if self.create_table_from_json(table_name, json_data):
                self.insert_json_data(table_name, json_data)
            
            self.log(f"Successfully imported {json_file_path}")
        except json.JSONDecodeError:
            self.log(f"Skipping {json_file_path} - Invalid JSON format")
            return
    
    def import_directory(self, directory_path):
        """Import all JSON files from a directory"""
        json_files = list(Path(directory_path).glob('*.json'))
        
        if not json_files:
            self.log("No JSON files found in the selected directory")
            return
        
        self.log(f"\nFound {len(json_files)} JSON file(s) to import\n")
        
        for json_file in json_files:
            try:
                self.import_json_file(str(json_file))
            except Exception as e:
                self.log(f"ERROR importing {json_file}: {str(e)}")
        
        self.log("\n=== Import process completed ===")
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.connection.close()
        self.log("Database connection closed")
    
    # Add context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ImporterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON to MySQL Importer")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # Connection properties
        self.create_connection_frame()
        
        # Directory selection
        self.create_directory_frame()
        
        # Execute button
        self.create_execute_button()
        
        # Status window
        self.create_status_window()
    
    def create_connection_frame(self):
        """Create database connection input fields"""
        frame = tk.LabelFrame(self.root, text="Database Connection", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")
        
        # Host
        tk.Label(frame, text="Host:", width=10, anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.host_entry = tk.Entry(frame, width=40)
        self.host_entry.grid(row=0, column=1, pady=5)
        self.host_entry.insert(0, "db-gov-central.mgmt.cms.caseloadpro.com")
        
        # User
        tk.Label(frame, text="Username:", width=10, anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.user_entry = tk.Entry(frame, width=40)
        self.user_entry.grid(row=1, column=1, pady=5)
        
        # Password
        tk.Label(frame, text="Password:", width=10, anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        # Database
        tk.Label(frame, text="Database:", width=10, anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.database_entry = tk.Entry(frame, width=40)
        self.database_entry.grid(row=3, column=1, pady=5)
    
    def create_directory_frame(self):
        """Create directory selection"""
        frame = tk.LabelFrame(self.root, text="JSON Files Location", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")
        
        self.directory_var = tk.StringVar()
        
        tk.Entry(frame, textvariable=self.directory_var, width=50, state="readonly").pack(side="left", padx=5)
        tk.Button(frame, text="Browse...", command=self.browse_directory, width=10).pack(side="left")
    
    def create_execute_button(self):
        """Create execute button"""
        self.execute_btn = tk.Button(
            self.root, 
            text="Execute Import", 
            command=self.execute_import, 
            bg="#4CAF50", 
            fg="white",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.execute_btn.pack(padx=10, pady=10, fill="x")
    
    def create_status_window(self):
        """Create status output window"""
        frame = tk.LabelFrame(self.root, text="Status", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.status_text = scrolledtext.ScrolledText(frame, height=10, state="disabled", wrap="word")
        self.status_text.pack(fill="both", expand=True)
    
    def browse_directory(self):
        """Open directory browser dialog"""
        directory = filedialog.askdirectory(title="Select JSON Files Directory")
        if directory:
            self.directory_var.set(directory)
    
    def log_status(self, message):
        """Add message to status window"""
        self.status_text.config(state="normal")
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Validate all inputs before execution"""
        if not self.host_entry.get().strip():
            messagebox.showerror("Validation Error", "Host is required")
            return False
        
        if not self.user_entry.get().strip():
            messagebox.showerror("Validation Error", "Username is required")
            return False
        
        if not self.password_entry.get().strip():
            messagebox.showerror("Validation Error", "Password is required")
            return False
        
        if not self.database_entry.get().strip():
            messagebox.showerror("Validation Error", "Database name is required")
            return False
        
        if not self.directory_var.get().strip():
            messagebox.showerror("Validation Error", "JSON files directory is required")
            return False
        
        return True
    
    def execute_import(self):
        """Execute the import process"""
        if not self.validate_inputs():
            return
        
        # Disable execute button during import
        self.execute_btn.config(state="disabled")
        
        # Clear status window
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, "end")
        self.status_text.config(state="disabled")
        
        # Run import in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.run_import)
        thread.start()
    
    def run_import(self):
        """Run the import process"""
        try:
            self.log_status("Starting import process...\n")
            
            importer = JSONtoMySQL(
                host=self.host_entry.get().strip(),
                user=self.user_entry.get().strip(),
                password=self.password_entry.get().strip(),
                database=self.database_entry.get().strip(),
                status_callback=self.log_status
            )
            
            importer.import_directory(self.directory_var.get().strip())
            importer.close()
            
            messagebox.showinfo("Success", "Import completed successfully!")
            
        except mysql.connector.Error as err:
            error_msg = f"Database Error: {err}"
            self.log_status(f"\nERROR: {error_msg}")
            messagebox.showerror("Database Error", error_msg)
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_status(f"\nERROR: {error_msg}")
            messagebox.showerror("Error", error_msg)
        finally:
            # Re-enable execute button
            self.execute_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImporterGUI(root)
    root.mainloop()