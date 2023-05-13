import re

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from .types import HardwareType

# Define Testing model class
class Hardware(Model):
    __table_name__ = 'hardware'
    hardware_id = columns.UUID(primary_key=True)
    serial_number = columns.Text(primary_key=True)
    order_number = columns.Integer(primary_key=True)
    name = columns.Text()
    hardware_type = columns.Text(discriminator_column=True)
    mirror = columns.Text()


class AU(Hardware):
    __discriminator_value__ = HardwareType.AU.value
    variant = columns.Text()
    static_test_id = columns.UUID()
    dynamic_test_id = columns.UUID()

    def variant_number(self) -> int:
        '''
        Extract variante number from member string

        Returns
        -------
        - `int`: Variante number
        '''
        return int(re.search(r'\D+(\d+)-', self.variant).group(1))

class MGC(Hardware):
    __discriminator_value__ = HardwareType.MGC.value
    variant = columns.Text()
    static_test = columns.UUID()
    dynamic_test_id = columns.UUID()
    size = columns.Text()

    def variant_number(self) -> int:
        '''
        Extract variante number from member string

        Returns
        -------
        - `int`: Variante number
        '''
        return int(re.search(r'\D+(\d+)-', self.variant).group(1))

class VCM(Hardware):
    __discriminator_value__ = HardwareType.VCM.value
    dynamic_test_id = columns.UUID()
    size = columns.Text()
