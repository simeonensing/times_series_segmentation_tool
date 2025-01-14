import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import ( 
    change_layout,
    initialise_gui,
    basic_functions,
    update_session_table,
    plot_eeg_channels,
    save_cropped_data,
)
from PyQt5.QtWidgets import QWidget

class ts_segmentation_GUI(QWidget):
    def __init__(self):
        super().__init__()
        initialise_gui.initialise(self)

    def change_layout(self):
        change_layout.change_layout(self)

    def show_warning_message(self, message):
        basic_functions.show_warning_message(self, message)

    def open_file_dialog(self):
        basic_functions.open_file_dialog(self)

    def remove_selected_files(self):
        basic_functions.remove_selected_files(self)

    def remove_all_files(self):
        basic_functions.remove_all_files(self)

    def update_remove_button_state(self):
        basic_functions.update_remove_button_state(self)

    def update_next_button_state(self):
        basic_functions.update_next_button_state(self)

    def update_session_table(self):
        update_session_table.update_session_table(self)

    def go_back(self):
        basic_functions.go_back(self)

    def show_notification(self, message):
        basic_functions.show_notification(self, message)

    def setup_item_changed_signals(self):
        basic_functions.setup_item_changed_signals(self)

    def setup_item_clicked_signals(self):
        basic_functions.setup_item_clicked_signals(self)

    def plot_eeg_channels(self):
        plot_eeg_channels.plot_eeg_channels(self)

    def save_cropped_data_as_edf(self):
        save_cropped_data.save_cropped_data_as_edf(self)

    def clear_all_fields(self):
        basic_functions.clear_all_fields(self)

    def highlight_invalid_times(self,item):
        basic_functions.highlight_invalid_times(self,item)
    
    def clear_highlight(self,item):
        basic_functions.clear_highlight(self,item)
    
    def set_save_off(self,item):
        basic_functions.set_save_off(self,item)
    
    def row_selection_changed(self):
        basic_functions.row_selection_changed(self)