from . import direct
from . import lookup
from . import datalake
from . import utils
from .datalake.base import query
from .datalake._data_objects import CSVFile, TempTable


import sys
import importlib

# importlib package ranamed after Python 3.8.0
if sys.version_info >= (3, 8, 0):
    from importlib.metadata import version
else:
    from importlib_metadata import version

__version__ = version(__name__)
