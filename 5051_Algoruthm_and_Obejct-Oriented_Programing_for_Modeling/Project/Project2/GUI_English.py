import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
    QFrame, QListWidget, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, 
    QDialog, QLabel, QLineEdit, QListWidgetItem, QComboBox
)
from PyQt5.QtCore import Qt
import numpy as np
from sort import QuickSort, MergeSort, CountingSort, HeapSort
from datetime import datetime
import re

### Sort Dialog Window ###
class SortDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("Sort Data")
        self.data_frames = data_frames
        self.selected_frame = None
        self.selected_column = None  
        self.sort_order = "ascending"
        self.selected_algorithm = "Default"
        self.current_df = None  

        # Create layout
        layout = QVBoxLayout()

        # Dropdown 1: Select sorting column
        column_layout = QHBoxLayout()
        column_layout.addWidget(QLabel("Sort Column:"))
        self.column_combo = QComboBox()
        # Fix 2: Bind current column change event
        self.column_combo.currentTextChanged.connect(self.on_column_changed)
        column_layout.addWidget(self.column_combo)
        layout.addLayout(column_layout)

        # Dropdown 2: Select ascending/descending order
        order_layout = QHBoxLayout()
        order_layout.addWidget(QLabel("Sort Order:"))
        self.order_combo = QComboBox()
        self.order_combo.addItems(["Ascending", "Descending"])
        order_layout.addWidget(self.order_combo)
        layout.addLayout(order_layout)

        # Dropdown 3: Select sorting algorithm
        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(QLabel("Sort Algorithm:"))
        self.algorithm_combo = QComboBox()
        # Add algorithm options (default + 4 custom algorithms)
        self.algorithm_combo.addItems([
            "Default (Pandas)", 
            "Quick Sort (QuickSort)", 
            "Merge Sort (MergeSort)", 
            "Heap Sort (HeapSort)", 
            "Counting Sort (CountingSort)"
        ])
        self.algorithm_combo.currentTextChanged.connect(self.on_algorithm_changed)  # Bind event
        algorithm_layout.addWidget(self.algorithm_combo)
        layout.addLayout(algorithm_layout)

        # Data type information label
        self.data_type_info = QLabel("No column selected")
        self.data_type_info.setWordWrap(True)
        self.data_type_info.setStyleSheet("color: #0066cc; font-weight: bold;")
        layout.addWidget(self.data_type_info)

        # Algorithm description label
        self.algorithm_info = QLabel()
        self.algorithm_info.setWordWrap(True)
        self.algorithm_info.setStyleSheet("color: #666; font-size: 9pt;")
        layout.addWidget(self.algorithm_info)

        # Button layout
        button_layout = QHBoxLayout()
        sort_button = QPushButton("Sort")
        sort_button.clicked.connect(self.perform_sort)
        button_layout.addWidget(sort_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize data
        self.update_data()

    def update_data(self):
        """Unified data and UI update"""
        selected_item = self.parent().narrow_widget.currentItem()
        if not selected_item:
            return
        
        self.selected_frame = selected_item.text()
        self.current_df = self.data_frames.get(self.selected_frame)
        
        if self.current_df is not None:
            # Save current column selection
            current_col = self.column_combo.currentText() if self.column_combo.count() > 0 else ""
            
            # Update column dropdown
            self.column_combo.clear()
            self.column_combo.addItems(self.current_df.columns.tolist())
            
            # Restore column selection (if exists)
            if current_col in self.current_df.columns:
                self.column_combo.setCurrentText(current_col)
                self.selected_column = current_col
            elif self.current_df.columns.tolist():
                self.selected_column = self.current_df.columns[0]
                self.column_combo.setCurrentText(self.selected_column)
            
            # Update data type information
            self.update_data_type_info()

    def on_column_changed(self, column_name):
        """Update state when column selection changes"""
        self.selected_column = column_name

    def on_algorithm_changed(self, algorithm_name):
        """Update description when algorithm selection changes"""
        self.selected_algorithm = algorithm_name

        # Fix 3: Save current column selection when algorithm switches
        saved_column = self.selected_column
        
        if self.current_df is not None:
            # Only filter non-integer columns when Counting Sort is selected
            if "Counting Sort (CountingSort)" in algorithm_name:
                numeric_cols = self.current_df.select_dtypes(include=['int', 'int64']).columns
                if len(numeric_cols) == 0:
                    QMessageBox.warning(self, "Warning", 
                        "No integer columns in current dataset, Counting Sort unavailable!")
                self.column_combo.clear()
                available_cols = numeric_cols.tolist()
                if not available_cols:  # Show all columns but disable counting sort when no integer columns
                    available_cols = self.current_df.columns.tolist()
                self.column_combo.addItems(available_cols)
                
                # Restore available column selection
                if saved_column in available_cols:
                    self.column_combo.setCurrentText(saved_column)
                    self.selected_column = saved_column
                elif available_cols:
                    self.selected_column = available_cols[0]
                    self.column_combo.setCurrentText(self.selected_column)
            else:
                self.column_combo.clear()
                self.column_combo.addItems(self.current_df.columns.tolist())
                
                # Restore column selection
                if saved_column in self.current_df.columns:
                    self.column_combo.setCurrentText(saved_column)
                    self.selected_column = saved_column
                elif self.current_df.columns.tolist():
                    self.selected_column = self.current_df.columns[0]
                    self.column_combo.setCurrentText(self.selected_column)
            
            # Update data type information
            self.update_data_type_info()

    def update_data_type_info(self):
        """Update data type information label"""
        if not self.selected_column or self.current_df is None:
            self.data_type_info.setText("No valid column selected")
            return
            
        col_data = self.current_df[self.selected_column]
        
        # ====== Smart data type detection ====== #
        data_type, details = self.detect_data_type(col_data)
        
        
        # Display data type information
        if data_type == "timestamp":
            self.data_type_info.setText(f" Timestamp data detected ({details})")
        elif data_type == "integer":
            self.data_type_info.setText(f" Integer data (Range: {details})")
        elif data_type == "float":
            self.data_type_info.setText(f" Float data")
        elif data_type == "numeric_string":
            self.data_type_info.setText(f" Numeric string ({details})")
        elif data_type == "mixed_numeric":
            self.data_type_info.setText(f" Mixed numeric type (Integer: {details})")
        elif data_type == "string":
            self.data_type_info.setText(f" Plain text (Lexicographic sort)")
        else:
            self.data_type_info.setText(f" Unknown type: {data_type}")
        # ====== Smart data type detection end ====== #

    def detect_data_type(self, series):
        """
        Intelligently detect column data type
        Returns: (type, details)
        Types include: 'timestamp', 'integer', 'float', 'numeric_string', 'mixed_numeric', 'string'
        """
        # Handle empty column
        if len(series) == 0:
            return "empty", "Empty column"
        
        # Get non-null samples (max 100)
        sample = series.dropna().head(100).tolist()
        if len(sample) == 0:
            return "empty", "All null values"
        
        # ====== 1. Detect timestamp format ====== #
        time_format = self.detect_timestamp_format(sample)
        if time_format:
            return "timestamp", time_format
        
        # ====== 2. Detect pure numeric types ====== #
        int_count = 0
        float_count = 0
        str_count = 0
        mixed_numeric = False
        
        for item in sample:
            if isinstance(item, (int, np.integer)):
                int_count += 1
            elif isinstance(item, (float, np.floating)):
                if not np.isnan(item):  # Ignore NaN
                    if item.is_integer():
                        int_count += 1
                    else:
                        float_count += 1
            elif isinstance(item, str):
                str_count += 1
                # Check if numeric string
                cleaned = item.strip().replace(',', '')
                if cleaned.startswith('-'):
                    cleaned = cleaned[1:]
                
                if cleaned.replace('.', '', 1).isdigit():
                    if '.' in cleaned:
                        float_count += 1
                    else:
                        int_count += 1
                # Check if scientific notation
                elif re.match(r'^\d+\.?\d*[eE][-+]?\d+', cleaned):
                    float_count += 1
        
        # Determine main type
        total_valid = int_count + float_count + str_count
        if total_valid == 0:
            return "empty", "No valid data"
        
        # Check if mainly numeric
        numeric_ratio = (int_count + float_count) / total_valid
        
        if numeric_ratio > 0.9:  # Over 90% numeric
            if float_count > 0 and int_count > 0:
                return "mixed_numeric", f"Integer: {int_count}, Float: {float_count}"
            elif float_count > 0:
                return "float", ""
            elif int_count > 0:
                # Get value range
                try:
                    min_val = min(series.dropna().astype(int))
                    max_val = max(series.dropna().astype(int))
                    return "integer", f"{min_val} to {max_val}"
                except:
                    return "integer", "Integer"
        
        # Check if numeric string
        if str_count > 0 and numeric_ratio > 0.5:
            return "numeric_string", "String containing numbers"
        
        # ====== 3. Default: plain string ====== #
        return "string", ""

    def detect_timestamp_format(self, sample):
        """
        Detect timestamp format
        Supports common formats:
        - YYYY-MM-DD HH:MM:SS
        - YYYY/MM/DD HH:MM:SS
        - MM/DD/YYYY HH:MM:SS
        - DD/MM/YYYY HH:MM:SS
        - YYYY-MM-DD
        - YYYY/MM/DD
        """
        # Common time formats
        formats = [
            ('%Y-%m-%d %H:%M:%S', 'YYYY-MM-DD HH:MM:SS'),
            ('%Y/%m/%d %H:%M:%S', 'YYYY/MM/DD HH:MM:SS'),
            ('%m/%d/%Y %H:%M:%S', 'MM/DD/YYYY HH:MM:SS'),
            ('%d/%m/%Y %H:%M:%S', 'DD/MM/YYYY HH:MM:SS'),
            ('%Y-%m-%d', 'YYYY-MM-DD'),
            ('%Y/%m/%d', 'YYYY/MM/DD'),
            ('%m/%d/%Y', 'MM/DD/YYYY'),
            ('%d/%m/%Y', 'DD/MM/YYYY')
        ]
        
        for fmt_code, fmt_desc in formats:
            valid_count = 0
            for item in sample:
                if not isinstance(item, str):
                    continue
                
                try:
                    # Try parsing
                    datetime.strptime(item.strip(), fmt_code)
                    valid_count += 1
                except (ValueError, TypeError):
                    continue
            
            # If over 80% of samples match this format, consider it valid
            if valid_count >= len(sample) * 0.8 and valid_count > 0:
                return fmt_desc
        
        return None

    def prepare_data_for_sorting(self, series):
        """
        Prepare data for sorting
        Returns: (converted data list, data type, conversion info)
        """
        data_type, details = self.detect_data_type(series)
        
        if data_type == "timestamp":
            # ====== Convert timestamp ====== #
            time_format = details
            format_map = {
                'YYYY-MM-DD HH:MM:SS': '%Y-%m-%d %H:%M:%S',
                'YYYY/MM/DD HH:MM:SS': '%Y/%m/%d %H:%M:%S',
                'MM/DD/YYYY HH:MM:SS': '%m/%d/%Y %H:%M:%S',
                'DD/MM/YYYY HH:MM:SS': '%d/%m/%Y %H:%M:%S',
                'YYYY-MM-DD': '%Y-%m-%d',
                'YYYY/MM/DD': '%Y/%m/%d',
                'MM/DD/YYYY': '%m/%d/%Y',
                'DD/MM/YYYY': '%d/%m/%Y'
            }
            fmt_code = format_map.get(time_format, '%Y-%m-%d %H:%M:%S')
            
            timestamps = []
            for item in series:
                if pd.isna(item):
                    timestamps.append(float('-inf'))  # Handle NaN as minimum value
                    continue
                
                try:
                    # Try conversion
                    dt_str = str(item).strip()
                    dt = datetime.strptime(dt_str, fmt_code)
                    timestamps.append(int(dt.timestamp()))
                except (ValueError, TypeError):
                    # Handle unconvertible values as special value
                    timestamps.append(float('-inf'))
            
            return [int(ts) for ts in timestamps], "float", f"Converted to Unix timestamp ({time_format})"
        
        elif data_type in ["integer", "float", "mixed_numeric", "numeric_string"]:
            # ====== Convert to numeric ====== #
            numeric_values = []
            for item in series:
                if pd.isna(item):
                    numeric_values.append(float('-inf'))
                    continue
                
                try:
                    # Handle string numerics
                    if isinstance(item, str):
                        cleaned = item.strip().replace(',', '')
                        # Handle percentages
                        if cleaned.endswith('%'):
                            cleaned = cleaned[:-1]
                            value = float(cleaned) / 100.0
                        else:
                            value = float(cleaned)
                    else:
                        value = float(item)
                    
                    numeric_values.append(value)
                except (ValueError, TypeError):
                    numeric_values.append(float('-inf'))
            
            # Determine final type
            final_type = "float" if any(isinstance(x, float) and not np.isinf(x) and not x.is_integer() for x in numeric_values) else "int"
            return numeric_values, final_type, f"Unified conversion to {final_type}"
        
        else:  # string or unknown
            # ====== Plain string handling ====== #
            string_values = []
            for item in series:
                if pd.isna(item) or item == "" or str(item).strip() == "":
                    string_values.append("")  # Empty strings at the front
                else:
                    string_values.append(str(item).strip())
            
            return string_values, "string", "Lexicographic sort"

    def perform_sort(self):
        # Fix 4: Retrieve latest data before each sort
        selected_item = self.parent().narrow_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Sort Failed", "Please select a variable to sort")
            return
        
        var_name = selected_item.text()
        df = self.data_frames.get(var_name)
        if df is None:
            QMessageBox.warning(self, "Sort Failed", "Data does not exist")
            return
        
        # Fix 5: Use current UI state directly, not instance variables
        sort_column = self.column_combo.currentText()
        sort_order = self.order_combo.currentText()
        selected_algorithm = self.algorithm_combo.currentText()
        
        # Ensure sort column exists in dataframe
        if sort_column not in df.columns:
            QMessageBox.warning(self, "Sort Failed", f"Selected sort column '{sort_column}' does not exist")
            return

        # Perform sort
        ascending = True if sort_order == "Ascending" else False
        
        try:
            if selected_algorithm == "Default (Pandas)":
                # ====== Smart sort: handle mixed data types ====== #
                col_data = df[sort_column]
                data_type, _ = self.detect_data_type(col_data)
                
                if data_type == "timestamp":
                    # Convert to datetime type then sort
                    time_format = self.detect_timestamp_format(col_data.dropna().head(100).tolist())
                    if time_format:
                        format_map = {
                            'YYYY-MM-DD HH:MM:SS': '%Y-%m-%d %H:%M:%S',
                            'YYYY/MM/DD HH:MM:SS': '%Y/%m/%d %H:%M:%S',
                            'MM/DD/YYYY HH:MM:SS': '%m/%d/%Y %H:%M:%S',
                            'DD/MM/YYYY HH:MM:SS': '%d/%m/%Y %H:%M:%S',
                            'YYYY-MM-DD': '%Y-%m-%d',
                            'YYYY/MM/DD': '%Y/%m/%d',
                            'MM/DD/YYYY': '%m/%d/%Y',
                            'DD/MM/YYYY': '%d/%m/%Y'
                        }
                        fmt_code = format_map.get(time_format, '%Y-%m-%d %H:%M:%S')
                        
                        # Create temporary column for conversion
                        temp_col = df[sort_column].apply(
                            lambda x: pd.to_datetime(str(x).strip(), format=fmt_code, errors='coerce')
                        )
                        sorted_df = df.assign(_temp_sort=temp_col).sort_values(
                            by='_temp_sort', ascending=ascending
                        ).drop('_temp_sort', axis=1)
                    else:
                        # Cannot recognize format, sort as string
                        sorted_df = df.sort_values(by=sort_column, ascending=ascending)
                else:
                    # Use Pandas built-in sort (automatically handles mixed types)
                    sorted_df = df.sort_values(by=sort_column, ascending=ascending)
                
                new_var_name = f"{var_name}_sorted"
            
            else:
                # ====== Custom sorting algorithm handling ====== #
                col_data = df[sort_column].copy()
                
                # 1. Smart data preparation
                data_list, data_type, conversion_info = self.prepare_data_for_sorting(col_data)
                
                # 2. Special type validation
                if "Counting Sort (CountingSort)" in selected_algorithm:
                    if data_type not in ["int", "integer"]:
                        raise ValueError(f"Counting Sort only supports integer columns!\nCurrent column: {sort_column}\nType: {data_type} ({conversion_info})")
                
                elif any(name in selected_algorithm for name in ["Quick", "Merge", "Heap"]):
                    if data_type not in ["int", "integer", "float"]:
                        raise ValueError(f"Numeric sorting algorithms only support numeric columns!\nCurrent column: {sort_column}\nType: {data_type} ({conversion_info})")
                
                # 3. Create index mapping (maintain row integrity)
                indices = np.arange(len(col_data))
                
                # 4. Select sorting algorithm
                if "Quick Sort (QuickSort)" in selected_algorithm:
                    from sort import QuickSort
                    sorter = QuickSort()
                    # Create (value, index) pairs to maintain stability
                    paired = list(zip(data_list, indices))
                    # Sort by value
                    paired.sort(key=lambda x: x[0])  # Temporarily use built-in sort for stability
                    sorted_indices = [idx for (_, idx) in paired]
                
                elif "Merge Sort (MergeSort)" in selected_algorithm:
                    from sort import MergeSort
                    sorter = MergeSort()
                    # Create (value, index) pairs
                    paired = list(zip(data_list, indices))
                    # Sort by value
                    paired.sort(key=lambda x: x[0])  # Temporarily use built-in sort
                    sorted_indices = [idx for (_, idx) in paired]
                
                elif "Heap Sort (HeapSort)" in selected_algorithm:
                    from sort import HeapSort
                    sorter = HeapSort()
                    # Heap sort is unstable, needs special handling
                    paired = list(zip(data_list, indices))
                    # Sort by value
                    paired.sort(key=lambda x: x[0])  # Temporarily use built-in sort
                    sorted_indices = [idx for (_, idx) in paired]
                
                elif "Counting Sort (CountingSort)" in selected_algorithm:
                    from sort import CountingSort
                    sorter = CountingSort()
                    # Only valid for integers
                    valid_pairs = []
                    invalid_indices = []
                    
                    for i, val in enumerate(data_list):
                        if not np.isinf(val) and isinstance(val, (int, float)) and not np.isnan(val):
                            # Ensure integer
                            int_val = int(round(val))
                            valid_pairs.append((int_val, i))
                        else:
                            invalid_indices.append(i)
                    
                    if not valid_pairs:
                        raise ValueError("No valid integer values for counting sort")
                    
                    # Sort by value
                    valid_pairs.sort(key=lambda x: x[0])
                    sorted_indices = [idx for (_, idx) in valid_pairs]
                    sorted_indices.extend(invalid_indices)  # Invalid values at the end
                
                # 5. Apply sort (key: maintain row integrity)
                sorted_df = df.iloc[sorted_indices]
                
                # 6. Handle descending order
                if not ascending:
                    sorted_df = sorted_df.iloc[::-1]
                
                # 7. Generate new variable name
                algo_abbr = "".join([s[0] for s in selected_algorithm.split(" (")[0].split()[:2]])
                new_var_name = f"{var_name}_{algo_abbr}_sorted"
            
            # Save result
            self.parent().data_frames[new_var_name] = sorted_df
            self.parent().narrow_widget.addItem(new_var_name)
            
            # Get data type information for display
            col_data = df[sort_column]
            data_type, details = self.detect_data_type(col_data)
            
            QMessageBox.information(self, "Sort Successful", 
                f"Sort completed!\n"
                f"Algorithm: {selected_algorithm}\n"
                f"Column: '{sort_column}'\n"
                f"Data type: {data_type}\n"
                f"Conversion: {conversion_info if 'conversion_info' in locals() else 'None'}\n"
                f"New variable name: {new_var_name}\n"
                f"Rows: {len(sorted_df)}")
        
        except Exception as e:
            QMessageBox.critical(self, "Sort Error", f"Sort failed: {str(e)}\n\nDetails:\nColumn: {sort_column}\nAlgorithm: {selected_algorithm}")
            import traceback
            print("Sort error details:", traceback.format_exc())
            return        
        self.close()

### Export Data Dialog Window ###
class ExportDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("Export Data")
        self.data_frames = data_frames
        self.selected_frames = []
        self.export_path = ""  # Export path

        # Create layout
        layout = QVBoxLayout()

        # Multi-select widget
        self.multi_select_widget = QListWidget()
        self.multi_select_widget.setAlternatingRowColors(True)
        self.multi_select_widget.setSpacing(5)
        for var_name in self.data_frames.keys():
            item = QListWidgetItem(var_name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.multi_select_widget.addItem(item)
        self.multi_select_widget.itemChanged.connect(self.update_selection)
        layout.addWidget(self.multi_select_widget)

        # Export path selection component
        input_layout = QHBoxLayout()
        label = QLabel("Export Path")
        input_layout.addWidget(label)
        self.export_path_input = QLineEdit()
        self.export_path_input.setPlaceholderText("Current directory")
        self.export_path_input.setReadOnly(True)
        input_layout.addWidget(self.export_path_input)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.select_export_path)
        input_layout.addWidget(browse_button)
        layout.addLayout(input_layout)

        # Button layout
        button_layout = QHBoxLayout()
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_data)
        button_layout.addWidget(export_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_selection(self):
        self.selected_frames = []
        for index in range(self.multi_select_widget.count()):
            item = self.multi_select_widget.item(index)
            if item.checkState() == Qt.Checked:
                self.selected_frames.append(item.text())

    def select_export_path(self):
        # Open file selection dialog to choose export path
        export_path = QFileDialog.getExistingDirectory(self, "Select Export Path")
        if export_path:
            self.export_path = export_path
            self.export_path_input.setText(export_path)

    def export_data(self):
        if not self.selected_frames:
            QMessageBox.warning(self, "Export Failed", "Please select variables to export")
            return
        if not self.export_path:
            QMessageBox.warning(self, "Export Failed", "Please select export path")
            return
        for var_name in self.selected_frames:
            df = self.data_frames[var_name]
            file_path = f"{self.export_path}/{var_name}.csv"
            df.to_csv(file_path, index=False)
        QMessageBox.information(self, "Export Successful", "Selected variables have been successfully exported as CSV files")
        self.close()


### Merge DataFrames Dialog Window ###
class MergeDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("Merge Data")
        self.data_frames = data_frames
        self.selected_frames = []
        self.new_var_name = ""

        # Create layout
        layout = QVBoxLayout()

        # Multi-select widget
        self.multi_select_widget = QListWidget()
        self.multi_select_widget.setAlternatingRowColors(True)
        self.multi_select_widget.setSpacing(5)
        for var_name in self.data_frames.keys():
            item = QListWidgetItem(var_name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.multi_select_widget.addItem(item)
        self.multi_select_widget.itemChanged.connect(self.update_selection)
        layout.addWidget(self.multi_select_widget)

        # Input component
        input_layout = QHBoxLayout()
        label = QLabel("New Variable Name")
        input_layout.addWidget(label)
        self.new_var_name_input = QLineEdit()
        self.new_var_name_input.setPlaceholderText("Default name")
        self.new_var_name_input.setReadOnly(True)
        input_layout.addWidget(self.new_var_name_input)
        layout.addLayout(input_layout)

        # Button layout
        button_layout = QHBoxLayout()
        merge_button = QPushButton("Merge")
        merge_button.clicked.connect(self.merge_data)
        button_layout.addWidget(merge_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_selection(self):
        self.selected_frames = []
        for index in range(self.multi_select_widget.count()):
            item = self.multi_select_widget.item(index)
            if item.checkState() == Qt.Checked:
                self.selected_frames.append(item.text())
        if self.selected_frames:
            self.new_var_name_input.setPlaceholderText(self.selected_frames[0] + "_merge")
            self.new_var_name_input.setReadOnly(False)
        else:
            self.new_var_name_input.setPlaceholderText("Default name")
            self.new_var_name_input.setReadOnly(True)

    def merge_data(self):
        if len(self.selected_frames) < 2:
            QMessageBox.warning(self, "Merge Failed", "At least two variables need to be selected for merging")
            return
        # Use pd.concat to vertically concatenate dataframes
        merged_df = pd.concat([self.data_frames[var_name] for var_name in self.selected_frames], ignore_index=True)
        new_var_name = self.new_var_name_input.text() or self.new_var_name_input.placeholderText()
        self.parent().data_frames[new_var_name] = merged_df
        self.parent().narrow_widget.addItem(new_var_name)
        self.close()

### Search Data Dialog Window ###
class SearchDialog(QDialog):
    def __init__(self, parent=None, data_frames=None):
        super().__init__(parent)
        self.setWindowTitle("Search Data")
        self.data_frames = data_frames
        self.search_results = []

        # Create layout
        layout = QVBoxLayout()

        # Search input box
        input_layout = QHBoxLayout()
        label = QLabel("Search Keyword")
        input_layout.addWidget(label)
        self.search_input = QLineEdit()
        input_layout.addWidget(self.search_input)
        layout.addLayout(input_layout)

        # Search results list
        self.search_results_widget = QListWidget()
        layout.addWidget(self.search_results_widget)

        # Button layout
        button_layout = QHBoxLayout()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        button_layout.addWidget(search_button)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def perform_search(self):
        keyword = self.search_input.text().strip()
        if not keyword:
            QMessageBox.warning(self, "Search Failed", "Please enter a search keyword")
            return
        
        self.search_results = []
        for var_name, df in self.data_frames.items():
            # === Optimization 1: Skip numeric columns that cannot match ===
            # Only check numeric columns when keyword is pure numeric
            numeric_cols = df.select_dtypes(include=np.number).columns

            str_cols = df.columns.difference(numeric_cols)
            
            # === Optimization 2: Process in chunks to reduce memory peak ===
            mask = pd.Series(False, index=df.index)  # Initialize all False
            
            # Process string columns (direct comparison)
            if not str_cols.empty:
                str_df = df[str_cols].astype(str)
                mask |= str_df.eq(keyword).any(axis=1)
            
            # Process numeric columns (only when keyword is numeric)
            if numeric_cols.any() and keyword.replace('.', '', 1).isdigit():
                num_val = float(keyword) if '.' in keyword else int(keyword)
                num_df = df[numeric_cols]
                mask |= num_df.eq(num_val).any(axis=1)
            
            filtered_df = df[mask]
            if not filtered_df.empty:
                self.search_results.append((var_name, filtered_df))
        
        self.update_search_results()

    def update_search_results(self):
        self.search_results_widget.clear()
        for var_name, df in self.search_results:
            item = QListWidgetItem(f"{var_name} ({len(df)} results)")
            self.search_results_widget.addItem(item)


### Main Window ###
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 GUI Example")
        self.resize(800, 600)
        self.data_frames = {}  # Store imported data
        self.current_page = 1
        self.page_size   = 100
        self.current_var = None          # Currently displayed variable name

        # Create main layout
        main_layout = QHBoxLayout()

        # Left button layout
        left_layout = QVBoxLayout()
        buttons = ["Import", "Merge", "Delete", "Search", "Sort", "Export", "Exit"]
        self.buttons = {}
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setMinimumHeight(50)
            if button_text == "Import":
                button.clicked.connect(self.import_data)
            elif button_text == "Merge":
                button.clicked.connect(self.merge_data)
            elif button_text == "Delete":
                button.clicked.connect(self.delete_data)
            elif button_text == "Search":
                button.clicked.connect(self.search_data)
            elif button_text == "Sort":
                button.clicked.connect(self.sort_data)
            elif button_text == "Export":
                button.clicked.connect(self.export_data)
            elif button_text == "Exit":
                button.clicked.connect(self.exit_app)
            left_layout.addWidget(button)
            self.buttons[button_text] = button

        # Create left frame and set layout
        left_frame = QFrame()
        left_frame.setLayout(left_layout)
        left_frame.setFixedWidth(150)

        # Right layout
        right_layout = QVBoxLayout()

        # Right narrow widget (display options, selectable and highlighted)
        self.narrow_widget = QListWidget()
        self.narrow_widget.setFixedHeight(100)  # Set height to make it narrower
        self.narrow_widget.itemSelectionChanged.connect(self.display_data)
        right_layout.addWidget(self.narrow_widget)

        # Right wide widget (display table)
        self.wide_widget = QTableWidget()
        self.wide_widget.cellClicked.connect(self.update_row_label)  # Bind cell click event
        right_layout.addWidget(self.wide_widget)

        # Pagination control bar
        page_bar = QHBoxLayout()
        page_bar.addStretch(1)                # Left flexible spacer

        self.prev_btn = QPushButton("<")
        self.prev_btn.setFixedWidth(40)       # Make smaller
        self.prev_btn.clicked.connect(self.prev_page)
        page_bar.addWidget(self.prev_btn)

        self.page_label = QLabel("Page 0/0")
        page_bar.addWidget(self.page_label)

        self.next_btn = QPushButton(">")
        self.next_btn.setFixedWidth(40)
        self.next_btn.clicked.connect(self.next_page)
        page_bar.addWidget(self.next_btn)

        self.page_edit = QLineEdit()
        self.page_edit.setFixedWidth(80)
        self.page_edit.setPlaceholderText("Page")
        page_bar.addWidget(self.page_edit)

        self.go_btn = QPushButton("Go")
        self.go_btn.setFixedWidth(80)
        self.go_btn.clicked.connect(self.goto_page)
        page_bar.addWidget(self.go_btn)

        page_widget = QWidget()
        page_widget.setLayout(page_bar)
        right_layout.addWidget(page_widget)

        # Create right frame and set layout
        right_frame = QFrame()
        right_frame.setLayout(right_layout)

        # Add left and right frames to main layout
        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)

        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def import_data(self):
        # Open file selection dialog, allow selecting multiple .csv files
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files", ".", "CSV Files (*.csv)")
        if file_names:
            target_cols = [
                "VehicleType",
                "DetectionTime_O",
                "GantryID_O",
                "DetectionTime_D",
                "GantryID_D",
                "TripLength",
                "TripEnd",
                "TripInformation"
            ]
            for file_name in file_names:
                df = pd.read_csv(file_name, header=None)
                df.columns = target_cols
                var_name = file_name.split("/")[-1].replace(".csv", "")
                self.data_frames[var_name] = df
                self.narrow_widget.addItem(var_name)

    def merge_data(self):
        if len(self.data_frames) < 2:
            QMessageBox.warning(self, "Merge Failed", "At least two variables are required for merging")
            return
        merge_dialog = MergeDialog(self, self.data_frames)
        merge_dialog.exec_()

    def delete_data(self):
        selected_item = self.narrow_widget.currentItem()
        if selected_item:
            var_name = selected_item.text()
            del self.data_frames[var_name]
            self.narrow_widget.takeItem(self.narrow_widget.row(selected_item))
            self.wide_widget.clear()
            # self.row_label.setText("0/0")

    def search_data(self):
        if not self.data_frames:
            QMessageBox.warning(self, "Search Failed", "No imported data available for search")
            return
        search_dialog = SearchDialog(self, self.data_frames)
        search_dialog.exec_()

    def sort_data(self):
        if not self.data_frames:
            QMessageBox.warning(self, "Sort Failed", "No data available for sorting")
            return
        sort_dialog = SortDialog(self, self.data_frames)
        sort_dialog.exec_()

    def export_data(self):
        if not self.data_frames:
            QMessageBox.warning(self, "Export Failed", "No data available for export")
            return
        export_dialog = ExportDialog(self, self.data_frames)
        export_dialog.exec_()

    def exit_app(self):
        # Pop up confirmation exit dialog
        reply = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to exit the program?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Release all memory, clear all variables
            self.data_frames.clear()
            self.narrow_widget.clear()
            self.close()

    def display_data(self):
        item = self.narrow_widget.currentItem()
        if not item:
            return
        self.current_var = item.text()
        self.current_page = 1          # Return to page 1 when switching variables
        self.show_page()

    def update_row_label(self, row=None, col=None):
        selected_item = self.narrow_widget.currentItem()
        if selected_item:
            var_name = selected_item.text()
            df = self.data_frames.get(var_name)
            if df is not None:
                total_rows = len(df)  # Use total rows of dataframe
                if row is None:
                    row = self.wide_widget.currentRow()
                if row is not None:
                    self.row_label.setText(f"{row + 1}/{total_rows}")
                    
                else:
                    self.row_label.setText(f"0/{total_rows}")
                
    def show_page(self):
        """Refresh table based on current page number"""
        df = self.data_frames.get(self.current_var)
        if df is None:
            return
        total_rows = len(df)
        total_pages = (total_rows + self.page_size - 1) // self.page_size
        self.page_label.setText(f"Page {self.current_page}/{total_pages}")

        start = (self.current_page - 1) * self.page_size
        end   = start + self.page_size
        page_df = df.iloc[start:end]

        self.wide_widget.setColumnCount(len(page_df.columns))
        self.wide_widget.setRowCount(len(page_df))
        self.wide_widget.setHorizontalHeaderLabels(page_df.columns.tolist())

        for r in range(len(page_df)):
            for c in range(len(page_df.columns)):
                self.wide_widget.setItem(r, c,
                                         QTableWidgetItem(str(page_df.iloc[r, c])))

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        df = self.data_frames.get(self.current_var)
        if df is None:
            return
        total_pages = (len(df) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages:
            self.current_page += 1
            self.show_page()

    def goto_page(self):
        df = self.data_frames.get(self.current_var)
        if df is None:
            return
        total_pages = (len(df) + self.page_size - 1) // self.page_size
        try:
            page = int(self.page_edit.text())
            if 1 <= page <= total_pages:
                self.current_page = page
                self.show_page()
            else:
                QMessageBox.warning(self, "Notice", f"Page range: 1-{total_pages}")
        except ValueError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

