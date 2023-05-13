import uuid
from datetime import datetime

from cassandra.cqlengine import columns, connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model

# Define Testing model class
class Test(Model):
    __table_name__ = 'testing'
    test_id = columns.UUID(primary_key=True)
    test_type = columns.Text(discriminator_column=True)
    test_success = columns.Boolean()
    test_date = columns.DateTime()

class Hardware(Model):
    __table_name__ = 'hardware'
    serial_number = columns.Text(primary_key=True)
    order_number = columns.Integer(primary_key=True)
    hardware_type = columns.Text(discriminator_column=True)
    project_name = columns.Text()