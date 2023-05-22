'''Cassandra interface'''
import logging
from datetime import datetime

import pandas as pd

from cassandra_interface import CassandraInterface
from cassandra_interface.models import AU, HardwareType, Mirror

def setup_logger():
    '''Setup logger for app'''
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
        format='[%(asctime)s] %(levelname)-9s %(message)s'
    )

def main():
    # Connect to cassandra cluster
    cas_session = CassandraInterface(host='0.0.0.0', port=9042)

    # Create keyspace (if not already existing)
    new_keyspace = 'au5000'
    cas_session.create_keyspace(keyspace_name=new_keyspace)

    # Create table in keyspace
    cas_session.create_table(keyspace=new_keyspace, table_model=AU)

    # Create element in new table
    _ = AU.create(
        serial_number='11-AU-3475-4538',
        order_number=258234,
        name='AU-M730',
        hardware_type=HardwareType.AU.value,
        mirror=Mirror.UNKNOWN.value,
        variant='AU5k-V03',
        created_on=datetime.now()
    )

    # Query oldest element in table
    au_table = cas_session.table_to_df()
    oldest_au_index = au_table['created_on'].idxmin()
    oldest_au = au_table.loc[oldest_row_index]



    # Delete element from table
    AU(hardware_id=oldest_au.hardware_id, serial_number=oldest_au.serial_number, order_number=oldest_au.order_number).timeout(None).delete()
    # cas_session.delete_row(
    #     keyspace_name='au5000',
    #     table_name='hardware',
    #     primary_key_values={
    #         'hardware_id':oldest_au.hardware_id,
    #         'serial_number':oldest_au.serial_number,
    #         'order_number':oldest_au.order_number
    #     }
    # )

    # Close connection to database
    cas_session.disconnect()

if __name__ == '__main__':
    setup_logger()
    main()
