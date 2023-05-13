from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

# Define Testing model class
class Test(Model):
    __table_name__ = 'testing'
    test_id = columns.UUID(primary_key=True)
    test_type = columns.Text(discriminator_column=True)
    test_success = columns.Boolean()
    test_pass = columns.Boolean()
    test_operator = columns.Text()
    test_date = columns.DateTime()
    tested_hardware = columns.UUID()
    result_file = columns.Text()

class StaticLoad(Test):
    __discriminator_value__ = 'static_load'

class Dynamic(Test):
    __discriminator_value__ = 'dynamic'
    pin_frequency = columns.Float()
    pin_damping = columns.Float()
    reaction_mass_frequency = columns.Float()
    reaction_mass_damping = columns.Float()
    axis = columns.Text()
