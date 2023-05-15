'''Cassandra interface'''
import logging

from cassandra_interface import CassandraInterface
from cassandra_interface.models import AU, HardwareType, Mirror, Hardware

def setup_logger():
    '''Setup logger for app'''
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
        format='[%(asctime)s] %(levelname)-9s %(message)s'
    )

def main():
    # Connect to cassandra cluster
    cas_session = CassandraInterface(host='0.0.0.0', port=9042, keyspace='au5000')

    # List keyspaces
    cas_session.create_table(keyspace='au5000', table_model=AU)

    # Close connection to database
    cas_session.disconnect()

if __name__ == '__main__':
    setup_logger()
    main()
