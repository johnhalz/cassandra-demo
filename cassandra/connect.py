'''Cassandra interface'''
import logging

from cassandra.cluster import Cluster, Session

def setup_logger():
    '''Setup logger for app'''
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
        format='[%(asctime)s] %(levelname)-9s %(message)s'
    )

class CassandraInterface:
    def __init__(self) -> None:
        pass

def create_keyspace(session: Session, keyspace_name: str):
    '''
    Create a new keyspace
    '''
    replication_opts = {
        'class': 'SimpleStrategy',
        'replication_factor': 1  # Change this value based on your replication requirements
    }

    query = f'CREATE KEYSPACE IF NOT EXISTS {keyspace_name} WITH REPLICATION = {replication_opts};'
    try:
        session.execute(query=query)
    except Exception as exc:
        raise Exception(
            f'Unable to create keyspace {keyspace_name}'
        ) from exc

def create_table(session: Session, keyspace: str, table_name: str) -> None:
    '''
    Create table in keyspace
    '''
    # Set keyspace
    session.set_keyspace(keyspace)

    # Create table
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id UUID PRIMARY KEY,
            name TEXT;
        )
    """
    session.execute(create_table_query)

def add_columns_to_table(session: Session, keyspace: str,
                         table_name: str, columns: list[str], types: list[str]) -> None:
    '''
    Alter table to add columns with specified type
    '''
    if len(columns) != len(types):
        raise ValueError(
            f'Length of column names and column data types must be the same! ({len(columns)} vs. {len(types)}).'
        )

    session.set_keyspace(keyspace)

    # alter_table_query = f'ALTER TABLE {table_name}'
    # for column, type in zip(columns, types):
    #     alter_table_query += f'\nADD {column} {type.upper()},'

    alter_table_query = """
        ALTER TABLE my_table
        ADD age INT,
        ADD email TEXT;
    """

    session.execute(alter_table_query)

def main():
    # Connect to cassandra cluster
    cluster = Cluster(['0.0.0.0'], port=9042)
    session = cluster.connect('au5000')

    # Create keyspace
    create_keyspace(session, 'au5000')

    # Create table and add columns
    # create_table(session, keyspace='au5000', table_name='au_dynamic_tests')

    # Close connection to database
    session.shutdown()
    cluster.shutdown()

if __name__ == '__main__':
    main()
