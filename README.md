# JCPZ-Digitalization

## Image Processing Application

A simple tkinter-based application for uploading, processing, and extracting data from multiple image files (PNG/JPG).

## Features

- **Multi-file upload**: Select multiple PNG/JPG images at once
- **Progress tracking**: Real-time progress bar and status updates
- **Mock processing**: Simulates image processing with customizable logic
- **CSV export**: Save extracted data to CSV format
- **Clean UI**: Simple, intuitive interface

## Requirements

- Python 3.6+
- tkinter (usually included with Python)

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Click "Select Images" to choose one or more PNG/JPG files

3. Click "Process Images" to process the selected files
   - Progress bar shows real-time processing status
   - Status messages display current file being processed

4. Click "Export to CSV" to save the extracted data
   - Choose a location and filename for your CSV file

## Code Structure

The application is built with a modular architecture, separating concerns for easy maintenance and extensibility:

### Modules

1. **`main.py`** - Application Controller/Orchestrator
   - Entry point for the application
   - Composes UI, processor, and exporter modules
   - Handles application state and coordinates between modules
   - Contains `ImageProcessorApp` controller class

2. **`ui.py`** - User Interface Module
   - All tkinter UI components and interactions
   - Contains `ImageProcessorUI` class
   - Handles file dialogs, buttons, progress bar, status updates
   - Exposes callbacks for controller to handle business logic

3. **`processor.py`** - Image Processing Module
   - Contains `ImageProcessor` class
   - Handles all image processing logic
   - Currently has mock implementation - **replace with your actual logic**
   - Includes image validation

4. **`exporter.py`** - CSV Export Module
   - Contains `CSVExporter` class
   - Handles data export to CSV format
   - Includes data validation before export

### Module Interaction

```
main.py (Controller)
    ├── Initializes ui.py (UI)
    ├── Initializes processor.py (Business Logic)
    ├── Initializes exporter.py (Data Export)
    └── Coordinates flow between modules
```

### Customization

**To add your own image processing logic**, modify `processor.py`:

```python
# In processor.py
def process_image(self, file_path: str) -> Dict:
    """Replace mock implementation with your actual logic."""
    
    # Example: Using PIL/Pillow
    from PIL import Image
    img = Image.open(file_path)
    width, height = img.size
    
    # Your processing code here
    # OCR, object detection, classification, etc.
    
    return {
        'filename': os.path.basename(file_path),
        'width': width,
        'height': height,
        'your_data_field': 'extracted_value',
        # Add more fields as needed
    }
```

## Adding Features

The modular structure makes it easy to extend:

1. **Add processing logic**: Modify `processor.py` → `ImageProcessor.process_image()`
2. **Add UI elements**: Modify `ui.py` → `ImageProcessorUI._create_ui()`
3. **Add export formats**: Create new exporter module (e.g., `json_exporter.py`)
4. **Add business logic**: Add methods to controller in `main.py`
5. **Change data structure**: Modify return value in `processor.py`