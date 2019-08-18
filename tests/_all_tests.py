import sys
import os

container_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
))
sys.path.insert(0, container_folder)

# noinspection PyUnresolvedReferences
from tests.unit.services.location_services_tests import *

# noinspection PyUnresolvedReferences
from tests.unit.services.user_services_tests import *
