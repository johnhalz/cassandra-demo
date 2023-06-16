import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

# Define Testing model class
class ProductionStep(Model):
    __table_name__ = 'production'
    id = columns.UUID(primary_key=True, default=uuid.uuid1())
    stand = columns.Text(discriminator_column=True)
    start_date = columns.DateTime()
    test_success = columns.Boolean()
    progress = columns.Double()
    test_operator = columns.Text()
    tested_hardware = columns.UUID()
    result_summary = columns.Text()

class StaticLoad(ProductionStep):
    __discriminator_value__ = 'static_load'

class Dynamic(ProductionStep):
    __discriminator_value__ = 'dynamic'
    pin_frequency = columns.Float()
    pin_damping = columns.Float()
    reaction_mass_frequency = columns.Float()
    reaction_mass_damping = columns.Float()
    axis = columns.Text()
