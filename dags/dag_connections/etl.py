import pandas as pd
import json
import logging
import psycopg2
import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Date, CHAR
sys.path.append(os.path.abspath("/opt/airflow/dags/dag_connections/"))
# sys.path.append(os.path.abspath("/home/emmanuel/Escritorio/linkedin_job_postings_etl/"))
# sys.path.append(os.path.abspath("/home/emmanuel/Escritorio/linkedin_job_postings_etl/dags/dag_connections"))
# sys.path.append(os.path.abspath("/opt/airflow/dags/dag_connections/"))
# from transformations.transformations import delete_column, delete_duplicated_id, duration_transformation, cat_genre, drop_transformation, fill_na_merge, fill_na_merge1, category_na, nominee, delete_artist, title
# from transformations.transformations import drop_columns, parenthesis_transformation, fill_nulls_first, fill_nulls_arts, fill_nulls_worker, drop_nulls, lower_case, rename_column
from dag_connections.db import engine_creation, finish_engine
# from driveconf import upload_file



# def read_linkedin_data():
    
#     df_linkedin = pd.read_excel("./Data/job_postulations.xlsx")
#     logging.info("Excel read successfully")
#     logging.info(f"Columns are: %s" , df_linkedin.head())

#     return df_linkedin.to_json(orient='records')

    
# def transform(**kwargs):
#     logging.info("The CSV has started transformation process")

#     ti = kwargs['ti']
#     data_strg = ti.xcom_pull(task_ids='read_csv_task')
#     json_data = json.loads(data_strg)
#     df_spotify = pd.json_normalize(data=json_data)

#     logging.info("df is type: %s", type(df_spotify))
    
#     #Column Unnamed Deleted
#     df_spotify = delete_column(df_spotify)
#     logging.info("Colunmn deleted %s", df_spotify.head(5)) 

#     #Delete duplicated track_id
#     df_spotify=  delete_duplicated_id(df_spotify)
#     logging.info("Duplicated deleted %s", df_spotify.head(5)) 

#     df_spotify= duration_transformation(df_spotify)
#     logging.info("Duration transformation done %s", df_spotify.head(5))

#     df_spotify= cat_genre(df_spotify)
#     logging.info("The Genre was categorized %s", df_spotify.head(5))

#     df_spotify=drop_transformation(df_spotify)
#     logging.info("The columns was deleted perfectly %s", df_spotify.head(5))

#     logging.info("The CSV has ended transformation process")

#     return df_spotify.to_json(orient='records')
    
    
def read_linkedin():
    query = "SELECT * FROM LinkedinSalary"
    
    engine = engine_creation()
    
    df_linkedin = pd.read_sql(query, engine)

    #Cerramos la conexion a la db
    finish_engine(engine)

    logging.info("database read succesfully")
    logging.info('data extracted is %s', df_linkedin.head(5))
    return df_linkedin.to_json(orient='records')



# def merge(**kwargs):
#     ti = kwargs["ti"]

#     logging.info( f"Spotify has started the merge proccess")
#     data_strg = ti.xcom_pull(task_ids="transform_csv_task")
#     json_data = json.loads(data_strg)
#     df_spotify = pd.json_normalize(data=json_data)

#     logging.info( f"Grammys has started the merge proccess")
#     data_strg = ti.xcom_pull(task_ids="transform_db_task")
#     json_data = json.loads(data_strg)
#     grammys_df = pd.json_normalize(data=json_data)

#     df_merge = df_spotify.merge(grammys_df, how='left', left_on='track_name', right_on='nominee')
#     df_merge = fill_na_merge(df_merge)
#     df_merge= fill_na_merge1(df_merge)
#     df_merge=delete_artist(df_merge)
#     df_merge=category_na(df_merge)
#     df_merge=nominee(df_merge)
#     df_merge=title(df_merge)
#     logging.info( f"THe merge is Done")
#     logging.info(f"The dimension is: {df_merge.shape}")
#     logging.info(f"the columns are: {df_merge.columns}")



#     return df_merge.to_json(orient='records')


# def load(**kwargs):
#     logging.info("Load proccess is started")
#     ti = kwargs["ti"]
#     data_strg = ti.xcom_pull(task_ids="merge_task")
#     json_data = json.loads(data_strg)
#     df_load = pd.json_normalize(data=json_data)
#     engine = engine_creation()

#     df_load.to_sql('merge', engine, if_exists='replace', index=False)

#     #Close the connection to the DB
#     finish_engine(engine)
#     df_load.to_csv("merge.csv", index=False)
#     logging.info( f"Merge is ready")

#     return df_load.to_json(orient='records')



# def store(**kwargs):
#     logging.info("The Store Process has Started")
#     ti = kwargs["ti"]
#     data_strg = ti.xcom_pull(task_ids="load_task")
#     json_data = json.loads(data_strg)
#     df_store = pd.json_normalize(data=json_data)

#     upload_file("merge.csv","11xQ7d8wvT5wcHQToTfNAmsGUvceG_6cX")    
#     logging.info( f"THe Data is Uploaded In GoogleDrive")