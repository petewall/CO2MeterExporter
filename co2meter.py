"""
This is a mock version of the real CO2 Monitor object
https://github.com/vfilimonov/co2meter
This allows the service to be run without the real monitor for testing.
"""

import datetime as dt

def now():
    """
    Returns the current time
    """
    return dt.datetime.now().replace(microsecond=0)

class CO2monitor:
    """
    Mock of the real CO2 Monitor, with only the methods used defined
    """
    def __init__(self, bypass_decrypt=False, interface_path=None):
        """
        Pretend to be a constructor
        """

    def read_data(self, max_requests=50):
        """
        Return mock data
        """
        return now(), 500.0, 21.5
