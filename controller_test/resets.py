import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path)

import money_controller as mc


@pytest.fixture(autouse=True)
def reset_funcs():
    supcheck_input = mc.check_input
    supnum_less_than = mc.num_less_than
    supcheck_type_input = mc.check_type_input
    supstop = mc.stop

    yield

    mc.check_input = supcheck_input
    mc.num_less_than = supnum_less_than
    mc.check_type_input = supcheck_type_input
    mc.stop = supstop
