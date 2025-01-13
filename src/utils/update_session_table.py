from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox
import os

def update_session_table(self):
    # Set up the table for the selected files
    self.session_table.setRowCount(0)
    
    # Prepare the new headers
    headers = ["Sessions"]
    for interval in range(1, self.intervals_per_recording + 1):
        headers.append(f"I{interval}T1")
        headers.append(f"I{interval}T2")
    
    # Check if we need to add an extra column when intervals_per_recording == 1
    if self.intervals_per_recording == 1:
        headers.append("State")  # Add the new column header

    self.session_table.setColumnCount(len(headers))
    self.session_table.setHorizontalHeaderLabels(headers)

    # Make column headers non-editable
    for col in range(len(headers)):
        header_item = self.session_table.horizontalHeaderItem(col)
        if header_item:
            header_item.setFlags(header_item.flags() & ~Qt.ItemIsEditable)

    # Add rows for each session
    for i, file in enumerate(self.selected_files):
        row_position = self.session_table.rowCount()
        self.session_table.insertRow(row_position)
        file_name = os.path.basename(file)  # Get only the file name, not the full path
        item = QTableWidgetItem(f"Session {i + 1} - {file_name}")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make row headers non-editable
        self.session_table.setItem(row_position, 0, item)
        
        # Populate interval cells with empty QTableWidgetItem
        for col in range(1, len(headers)):
            self.session_table.setItem(row_position, col, QTableWidgetItem(""))

        # Add the drop-down list in the new column if intervals_per_recording == 1
        if self.intervals_per_recording == 1:
            combo_box = QComboBox()

            # Add other valid options
            combo_box.addItems(["Active", "Inactive"])
            
            # Set the combo box to the 'Active' state by default, or just leave it uninitialized
            combo_box.setCurrentIndex(-1)  # Or remove this line to leave it uninitialized

            # Set the combo box in the cell of the extra column
            self.session_table.setCellWidget(row_position, len(headers) - 1, combo_box)
            # print(f"Combo box value: {combo_box.currentText()}")

            