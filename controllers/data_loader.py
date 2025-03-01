from PyQt6.QtWidgets import QFileDialog
from controllers.ui_controller import UIController

def load_data_file(window):
    """
    Load data from a file and update the application state.
    
    Args:
        window: The main application window
    """
    path, _ = QFileDialog.getOpenFileName(
        window,
        'Select the File',
        '',
        'Text Files (*.txt);;All Files (*)'
    )

    if path:
        data = window.data_model.load_data(path)

        if data is not None and not data.empty:
            window.data = data
            window.data_processor.add_data(data)
            
            # enable UI
            window.bins_spinbox.setEnabled(True)
            window.plot_button.setEnabled(True)
            window.standardize_button.setEnabled(True)
            window.log_button.setEnabled(True)
            window.shift_spinbox.setEnabled(True)
            window.shift_button.setEnabled(True)
            window.data_version_combo.setEnabled(True)
            
            # update data versions
            window.ui_controller.update_data_versions()
            
            # set default bins
            from controllers.plot_controller import set_default_bins
            window.bins_spinbox.setValue(set_default_bins(window.data))
            
            print(f'File {path} selected successfully')
        else:
            print(f'Failed to load file {path} or file is empty')