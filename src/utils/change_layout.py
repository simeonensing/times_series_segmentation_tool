import os
import mne

def change_layout(self):
    project_dir = self.project_dir_input.text()
    if not project_dir:
        self.show_warning_message("Please enter a project directory name.")
        return
    
        # Create the project directory
    project_dir = os.path.join(os.getcwd(), project_dir)

    for file in self.selected_files:
        try:
            raw = None
            if file.endswith('.fif'):
                raw = mne.io.read_raw_fif(file, preload=True, verbose = 0)
            elif file.endswith('.edf'):
                raw = mne.io.read_raw_edf(file, preload=True, verbose = 0)
            elif file.endswith('.bdf'):
                raw = mne.io.read_raw_bdf(file, preload=True, verbose = 0)
            elif file.endswith('.set'):
                raw = mne.io.read_raw_eeglab(file, preload=True, verbose = 0)
            if raw:
                self.mne_data_objects[file] = raw
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            self.show_warning_message(f"Error loading EEG data from '{file}': {str(e)}")

    self.update_session_table()
    self.stacked_widget.setCurrentIndex(1)
    self.save_button.setEnabled(0)

    if self.session_table.rowCount() > 0:
        self.session_table.selectRow(0)
        self.plot_eeg_channels()
