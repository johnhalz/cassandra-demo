import os
import logging
from typing import Union, List, Dict

import pandas as pd

from cassandra.cluster import Cluster
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.policies import RoundRobinPolicy

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'
logging.getLogger('cassandra').setLevel(logging.WARNING)

class CassandraInterface:
    def __init__(self, host: Union[str, List[str]], port: int, keyspace: str = None,
                 connect_immediately: bool = True) -> None:
        # Create cluster
        if isinstance(host, str):
            host = [host]

        self.cluster = Cluster(
            host,
            port=port,
            protocol_version=5,
            load_balancing_policy=RoundRobinPolicy()
        )

        # Connect (if required)
        self.session = None
        if connect_immediately:
            self.connect(keyspace)

    def connect(self, start_keyspace: str = None) -> None:
        '''
        Connect to cassandra database

        Parameters
        ----------
        - `start_keyspace` (`str`): Starting keyspace name
        '''
        if not self.connected:
            self.session = self.cluster.connect(start_keyspace)

        logging.info(f'Successfully connected.')

    def disconnect(self) -> None:
        '''
        Disconnect from cassandra database
        '''
        if self.connected:
            self.session.shutdown()
            self.cluster.shutdown()

        logging.info(f'Successfully disconnected.')

    @property
    def connected(self) -> bool:
        '''
        Check whether interface instance is connected to database or not

        Returns
        -------
        - `bool`: If interface is connected or not
        '''
        return self.session

    def list_keyspaces(self) -> List[str]:
        '''
        Get a list of keyspaces from connected cluster

        Returns
        -------
        - `List[str]`: List of keyspace names
        '''
        # Retrieve the list of keyspaces
        query = "DESCRIBE KEYSPACES;"
        keyspaces = self.session.execute(query)

        # Print the names of the keyspaces
        return list(keyspace.keyspace_name for keyspace in keyspaces)

    def create_keyspace(self, keyspace_name: str) -> None:
        '''
        Create a new keyspace

        Parameters
        ----------
        - `keyspace_name` (`str`): Name of keyspace
        '''
        replication_opts = {
            'class': 'SimpleStrategy',
            'replication_factor': 1  # Change this value based on your replication requirements
        }

        # Log message
        logging.debug(f'Creating keyspace {keyspace_name} (if not exists).')

        # Attempt to create keyspace
        query = f'CREATE KEYSPACE IF NOT EXISTS {keyspace_name} WITH REPLICATION = {replication_opts};'
        try:
            self.session.execute(query=query)

        except Exception as exc:
            raise Exception(
                f'Unable to create keyspace {keyspace_name}'
            ) from exc

    def create_table(self, keyspace: str = None, table_model: Model = None) -> None:
        '''
        Create a table from a given table model (very similar to a dataclass)

        Parameters
        ----------
        - `keyspace` (`str`): Keyspace name (default: `None`)
        - `table_model` (`Model`): Subclass of cassandra-driver Model class
        '''
        if not hasattr(table_model, '__table_name__'):
            raise AttributeError('The variable __table_name__ needs to be set.')

        if keyspace is not None:
            self.session.set_keyspace(keyspace)

        # Create connection
        connection.set_session(self.session)

        sync_table(table_model)
        logging.info(f'Created table {table_model.__table_name__} in keyspace {keyspace}.')

    def delete_row(self, keyspace_name: str, table_name: str,
                   primary_key_values: Union[str, Dict[str, str]]) -> None:
        '''
        Delete row from a table based on the primary key(s).

        The primary key values can be either a string (if the table has a single primary key
        column), or a dictionary of column names (as keys) and column values (as values) in
        the dictionary.

        Parameters
        ----------
        - `keyspace_name` (`str`): Name of keyspace
        - `table_name` (`str`): Name of table
        - `primary_key_values` (`Union[str, Dict[str, str]]`): Primary key value(s)
        '''
        if isinstance(primary_key_values, str):
            delete_query = f"DELETE FROM {keyspace_name}.{table_name} WHERE primary_key_column = %s"
            self.session.execute(delete_query, [primary_key_values])

        elif isinstance(primary_key_values, dict):
            # Create delete query from dictionary values
            delete_query = f'DELETE FROM {keyspace_name}.{table_name} WHERE '
            for primary_column in primary_key_values.keys():
                delete_query += f'{primary_column} = %s AND '

            # Remove the trailing 'AND' and add a semicolon at end of query
            delete_query = delete_query[:-5] + ';'

            # Execute query
            self.session.execute(delete_query, list(primary_key_values.values()))

    def table_to_df(self, keyspace_name: str, table_name: str) -> pd.DataFrame:
        '''
        Return a cassandra table to a pandas dataframe

        Parameters
        ----------
        - `keyspace_name` (`str`): Name of keyspace
        - `table_name` (`str`): Name of table

        Returns
        -------
        - `pd.DataFrame`: Pandas dataframe
        '''
        query = f'SELECT * FROM {keyspace_name}.{table_name}'
        result_set = self.session.execute(query)

        # Convert the query result to a pandas DataFrame
        data = list(result_set)
        return pd.DataFrame(data)
