import mne
from PyQt5.QtWidgets import QFileDialog, QComboBox
import os

def save_cropped_data_as_edf(self):
    # Create directory for saving EDF files
    save_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save EDF Files")
    if not save_dir:
        return  # User canceled the save dialog

    project_dir = os.path.join(save_dir, self.project_dir_input.text())
    
    if os.path.exists(project_dir):
        # Check if the directory exists, and if so, append a number to the name
        project_dir_with_num = project_dir
        counter = 0
        while os.path.exists(project_dir_with_num):
            counter += 1
            project_dir_with_num = f'{project_dir}_{counter}'
        project_dir = project_dir_with_num
    
    os.makedirs(project_dir)
    if self.intervals_per_recording > 1:
        # Iterate through selected sessions
        for row in range(self.session_table.rowCount()):
            file_path = self.selected_files[row]
            if file_path in self.mne_data_objects:
                raw = self.mne_data_objects[file_path]

                # Get the parent filename (e.g., remove directory path)
                root, _ = os.path.splitext(file_path)
                parent_filename = str(os.path.basename(root)).replace('.', '_')

                # Extract first and last timestamps
                first_timestamp = raw.times[0]  # The first timestamp in the raw data
                last_timestamp = raw.times[-1]  # The last timestamp in the raw data

                # Iterate over intervals and save the cropped data from T1 to T2
                for interval_num in range(self.intervals_per_recording):
                    # Get start and end times for the current interval (T1 to T2)
                    start_time_item = self.session_table.item(row, 2 * interval_num + 1)  # T1
                    end_time_item = self.session_table.item(row, 2 * interval_num + 2)  # T2

                    # If both start and end times are available
                    if start_time_item and end_time_item:
                        try:
                            start_time = float(start_time_item.text())
                            end_time = float(end_time_item.text())

                            # Validate times: Ensure they are within the range of raw data's timestamps
                            if start_time < 0 or end_time < 0 or start_time >= end_time:
                                raise ValueError("Start time must be less than end time and non-negative.")
                            if start_time < first_timestamp or end_time > last_timestamp:
                                raise ValueError(f"Times must be between {first_timestamp} and {last_timestamp}.")

                            # Remove decimal points from the start and end times
                            start_time_str = str(start_time).replace('.', '_') + 's'
                            end_time_str = str(end_time).replace('.', '_') + 's'

                            # Create a directory for the current interval (if it doesn't exist)
                            interval_dir = os.path.join(project_dir, f"interval_{interval_num + 1}")
                            if not os.path.exists(interval_dir):
                                os.makedirs(interval_dir)  # Create the directory if it doesn't exist

                            # Create a new filename for the saved cropped data
                            new_filename = f"{parent_filename}_T1_{start_time_str}_T2_{end_time_str}.edf"
                            new_file_path = os.path.join(interval_dir, new_filename)

                            # Crop the raw data between start_time and end_time
                            start_sample = int(start_time * raw.info['sfreq'])  # Convert time to sample index
                            end_sample = int(end_time * raw.info['sfreq'])  # Convert time to sample index
                            cropped_data = raw.get_data(start=start_sample, stop=end_sample, verbose=0)

                            # Create a new Raw object for the cropped data
                            info = raw.info
                            cropped_raw = mne.io.RawArray(cropped_data, info, verbose=0)

                            # Export the cropped data as an EDF file
                            mne.export.export_raw(new_file_path, cropped_raw, fmt='edf', overwrite=True, verbose=0)

                        except ValueError as ve:
                            # Show warning for invalid time values and return to main screen
                            self.show_warning_message(f"Invalid time values for interval {interval_num + 1} in session {parent_filename}: {ve}")
                            return  # Exit the function, no crops saved
                        except Exception as e:
                            # Show general error message and return to main screen
                            self.show_warning_message(f"Error saving cropped data: {e}")
                            return  # Exit the function, no crops saved

    else:
        # print('Testing Single Interval Crops')
        active_state_dir = os.path.join(project_dir, f"active_state")
        inactive_state_dir = os.path.join(project_dir, f"inactive_state")
        if not os.path.exists(active_state_dir):
            os.makedirs(active_state_dir)  # Create the directory if it doesn't exist
        if not os.path.exists(inactive_state_dir):
            os.makedirs(inactive_state_dir)  # Create the directory if it doesn't exist

        for row in range(self.session_table.rowCount()):
            file_path = self.selected_files[row]
            if file_path in self.mne_data_objects:
                raw = self.mne_data_objects[file_path]

                # Get the parent filename (e.g., remove directory path)
                root, _ = os.path.splitext(file_path)
                parent_filename = str(os.path.basename(root)).replace('.', '_')

                # Extract first and last timestamps
                first_timestamp = raw.times[0]  # The first timestamp in the raw data
                last_timestamp = raw.times[-1]  # The last timestamp in the raw data


                # Get start and end times for the current interval (T1 to T2)
                start_time_item = self.session_table.item(row, 1)  # T1
                end_time_item = self.session_table.item(row, 2)  # T2

                # If both start and end times are available
                if start_time_item and end_time_item:
                    try:
                        start_time = float(start_time_item.text())
                        end_time = float(end_time_item.text())
                        # print(start_time)
                        # print(end_time)

                        # Validate times: Ensure they are within the range of raw data's timestamps
                        if start_time < 0 or end_time < 0 or start_time >= end_time:
                            raise ValueError("Start time must be less than end time and non-negative.")
                        if start_time < first_timestamp or end_time > last_timestamp:
                            raise ValueError(f"Times must be between {first_timestamp} and {last_timestamp}.")

                        # Remove decimal points from the start and end times
                        start_time_str = str(start_time).replace('.', '_') + 's'
                        end_time_str = str(end_time).replace('.', '_') + 's'

                        # Create a new filename for the saved cropped data
                        new_filename = f"{parent_filename}_T1_{start_time_str}_T2_{end_time_str}.edf"
                        # print(new_filename)
                        table_widget = self.session_table
                        num_cols = table_widget.columnCount()
                        # print(num_cols)
                        combo_box = table_widget.cellWidget(row, num_cols-1)
                        state = None
                        new_file_path = None
                        if combo_box and isinstance(combo_box, QComboBox):
                            state = combo_box.currentText()
                            # print(f'state: {state}')
                        if state == 'Active':
                            new_file_path = os.path.join(active_state_dir, new_filename)
                        elif state == 'Inactive':
                            new_file_path = os.path.join(inactive_state_dir, new_filename)
                        
                        

                        # Crop the raw data between start_time and end_time
                        start_sample = int(start_time * raw.info['sfreq'])  # Convert time to sample index
                        end_sample = int(end_time * raw.info['sfreq'])  # Convert time to sample index
                        cropped_data = raw.get_data(start=start_sample, stop=end_sample, verbose=0)

                        # Create a new Raw object for the cropped data
                        info = raw.info
                        cropped_raw = mne.io.RawArray(cropped_data, info, verbose=0)

                        # Export the cropped data as an EDF file
                        mne.export.export_raw(new_file_path, cropped_raw, fmt='edf', overwrite=True, verbose=0)

                    except ValueError as ve:
                        # Show warning for invalid time values and return to main screen
                        self.show_warning_message(f"Invalid time values for interval {interval_num + 1} in session {parent_filename}: {ve}")
                        return  # Exit the function, no crops saved
                    except Exception as e:
                        # Show general error message and return to main screen
                        self.show_warning_message(f"Error saving cropped data: {e}")
                        return  # Exit the function, no crops saved

    # Clear all fields after saving the data
    self.clear_all_fields()
    self.stacked_widget.setCurrentIndex(0)  # Switch back to the original page
    self.show_notification("Data saved successfully.")
