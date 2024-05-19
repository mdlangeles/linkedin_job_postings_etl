import json
import pandas as pd
import sys
import os
import psycopg2
sys.path.append(os.path.abspath("/opt/airflow/"))

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


api_csv = './Data/jobs1.csv'


with open('Credentials/keys_e.json', 'r') as json_file:
    data = json.load(json_file)
    user = data["user"]
    password = data["password"]
    port= data["port"]
    server = data["server"]
    db = data["db"]

db_connection = f"postgresql://{user}:{password}@{server}:{port}/{db}"
engine=create_engine(db_connection)
Base = declarative_base()


def engine_creation():
    engine = create_engine(db_connection)
    return engine

def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_data_warehouse():
    create_company_dimension = '''
    CREATE TABLE IF NOT EXISTS dim_company(
        company_id FLOAT PRIMARY KEY,
        industry_id BIGINT,
        industry_name VARCHAR(255),
        job_id BIGINT
    );
    '''

    create_industry_dimension = '''
    CREATE TABLE IF NOT EXISTS dim_industry(
        industry_id BIGINT PRIMARY KEY,
        industry_name VARCHAR(255),
        job_id BIGINT
    );
    '''

    create_salary_facts = '''
    CREATE TABLE IF NOT EXISTS fact_salary(
        job_id BIGINT PRIMARY KEY,
        annual_salary FLOAT,
        compensation_type VARCHAR(255),
        currency VARCHAR(255)
    );
    '''

    create_jobs_dimension = '''
    CREATE TABLE IF NOT EXISTS dim_jobs(
        job_id BIGINT PRIMARY KEY,
        job_posting_url VARCHAR(255),
        location VARCHAR(255),
        sponsored BOOLEAN,
        title VARCHAR(255)
    );
    '''


    engine = create_engine(db_connection)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.execute(create_salary_facts)
        session.execute(create_jobs_dimension)
        session.execute(create_company_dimension)
        session.execute(create_industry_dimension)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()

def insert_data_warehouse(df, table):
    df = df.astype(str)
    column_names = df.columns.tolist()
    insert_salary_query = f"""
        INSERT INTO {table}({", ".join(column_names)})
        VALUES ({", ".join([f":{col}" for col in column_names])})
        ON CONFLICT (job_id) DO UPDATE SET
        currency = EXCLUDED.currency,
        compensation_type = EXCLUDED.compensation_type,
        annual_salary = EXCLUDED.annual_salary;
    """
    # insert_company_query = f"""
    #     INSERT INTO {table}({", ".join(column_names)})
    #     VALUES ({", ".join([f":{col}" for col in column_names])})
    #     ON CONFLICT (company_id) DO UPDATE SET
    #     company_id = EXCLUDED.company_id,
    #     industry_id = EXCLUDED.industry_id,
    #     industry_name = EXCLUDED.industry_name,
    # """
    engine = create_engine(db_connection)  # Asegúrate de que db_connection es la cadena de conexión a tu base de datos
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        for index, row in df.iterrows():
            values = {col: val for col, val in zip(column_names, row)}
            session.execute(insert_salary_query, values)
        session.commit()
        print(f"Data has been loaded into: {table}")

        # for index, row in df.iterrows():
        #     values = {col: val for col, val in zip(column_names, row)}
        #     session.execute(insert_company_query, values)
        # session.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        session.close()
    



def create_api_table(engine):

    class api(Base):
        _tablename_ = 'API_transform'
        id = Column(Integer, primary_key=True, autoincrement=True)
        work_year = Column(Integer, nullable=False)
        experience_level = Column(String(100), nullable=False)
        employment_type = Column(String(100), nullable=False)
        job_title = Column(String(100), nullable=False)
        salary = Column(Integer, nullable=False)
        salary_currency = Column(String(100), nullable=False)
        salary_in_usd = Column(Integer, nullable=False)
        employee_residence = Column(String(100), nullable=False)
        company_location = Column(String(100), nullable=False)
        company_size = Column(String(100), nullable=False)

    Base.metadata.create_all(engine)
    api._table_

def insert_merge():
    df_api = pd.read_csv(api_csv)
    df_api.to_sql('API_transform', engine, if_exists='replace', index=False)

def finish_engine(engine):
    engine.dispose()