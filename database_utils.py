from sqlalchemy import create_engine
from sqlalchemy import inspect
import tabula
import pandas as pd
import yaml

pd.set_option('display.max_columns', None)
class DatabaseConnector:
    def read_db_creds(self,yaml1):
        with open(yaml1, 'r') as stream:
            data = yaml.safe_load(stream)
        return data

    def init_db_engine(self, file):
        prime = self.read_db_creds(file)
        engine = create_engine(url=f"postgresql://{prime['RDS_USER']}:{prime['RDS_PASSWORD']}@{prime['RDS_HOST']}:{prime['RDS_PORT']}/{prime['RDS_DATABASE']}")
        return engine.connect()

    def list_db_tables(self, file):
        tables = self.init_db_engine(file)
        inspector = inspect(tables)
        table_names = inspector.get_table_names()
        return table_names
    
    def upload_to_db(self, df, upload_table):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'nazir40297'
        DATABASE = 'sales_data'
        PORT = 5432
        engine2 = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
        engine2.connect()
        df.to_sql(upload_table, engine2)

    def retrieve_pdf_data(self, link):
        df = tabula.read_pdf(link, pages = 'all')
        dfs = pd.concat(df, axis = 0, ignore_index = True)
        return dfs

