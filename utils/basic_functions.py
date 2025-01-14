from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox, QComboBox
from PyQt5.QtGui import QBrush, QColor
import numpy as np

def show_warning_message(self, message):
    """Displays a warning message box with the provided message."""
    try:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.exec_()
    except Exception as e:
        # Handle any unexpected errors gracefully
        print(f"Error displaying warning message: {e}")

def open_file_dialog(self):
    """Opens a file dialog for selecting session files and adds them to the table."""
    try:
        mne_compatible_extensions = "MNE Files (*.fif *.edf *.bdf *.gdf *.set)"
        files, _ = QFileDialog.getOpenFileNames(self, "Select Session Files", "", mne_compatible_extensions)
        if files:
            for file in files:
                # Add the selected file if it's not already in the list
                if file not in self.selected_files:
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    self.table.setItem(row_position, 0, QTableWidgetItem(file))
                    self.selected_files.append(file)
                else:
                    self.show_warning_message(f"The file '{file}' has already been selected.")
            # Update the state of the next button and the session table
            self.update_next_button_state()
            self.update_session_table()
    except Exception as e:
        # Handle any file dialog errors
        print(f"Error opening file dialog: {e}")

def remove_selected_files(self):
    """Removes selected files from the table and the list of selected files."""
    try:
        selected_rows = self.table.selectionModel().selectedRows()
        for row in reversed(selected_rows):
            file_to_remove = self.table.item(row.row(), 0).text()
            self.selected_files.remove(file_to_remove)
            self.table.removeRow(row.row())
        # Update the state of the next button and the session table
        self.update_next_button_state()
        self.update_session_table()
    except Exception as e:
        # Handle any errors while removing files
        print(f"Error removing selected files: {e}")

def remove_all_files(self):
    """Removes all selected files from the table and list."""
    try:
        self.selected_files.clear()  # Clear the list of selected files
        self.table.setRowCount(0)  # Clear all rows in the table
        self.update_next_button_state()  # Update next button state based on empty list
        self.update_session_table()  # Update the session table if necessary
    except Exception as e:
        # Handle any errors while removing all files
        print(f"Error removing all files: {e}")
    
def update_remove_button_state(self):
    """Updates the state of the remove button based on selection in the table."""
    try:
        self.remove_button.setEnabled(self.table.selectionModel().hasSelection())
    except Exception as e:
        # Handle any errors while updating the remove button state
        print(f"Error updating remove button state: {e}")
    
def update_next_button_state(self):
    """Updates the state of the next button based on various conditions."""
    try:
        intervals_per_recording = int(self.intervals_input.text())  # Parse the number of intervals
        self.intervals_per_recording = intervals_per_recording  # Store the value of intervals_per_recording
        project_filled = bool(self.project_dir_input.text().strip())  # Check if the project field is filled
        self.next_button.setEnabled(intervals_per_recording > 0 and len(self.selected_files) > 0 and project_filled )
    except ValueError:
        # If the value in intervals_input is not an integer, disable the next button
        self.next_button.setEnabled(False)
    except Exception as e:
        # Handle other unexpected errors
        print(f"Error updating next button state: {e}")

def go_back(self):
    """Switches back to the previous screen in the stacked widget."""
    try:
        self.stacked_widget.setCurrentIndex(0)
    except Exception as e:
        # Handle any errors while navigating to the previous screen
        print(f"Error navigating back: {e}")

def show_notification(self, message):
    """Displays a notification message box with the provided message."""
    try:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Notification")
        msg.setText(message)
        msg.exec_()
    except Exception as e:
        # Handle any errors while displaying the notification
        print(f"Error displaying notification: {e}")

def setup_item_changed_signals(self):
    """Sets up the itemChanged signal for the session_table to trigger a function."""
    try:
        self.session_table.itemChanged.connect(self.plot_eeg_channels)
    except Exception as e:
        # Handle any errors while connecting signals
        print(f"Error setting up itemChanged signal: {e}")

def setup_item_clicked_signals(self):
    """Sets up the itemClicked signal for the session_table to trigger a function."""
    try:
        self.session_table.itemClicked.connect(self.plot_eeg_channels)
    except Exception as e:
        # Handle any errors while connecting signals
        print(f"Error setting up itemClicked signal: {e}")

def clear_all_fields(self):
    """Clears all input fields and removes selected files."""
    try:
        self.remove_all_files()
        # Reset the project directory input
        self.project_dir_input.clear()
        # Reset the intervals input field
        self.intervals_input.clear()  # Clears the input
        self.intervals_input.setPlaceholderText("Enter an Integer > 1")
        # Force the field to lose focus (optional, ensures placeholder shows immediately)
        self.intervals_input.clearFocus()
    except Exception as e:
        # Handle any errors while clearing fields
        print(f"Error clearing all fields: {e}")

def highlight_invalid_times(self, item):
    self.session_table.clearSelection()
    table_data = get_table_data(self, self.session_table)
    # print(table_data)
    num_rows, num_cols = table_data.shape
    # print(f"num_rows: {num_rows}, num_cols: {num_cols}")
    invalid_indices = np.zeros((num_rows, num_cols-1))
    for row in range(num_rows):
        file = self.selected_files[row]
        raw = self.mne_data_objects[file]
        start_time = float(raw.times[0])
        end_time = float(raw.times[-1])
        for col in range(1, num_cols -1, 2):
            t1 = table_data[row][col]
            t2 = table_data[row][col + 1]
            state = None
            try:
                t1 = float(t1)
                if t1 < start_time or t1 > end_time:
                    invalid_indices[row][col -1 ] = 1
            except:
                invalid_indices[row][col - 1] = 1
            try:
                t2 = float(t2)
                if t2 < start_time or t2 > end_time:
                    invalid_indices[row][col] = 1
            except:
                invalid_indices[row][col] = 1
            try: 
                t1 = float(t1)
                t2 = float(t2)
                if t1 >= t2:
                    invalid_indices[row][col-1] = 1
                    invalid_indices[row][col] = 1
            except:
                pass
            
            if col + 2 == num_cols -1:
                state = table_data[row][-1]
                if state not in ('Active', 'Inactive'):
                    invalid_indices[row][-1] = 1

    # print(invalid_indices)

    for row in range(num_rows):
        for col in range(num_cols - 1):
            if  invalid_indices[row][col]:
                if col + 1 == num_cols -1 and self.intervals_per_recording == 1:
                    self.session_table.cellWidget(row,col + 1).setStyleSheet("background-color: red;")
                else:
                    self.session_table.item(row, col + 1).setBackground(QBrush(QColor('red')))
            else:
                if col + 1 == num_cols -1 and self.intervals_per_recording == 1:
                    # print(num_cols)
                    self.session_table.cellWidget(row,col + 1).setStyleSheet("background-color: white;")
                else:
                    self.session_table.item(row, col + 1).setBackground(QBrush(QColor('white')))

    # self.session_table.cellWidget(row,num_cols-1).setStyleSheet("background-color: red;")

    # for row in range(num_rows):
    #     for col in range(num_cols - 1):
    #         if col + 2 == num_cols -1:
    #             item = self.session_table.cellWidget(row, col + 1)
    #         else:
    #             item = self.session_table.item(row, col + 1)
    #         if invalid_indices[row][col]:
    #             # Check if the item is a QComboBox and set the background color to red
    #             if isinstance(item, QComboBox):
    #                 item.setStyleSheet("background-color: red;")
    #             else:
    #                 item.setBackground(QBrush(QColor('red')))
    #         else:
    #             # If not invalid, reset to white
    #             if isinstance(item, QComboBox):
    #                 item.setStyleSheet("background-color: white;")
    #             else:
    #                 item.setBackground(QBrush(QColor('white')))

        
    if  not np.sum(invalid_indices):
        self.save_button.setEnabled(1)
    else :
        self.save_button.setEnabled(0)


def get_table_data(self, table_widget):
    # Create an empty NumPy array with the shape of the table
    data = np.empty((table_widget.rowCount(), table_widget.columnCount()), dtype=object)
    if self.intervals_per_recording == 1:
        num_cols = table_widget.columnCount()-1
    else:
        num_cols = table_widget.columnCount()
    
    num_rows = table_widget.rowCount()
    
    for row in range(num_rows):
        for column in range(num_cols):
            item = table_widget.item(row, column)  # Get QTableWidgetItem
            if item is not None:
                data[row, column] = item.text()  # Assign text if item exists
            else:
                data[row, column] = ""  # Assign empty string if no item exists

    if self.intervals_per_recording == 1:
        for row in range(num_rows):
            combo_box = table_widget.cellWidget(row, num_cols)
            if combo_box and isinstance(combo_box, QComboBox):
                data[row, num_cols] = combo_box.currentText()
                # print(combo_box.currentText())
            else:
                data[row, num_cols] = ""


    return data      

def clear_highlight(self,item):
    item.setBackground(QBrush(QColor('white')))

def set_save_off(self,item):
    self.save_button.setEnabled(0)

def row_selection_changed(self):
    # Get the currently selected row
    current_row = self.session_table.currentRow()

    # Compare with the previous row
    if not hasattr(self, 'previous_row'):  # Initialize if it doesn't exist
        self.previous_row = current_row

    if current_row != self.previous_row:
        # print(f"Row changed from {self.previous_row} to {current_row}")
        self.previous_row = current_row  # Update the previous row
        self.plot_eeg_channels()