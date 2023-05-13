import logging

from cassandra.cluster import Cluster

class CassandraInterface:
    def __init__(self, host: str, port: int, keyspace: str = None,
                 connect_immediately: bool = True) -> None:
        self.cluster = Cluster([host], port=port)
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

    def disconnect(self) -> None:
        '''
        Disconnect from cassandra database
        '''
        if self.connected:
            self.session.shutdown()
            self.cluster.shutdown()

    @property
    def connected(self) -> bool:
        '''
        Check whether interface instance is connected to database or not

        Returns
        -------
        - `bool`: If interface is connected or not
        '''
        return self.session


    def create_keyspace(self, keyspace_name: str):
        '''
        Create a new keyspace
        '''
        replication_opts = {
            'class': 'SimpleStrategy',
            'replication_factor': 1  # Change this value based on your replication requirements
        }

        query = f'CREATE KEYSPACE IF NOT EXISTS {keyspace_name} WITH REPLICATION = {replication_opts};'
        try:
            self.session.execute(query=query)
            self.cluster.refresh_keyspace_metadata()
        except Exception as exc:
            raise Exception(
                f'Unable to create keyspace {keyspace_name}'
            ) from exc

    def create_table(self, keyspace: str = None, table_name: str = None) -> None:
        '''
        Create table in keyspace
        '''
        # Verify table name
        if table_name is None:
            raise ValueError('A table name must be provided!')

        # Set keyspace
        if keyspace is not None:
            self.session.set_keyspace(keyspace)

        # Create table
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name}"""
        self.session.execute(create_table_query)
        self.cluster.refresh_table_metadata()

    def add_columns_to_table(self, keyspace: str,
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
