#%%
# Imports
import keyring as kr
import pandas as pd
import time

import sqlalchemy as sa
from sqlalchemy.engine import create_engine
import cx_Oracle

from warnings import filterwarnings
filterwarnings("ignore")

from umbitlib.helpers import convert_seconds
from umbitlib.helpers import generate_sqlalchemy_dtypes

#%%
# Security
class SecurityHandler:
    """
    A class for handling security operations for various services.

    This class provides methods for initializing security instances and accessing service credentials.

    Args:
        service_name (str): The desired service name for security operations.
        NOTE: Valid service names: {'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'}

    Raises:
        ValueError: If the provided service_name is not one of the valid options.

    Example:
        orc = SecurityHandler('oracle')
    """

    _VALID_SERVICE_NAMES = {'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'}

    def __init__(self, service_name):
        """
        Initializes a security instance

        Args:
        service_name (str): The desired service_name for security operations.

        Raises:
        ValueError: If the provided service_name is not one of the valid options.

        Example:
        orc = SecurityHandler('oracle')
        """

        self._service_name = service_name.lower()

        if self._service_name not in self._VALID_SERVICE_NAMES:
            raise ValueError(f"service_name must be one of {self._VALID_SERVICE_NAMES}")

        self._security_obj = kr.get_credential(service_name=self._service_name, username=None)
        self.username = self._security_obj.username
        self._password = self._security_obj.password

    # Use of the @property decorator with no accompanying setter method ensures that the service_name cannot be set 
    # to another value after initialization. (Unless the user calls _service_name which is technically private)
    @property
    def service_name(self):
        """
        str: The selected service_name for security operations.
        """
        return self._service_name
    

# Engine Handler
class DatabaseEngine(SecurityHandler):
    """
    A class for managing database connections with various engines.

    This class inherits from SecurityHandler and provides methods to create database connections
    for different database engines, such as Oracle and PostgreSQL.

    Args:
        service_name (str): The desired service name for security operations, inherited from SecurityHandler.

    Example:
        engine = DatabaseEngine('oracle')
    """

    def __init__(self, service_name):
        """
        Initializes a database engine instance and establishes a connection to the specified database.

        Args:
            service_name (str): The desired service name for security operations, inherited from SecurityHandler.

        Example:
            engine = DatabaseEngine('oracle')
        """
        super().__init__(service_name)

        try:
            import sys
            sys.path.append("\\\\ad.utah.edu\\uuhc\\umb2\\shared\\Analytics Team\\Security")
            import db_conn_vars

        except ModuleNotFoundError as e:
            print(f"Security file not found: {e}")
            pass

        if self.service_name in ['oracle', 'oracle_serv_acc']:
            self._dsn = db_conn_vars.ODB_NAME
            self.engine = sa.create_engine(f"oracle+cx_oracle://{self.username}:{self._password}@{self._dsn}", echo=False)  # Set echo=True for debugging
        elif self.service_name in ['postgres_dev', 'postgres_prod', 'postgres_serv_acc']:
            if self.service_name == 'postgres_dev':
                self._db = db_conn_vars.PG_DEV_DB
                self._host = db_conn_vars.PG_DEV_HOST
                self._port = db_conn_vars.PG_DEV_PORT
            elif self.service_name == 'postgres_prod':
                self._db = db_conn_vars.PG_PROD_DB
                self._host = db_conn_vars.PG_PROD_HOST
                self._port = db_conn_vars.PG_PROD_PORT

            self.engine = create_engine(f"postgresql://{self.username}:{self._password}@{self._host}:{self._port}/{self._db}")


# SQL Handler
class SqlHandler(DatabaseEngine):
    """
    A class for executing SQL statements against databases.

    This class inherits from DatabaseEngine and provides methods for executing SQL queries on the database
    and uploading DataFrames to the database tables making a usable connection and other standard SQL functions.

    Args:
        service_name (str): The desired service name for security operations, inherited from DatabaseEngine.

    Example:
        sql_handler = SqlHandler('oracle')
    """

    def __init__(self, service_name):
        """
        Initializes an SQL handler instance.

        Args:
            service_name (str): The desired service name for security operations, inherited from DatabaseEngine.

        Example:
            sql_handler = SqlHandler('oracle')
        """
        super().__init__(service_name)


    def connect(self, conn_success_msg: bool = True):
        """
        Creates a connection to a database.  Requires that the programmer closes the connection in a separate statment.

        Args:
            conn_success_msg (bool): Determines if connection successful message will print out or not. Default = True

        Returns:
            A connection to the specified database
        
        Example:
            sql_handler = SqlHandler('oracle)
            sql_conn = sql_handler.connect()
                //your code here//
            sql_conn.close()
        """
        try:
            sql_connection = self.engine.connect()
            if conn_success_msg:
                print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful. Use of this function requires manual closing of this connection upon end of use.")
            return sql_connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None


    def query(self, sql_query, conn_success_msg: bool = True, sql_success_msg: bool = True):
        """
        Execute a SQL query on the database and return the result as a DataFrame.

        Args:
            sql_query (str): The SQL query to execute.
            conn_success_msg (bool): Turns on or off the output of the connection success message (default is True)
            query_success_msg (bool): Turns on or off the output of the query success message and runtime (default is True)

        Returns:
            pandas.DataFrame: A DataFrame containing the query result.

        Example:
            sql_handler = SqlHandler('oracle')
            df = sql_handler.query('SELECT * FROM your_table')
        """
        try:
            with self.engine.connect() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful")

                tic = time.perf_counter()
                result_df = pd.read_sql(sql_query, con=connection)
                toc = time.perf_counter() 

                if sql_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass
            
            return result_df
        except Exception as e:
            print(f"Error executing query against {self.service_name}: {e}." 
                  f"Check or set your keyring credentials and/or SQLAlchemy engine")
            return None
        
    
    def upload_df(self, dataframe, table_name, if_exists='replace', index=False, auto_dtype=True, dtype=None, conn_success_msg: bool = True, sql_success_msg: bool = True):
        """
        Upload a DataFrame to the database.

        Args:
            dataframe (pandas.DataFrame): The DataFrame to upload.
            table_name (str): The name of the table to upload the DataFrame to.
            if_exists (str, optional): How to behave if the table already exists. Defaults to 'replace'. ('replace', 'append', 'fail')
            index (bool, optional): Whether to include the DataFrame index as a column. Defaults to False.
            auto_dtype (bool, optional): Automatically generate SQLAlchemy data types based on DataFrame. Defaults to True.
            dtype (dict, optional): Data type mapping to apply to columns when creating the table. Defaults to None.
            conn_success_msg (bool): Turns on or off the output of the connection success message (default is True)
            query_success_msg (bool): Turns on or off the output of the query success message and runtime (default is True)

        Example:
            sql_handler = SqlHandler('oracle')
            sql_handler.upload_df(your_dataframe, 'target_table')

            Example without auto_dtype
            my_dtypes = {'state_c': VARCHAR(length=3),
                        'name': VARCHAR(length=30),
                        'title': VARCHAR(length=30),
                        'abbr': VARCHAR(length=12),
                        'internal_id': VARCHAR(length=3)}
            sql_handler.upload_df(your_dataframe, 'target_table' auto_dtype=False, dtype=my_dtypes)
        """
        try:

            if auto_dtype:
                    pg_dtype = generate_sqlalchemy_dtypes(dataframe)
            else:
                pg_dtype = dtype
            
            # Upload DataFrame to Oracle
            with self.engine.begin() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.service_name} for user {self.username} via Keyring: Successful")

                tic = time.perf_counter()   
                dataframe.to_sql(table_name, connection, if_exists=if_exists, index=index, dtype=pg_dtype)
                toc = time.perf_counter() 

                if sql_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Sql executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass
                
            print(f"DataFrame uploaded successfully to {self.service_name}.")
            
        except Exception as e:
            print(f"Error uploading DataFrame to {self.service_name}:", str(e))



###############################
# To be deprecated - Start
###############################
#%%
# Security
class SecurityIo:
    """
    A class to manage security-related operations based on specified destinations.

    This class provides a way to interact with security objects based on predefined destinations.

    Parameters:
    dest (str): The desired destination for security operations. Must be one of:
                'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'.

    Attributes:
    VALID_DESTINATIONS (set): A set of valid destination options.

    Properties:
    destination (str): The selected destination for security operations.

    Raises:
    ValueError: If the provided destination is not one of the valid options.

    """

    VALID_DESTINATIONS = {'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'}

    def __init__(self, dest: str):
        """
        Initializes a SecurityIo instance.

        Args:
        dest (str): The desired destination for security operations.

        Raises:
        ValueError: If the provided destination is not one of the valid options.
        """

        self._destination = dest.lower()

        if self._destination not in self.VALID_DESTINATIONS:
            raise ValueError(f"destination must be one of {self.VALID_DESTINATIONS}")

        self._security_obj = kr.get_credential(service_name=self._destination, username=None)
        self.username = self._security_obj.username
        self._password = self._security_obj.password

    # Use of the @property decorator with no accompanying setter method ensures that the destination cannot be set 
    # to another value after initialization. (Unless the user calls _destination which is technically private)
    @property
    def destination(self):
        """
        str: The selected destination for security operations.
        """
        return self._destination


#%%
# Oracle
class Oracle(SecurityIo):
    """
    A class to manage Oracle database operations securely using inherited credentials. Defaults to oracle rather than oracle_serv_acc

    This class extends the SecurityIo class and provides methods to interact with an Oracle database securely.

    Parameters:
    destination (str): The desired destination for security operations. Must be one of:
                      'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'.

    Attributes:
    engine (sqlalchemy.engine.base.Engine): An SQLAlchemy engine for connecting to the Oracle database.

    Methods:
    connect() -> cx_Oracle.connection:
        Establishes a connection to the target database.  This connection must be closed manually by the programmer in a later call.

    query(sql_query: str) -> pandas.DataFrame:
        Execute a SQL query on the Oracle database and return the result as a DataFrame.

    """
    def __init__(self, destination = 'oracle'):
        super().__init__(destination)

        try:
            import sys
            sys.path.append("\\\\ad.utah.edu\\uuhc\\umb2\\shared\\Analytics Team\\Security")
            import db_conn_vars

        except Exception as e:
            print(f"{e}: Security file not found.")
            pass       

        # DB Params
        self.dsn = db_conn_vars.ODB_NAME

        # Connection
        self.engine = sa.create_engine(f"oracle+cx_oracle://{self.username}:{self._password}@{self.dsn}", echo=False)  # Set echo=True for debugging


    def connect(self, conn_success_msg: bool = True):
        """
        Creates a connection to an Oracle database.  Requires that the programmer closes the connection in a separate statment.

        Example:
        oracle = Oracle()
        oracle_conn = oracle.connect()
            //your code here//
        oracle_conn.close()
        """
        oracle_connection = self.engine.connect()
        if conn_success_msg:
            print(f"Connection to {self.destination} for user {self.username} via Keyring: Successful. Use of this function requires manual closing of this connection upon end of use.")
        return oracle_connection
    

    def query(self, sql_query: str, conn_success_msg: bool = True, query_success_msg: bool = True) -> pd.DataFrame:
        """
        Execute a SQL query on the Oracle database and return the result as a DataFrame. This function closes the connection after execution.

        Args:
        sql_query (str): The SQL query to execute.

        Returns:
        pandas.DataFrame: A DataFrame containing the query result.

        Example:
        oracle = Oracle()
        df = oracle.query(your_sql_str_here)
        """
        try:
            with self.engine.connect() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.destination} for user {self.username} via Keyring: Successful")                

                tic = time.perf_counter()
                df = pd.read_sql(sql_query, con=connection)            
                toc = time.perf_counter()            

                if query_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass
                return df
            
        except Exception as e:
            print(f"Error executing query: {e}. Check or set your keyring credentials and SQLAlchemy engine")
            return None

#%%
class Postgres(SecurityIo):
    """
    A class to manage Postgres database operations securely using inherited credentials. Defaults to postgres_dev rather than postgers_prod or postgres_serv_acc

    This class extends the SecurityIo class and provides methods to interact with an Postgres database securely.

    Parameters:
    destination (str): The desired destination for security operations. Must be one of:
                      'oracle', 'oracle_serv_acc', 'postgres_dev', 'postgres_prod', 'postgres_serv_acc'.

    Attributes:
    engine (sqlalchemy.engine.base.Engine): An SQLAlchemy engine for connecting to the Postgres database.

    Methods:
    connect():
        Establishes a connection to the target database.  This connection must be closed manually by the programmer in a later call.

    query(sql_query: str) -> pandas.DataFrame:
        Execute a SQL query on the Postgres database and return the result as a DataFrame.

    """
    def __init__(self, destination = 'postgres_dev'):
        super().__init__(destination)
       
        try:
            import sys
            sys.path.append("\\\\ad.utah.edu\\uuhc\\umb2\\shared\\Analytics Team\\Security")
            import db_conn_vars

        except Exception as e:
            print(f"{e}: Security file not found.")
            pass
       
        if self.destination == 'postgres_dev':
            self.db = db_conn_vars.PG_DEV_DB
            self.host = db_conn_vars.PG_DEV_HOST
            self.port = db_conn_vars.PG_DEV_PORT
        elif self.destination == 'postgres_prod':
            self.db = db_conn_vars.PG_PROD_DB
            self.host = db_conn_vars.PG_PROD_HOST
            self.port = db_conn_vars.PG_PROD_PORT

        self.engine = create_engine(f"postgresql://{self.username}:{self._password}@{self.host}:{self.port}/{self.db}")


    def connect(self, conn_success_msg: bool = True):
        """
        Creates a connection to a Postgres database.  Requires that the programmer closes the connection in a separate statment.

        Example:
        postgres = Postgres()
        postgres_conn = postgres.connect()
            //your code here//
        postgres_conn.close()
        """
        postgres_connection = self.engine.connect()
        if conn_success_msg:
            print(f"Connection to {self.destination} for user {self.username} via Keyring: Successful. Use of this function requires manual closing of this connection upon end of use.")
        return postgres_connection


    def query(self, sql_query: str, conn_success_msg: bool = True, query_success_msg: bool = True) -> pd.DataFrame:
        """
        Execute a SQL query on the Postgres database and return the result as a DataFrame. This function closes the connection after execution.

        Args:
        sql_query (str): The SQL query to execute.

        Returns:
        pandas.DataFrame: A DataFrame containing the query result.

        Example:
        postgres = Postgres()
        df = postgres.query(your_sql_str_here)
        """
        try:       
            with self.engine.connect() as connection:
                if conn_success_msg:
                    print(f"Connection to {self.destination} for user {self.username} via Keyring: Successful") 
                
                tic = time.perf_counter()
                df = pd.read_sql(sql_query, con=connection)           
                toc = time.perf_counter()
                
                if query_success_msg:
                    try:
                        elapsed_time = toc - tic
                        days, hours, minutes, seconds = convert_seconds(elapsed_time)
                        print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                    except:
                        print("Problem getting elapsed time")
                        pass
                return df
            
        except Exception as e:
            print(f"Error executing query: {e} Check or set your keyring credentials and SQLAlchemy engine")
            return None

###############################
# To be deprecated - End
###############################