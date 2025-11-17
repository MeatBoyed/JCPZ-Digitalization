"""
CSV Exporter Module
Handles exporting processed data to CSV format.
"""

import csv
from typing import List, Dict


class CSVExporter:
    """Handles CSV export operations."""
    
    def __init__(self):
        """Initialize the CSV exporter."""
        pass
    
    def export_to_csv(self, data: List[Dict], file_path: str) -> None:
        """Export data to a CSV file.
        
        Args:
            data: List of dictionaries containing the data to export
            file_path: Path where the CSV file should be saved
            
        Raises:
            ValueError: If data is empty
            IOError: If file cannot be written
        """
        if not data:
            raise ValueError("No data to export")
        
        # Write data to CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data)
    
    def validate_data(self, data: List[Dict]) -> bool:
        """Validate that data is in correct format for export.
        
        Args:
            data: List of dictionaries to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if not data:
            return False
        
        if not isinstance(data, list):
            return False
        
        # Check that all items are dictionaries
        if not all(isinstance(item, dict) for item in data):
            return False
        
        # Check that all dictionaries have the same keys
        if len(data) > 1:
            first_keys = set(data[0].keys())
            if not all(set(item.keys()) == first_keys for item in data[1:]):
                return False
        
        return True
