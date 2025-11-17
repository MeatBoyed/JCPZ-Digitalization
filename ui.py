"""
UI Module
Handles all user interface components and interactions.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Callable, Optional


class ImageProcessorUI:
    """Main UI class for the image processor application."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the UI.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Callbacks - to be set by the controller
        self.on_select_files: Optional[Callable] = None
        self.on_process_images: Optional[Callable] = None
        self.on_export_csv: Optional[Callable] = None
        
        # UI components (will be created in _create_ui)
        self.select_btn = None
        self.process_btn = None
        self.export_btn = None
        self.file_listbox = None
        self.file_count_label = None
        self.progress_bar = None
        self.status_label = None
        
        # Create the UI
        self._create_ui()
        
    def _create_ui(self):
        """Create all UI components."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Image Processing Tool",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.select_btn = ttk.Button(
            file_frame,
            text="Select Images",
            command=self._handle_select_files,
            width=20
        )
        self.select_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.file_count_label = ttk.Label(file_frame, text="No files selected")
        self.file_count_label.grid(row=0, column=1, sticky=tk.W)
        
        # File list
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Scrollbar for file list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(
            list_frame,
            height=8,
            yscrollcommand=scrollbar.set
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Processing section
        process_frame = ttk.LabelFrame(main_frame, text="Processing", padding="10")
        process_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.process_btn = ttk.Button(
            process_frame,
            text="Process Images",
            command=self._handle_process_images,
            width=20,
            state=tk.DISABLED
        )
        self.process_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.export_btn = ttk.Button(
            process_frame,
            text="Export to CSV",
            command=self._handle_export_csv,
            width=20,
            state=tk.DISABLED
        )
        self.export_btn.grid(row=0, column=1)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=600
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def _handle_select_files(self):
        """Handle the select files button click."""
        if self.on_select_files:
            self.on_select_files()
    
    def _handle_process_images(self):
        """Handle the process images button click."""
        if self.on_process_images:
            self.on_process_images()
    
    def _handle_export_csv(self):
        """Handle the export CSV button click."""
        if self.on_export_csv:
            self.on_export_csv()
    
    def show_file_dialog(self) -> List[str]:
        """Show file selection dialog and return selected files.
        
        Returns:
            List of selected file paths
        """
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg'),
            ('PNG files', '*.png'),
            ('JPG files', '*.jpg *.jpeg'),
            ('All files', '*.*')
        )
        
        files = filedialog.askopenfilenames(
            title='Select image files',
            filetypes=filetypes
        )
        
        return list(files) if files else []
    
    def show_save_dialog(self, default_filename: str = "output.csv") -> str:
        """Show save file dialog and return selected path.
        
        Args:
            default_filename: Default filename for the save dialog
            
        Returns:
            Selected file path or empty string if cancelled
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            title='Save CSV file',
            initialfile=default_filename
        )
        
        return file_path if file_path else ""
    
    def update_file_list(self, file_paths: List[str]):
        """Update the file listbox with selected files.
        
        Args:
            file_paths: List of file paths to display
        """
        self.file_listbox.delete(0, tk.END)
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, filename)
        
        count = len(file_paths)
        self.file_count_label.config(
            text=f"{count} file{'s' if count != 1 else ''} selected"
        )
    
    def update_status(self, message: str):
        """Update the status label.
        
        Args:
            message: Status message to display
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def setup_progress_bar(self, maximum: int):
        """Setup the progress bar with a maximum value.
        
        Args:
            maximum: Maximum value for the progress bar
        """
        self.progress_bar['maximum'] = maximum
        self.progress_bar['value'] = 0
    
    def update_progress(self, value: int):
        """Update the progress bar value.
        
        Args:
            value: Current progress value
        """
        self.progress_bar['value'] = value
        self.root.update_idletasks()
    
    def reset_progress(self):
        """Reset the progress bar to zero."""
        self.progress_bar['value'] = 0
    
    def enable_button(self, button_name: str):
        """Enable a specific button.
        
        Args:
            button_name: Name of button ('select', 'process', or 'export')
        """
        button_map = {
            'select': self.select_btn,
            'process': self.process_btn,
            'export': self.export_btn
        }
        
        if button_name in button_map:
            button_map[button_name].config(state=tk.NORMAL)
    
    def disable_button(self, button_name: str):
        """Disable a specific button.
        
        Args:
            button_name: Name of button ('select', 'process', or 'export')
        """
        button_map = {
            'select': self.select_btn,
            'process': self.process_btn,
            'export': self.export_btn
        }
        
        if button_name in button_map:
            button_map[button_name].config(state=tk.DISABLED)
    
    def show_info(self, title: str, message: str):
        """Show an info message box.
        
        Args:
            title: Message box title
            message: Message to display
        """
        messagebox.showinfo(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show a warning message box.
        
        Args:
            title: Message box title
            message: Message to display
        """
        messagebox.showwarning(title, message)
    
    def show_error(self, title: str, message: str):
        """Show an error message box.
        
        Args:
            title: Message box title
            message: Message to display
        """
        messagebox.showerror(title, message)
