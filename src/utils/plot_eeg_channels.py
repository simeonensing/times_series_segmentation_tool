import numpy as np
from scipy.signal import resample
import os
from PyQt5.QtWidgets import QDesktopWidget

def plot_eeg_channels(self):
    # Get the selected row in the session table
    selected_row = self.session_table.currentRow()
    
    # Ensure the selected row is valid (within the range of selected files)
    if selected_row < 0 or selected_row >= len(self.selected_files):
        return  # No valid selection, so return immediately

    # Get the file path corresponding to the selected row
    file_path = self.selected_files[selected_row]

    # Check if the file is in the mne_data_objects dictionary (contains EEG data)
    if file_path in self.mne_data_objects:
        raw = self.mne_data_objects[file_path]

        # List of emotive EEG channels to look for
        emotive_channels = ['AF3', 'AF4', 'F7', 'F8', 'F3', 'F4', 'FC5', 'FC6', 'T7', 'T8', 'P7', 'P8', 'O1', 'O2']
        
        # Pick EEG channels from the data
        raw.pick_types(eeg=True)
        eeg_channels = [ch for ch in raw.info['ch_names'] if ch in emotive_channels]

        # If no emotive channels are found, use all EEG channels
        if not eeg_channels:
            eeg_channels = raw.info['ch_names']

        # Clear the current plot
        self.ax.clear()


        # Resample data to 2^n samples for better resolution in time
        n = 10
        n_resampled = 2**n  # Hard-coded number of samples (2^n)
        times_resampled = np.linspace(raw.times[0], raw.times[-1], n_resampled)

        # Plot each EEG channel
        for ch in eeg_channels:
            try:
                # Get the data for the current EEG channel and resample it
                channel_data = raw.get_data(picks=[ch])[0]
                resampled_data = resample(channel_data, n_resampled)

                # Plot the resampled EEG data
                self.ax.plot(times_resampled, resampled_data, label=ch)
            except Exception as e:
                # Log any error that occurs during plotting for the current channel
                print(f"Error plotting data for channel {ch}: {e}")
                continue  # Continue with the next channel if there's an error

        # Add vertical lines to the plot based on interval values from the table
        for col in range(1, self.intervals_per_recording * 2 + 1):
            item = self.session_table.item(selected_row, col)
            if item and item.text():  # Ensure the item exists and contains text
                try:
                    interval_value = float(item.text())  # Try to convert the text to a float
                    self.ax.axvline(x=interval_value, color='r', linestyle='--', label=None)  # Add vertical line at interval
                except ValueError:
                    # Ignore invalid values (non-numeric text) by passing
                    pass

        # Set the plot title and axis labels
        self.ax.set_title(f"Time Series data {os.path.basename(file_path)}")
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude (uV)')
        
        # Display the legend for the channels
        self.ax.legend()

        # Update the canvas to reflect the new plot
        self.canvas.draw()
    else:
        # If the file is not found in mne_data_objects, show an error message
        self.show_warning_message("Selected file does not contain EEG data.")
