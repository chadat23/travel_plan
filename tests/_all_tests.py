import sys
import os

container_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'
))
sys.path.insert(0, container_folder)

# noinspection PyUnresolvedReferences
from tests.unit.viewmodels.test_travel_entry_viewmodel import *

# noinspection PyUnresolvedReferences
from tests.unit.services.test_car_services import *

# noinspection PyUnresolvedReferences
from tests.unit.services.test_color_services import *

# noinspection PyUnresolvedReferences
from tests.unit.services.test_location_services import *

# noinspection PyUnresolvedReferences
from tests.unit.services.test_patrol_services import *

# noinspection PyUnresolvedReferences
from tests.unit.services.test_user_services import *
