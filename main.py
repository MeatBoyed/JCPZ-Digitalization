"""
Image Processing Application
Main entry point - composes UI, processor, and exporter modules.
"""

import tkinter as tk
import os
from typing import List, Dict

from ui import ImageProcessorUI
from processor import ImageProcessor
from exporter import CSVExporter


class ImageProcessorApp:
    """Application controller - orchestrates UI, processor, and exporter."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        
        # Initialize modules
        self.ui = ImageProcessorUI(root)
        self.processor = ImageProcessor()
        self.exporter = CSVExporter()
        
        # Application state
        self.selected_files: List[str] = []
        self.processed_data: List[Dict] = []
        
        # Connect UI callbacks to controller methods
        self.ui.on_select_files = self.handle_select_files
        self.ui.on_process_images = self.handle_process_images
        self.ui.on_export_csv = self.handle_export_csv
        
    def handle_select_files(self):
        """Handle file selection from UI."""
        files = self.ui.show_file_dialog()
        
        if files:
            # Validate files
            valid_files = [f for f in files if self.processor.validate_image_file(f)]
            
            if len(valid_files) != len(files):
                invalid_count = len(files) - len(valid_files)
                self.ui.show_warning(
                    "Invalid Files",
                    f"{invalid_count} file(s) were skipped (not valid image files)"
                )
            
            if valid_files:
                self.selected_files = valid_files
                self.ui.update_file_list(self.selected_files)
                self.ui.enable_button('process')
                self.ui.disable_button('export')
                self.processed_data = []
                self.ui.update_status(f"{len(self.selected_files)} files selected")
            else:
                self.ui.show_warning("No Valid Files", "No valid image files were selected.")
    
    def handle_process_images(self):
        """Handle image processing."""
        if not self.selected_files:
            self.ui.show_warning("No Files", "Please select files first.")
            return
        
        # Reset processed data
        self.processed_data = []
        
        # Setup progress bar
        self.ui.setup_progress_bar(len(self.selected_files))
        
        # Disable buttons during processing
        self.ui.disable_button('process')
        self.ui.disable_button('select')
        self.ui.disable_button('export')
        
        # Process each file
        for idx, file_path in enumerate(self.selected_files, 1):
            filename = os.path.basename(file_path)
            self.ui.update_status(f"Processing {idx}/{len(self.selected_files)}: {filename}")
            
            # Process the image using the processor module
            try:
                result = self.processor.process_image(file_path)
                self.processed_data.append(result)
            except Exception as e:
                self.ui.show_error("Processing Error", f"Error processing {filename}:\n{str(e)}")
                # Continue processing other files
            
            # Update progress
            self.ui.update_progress(idx)
        
        # Re-enable buttons
        self.ui.enable_button('select')
        self.ui.enable_button('process')
        
        # Enable export if we have processed data
        if self.processed_data:
            self.ui.enable_button('export')
            self.ui.update_status(f"Processing complete! {len(self.processed_data)} images processed.")
            self.ui.show_info("Success", f"Successfully processed {len(self.processed_data)} images!")
        else:
            self.ui.update_status("Processing failed - no data extracted.")
    
    def handle_export_csv(self):
        """Handle CSV export."""
        if not self.processed_data:
            self.ui.show_warning("No Data", "Please process images first.")
            return
        
        # Validate data before exporting
        if not self.exporter.validate_data(self.processed_data):
            self.ui.show_error("Invalid Data", "Processed data is not in valid format for export.")
            return
        
        # Show save dialog
        file_path = self.ui.show_save_dialog("processed_images.csv")
        
        if not file_path:
            return  # User cancelled
        
        try:
            # Export using the exporter module
            self.exporter.export_to_csv(self.processed_data, file_path)
            
            filename = os.path.basename(file_path)
            self.ui.update_status(f"Data exported to {filename}")
            self.ui.show_info("Success", f"Data successfully exported to:\n{file_path}")
            
        except Exception as e:
            self.ui.show_error("Export Error", f"Failed to export data:\n{str(e)}")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
