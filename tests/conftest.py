"""Pytest configuration: mock co2meter hardware before main is imported."""
import sys
from unittest.mock import MagicMock

mock_monitor = MagicMock()
mock_monitor.info = {
    'manufacturer': 'Test Manufacturer',
    'product_name': 'Test Product',
    'serial_no': '12345',
}
mock_monitor.read_data.return_value = ('2024-01-01 12:00:00', 850, 22.5)

sys.modules['co2meter'] = MagicMock(CO2monitor=MagicMock(return_value=mock_monitor))
