import re
import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from .types import HardwareType

# Define Testing model class
class Hardware(Model):
    __table_name__ = 'hardware'
    hardware_id = columns.UUID(primary_key=True, default=uuid.uuid1())
    serial_number = columns.Text(primary_key=True, required=True)
    order_number = columns.Integer(primary_key=True, required=True)
    name = columns.Text(required=True)
    hardware_type = columns.Text(discriminator_column=True, required=True)
    mirror = columns.Text(required=True)


class AU(Hardware):
    __discriminator_value__ = HardwareType.AU.value
    variant = columns.Text(required=True)
    static_test_id = columns.UUID(default=uuid.uuid1())
    dynamic_test_id = columns.UUID(default=uuid.uuid1())

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
    variant = columns.Text(required=True)
    static_test = columns.UUID(default=uuid.uuid1())
    dynamic_test_id = columns.UUID(default=uuid.uuid1())
    size = columns.Text(required=True)

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
    size = columns.Text(required=True)
