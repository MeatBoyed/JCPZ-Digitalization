# Project Structure

```
JCPZ-Digitalization/
├── main.py           # Application orchestrator/controller
├── ui.py             # User interface (tkinter components)
├── processor.py      # Image processing logic
├── exporter.py       # CSV export functionality
└── README.md         # Documentation
```

## Module Dependencies

```
main.py
├── imports ui.ImageProcessorUI
├── imports processor.ImageProcessor
└── imports exporter.CSVExporter

ui.py
└── (no internal dependencies, just tkinter)

processor.py
└── (no internal dependencies)

exporter.py
└── (no internal dependencies)
```

## Data Flow

1. **User clicks "Select Images"**
   ```
   UI → main.handle_select_files() → processor.validate_image_file() → UI.update_file_list()
   ```

2. **User clicks "Process Images"**
   ```
   UI → main.handle_process_images() → processor.process_image() → UI.update_progress()
   ```

3. **User clicks "Export to CSV"**
   ```
   UI → main.handle_export_csv() → exporter.validate_data() → exporter.export_to_csv()
   ```

## Key Benefits of This Structure

✅ **Separation of Concerns**: UI, business logic, and data export are independent
✅ **Easy Testing**: Each module can be tested in isolation
✅ **Maintainable**: Changes to UI don't affect processing logic and vice versa
✅ **Extensible**: Easy to add new features or swap implementations
✅ **Readable**: Clear responsibility for each module

## Where to Make Changes

- **Change how images are processed**: Edit `processor.py`
- **Change the UI layout/design**: Edit `ui.py`
- **Add new export formats**: Create new file like `json_exporter.py`
- **Add new workflows**: Edit `main.py` controller methods
- **Change data validation**: Edit `exporter.py` or `processor.py`
