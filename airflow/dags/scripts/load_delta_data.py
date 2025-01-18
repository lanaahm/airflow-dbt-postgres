import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from airflow.hooks.postgres_hook import PostgresHook

def get_sqlalchemy_connection():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn_dwh')
    conn_uri = postgres_hook.get_uri()
    engine = create_engine(conn_uri)
    return engine

def get_last_loaded_timestamp():
    """
    Retrieve the last loaded timestamp from the database.
    If no data exists, return datetime.min.
    """
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn_dwh')
    sql = "SELECT MAX(updated_at) FROM orders;"
    result = postgres_hook.get_first(sql)
    last_loaded = result[0] if result and result[0] else None
    return last_loaded if last_loaded else datetime.min

def load_data_to_staging(path_dirr):
    """
    Load delta data newer than the last loaded timestamp into staging tables.
    """
    last_loaded = get_last_loaded_timestamp()
    engine = get_sqlalchemy_connection()
    conn = engine.connect()

    for root, _, files in os.walk(path_dirr):
        for file in files:
            if file.endswith('.csv'):
                table = file.split('.')[0]
                file_path = os.path.join(root, file)

                folder_date = root.split('/')[-2]  # Example: 20250115
                folder_hour = root.split('/')[-1]  # Example: 14
                file_timestamp = datetime.strptime(f"{folder_date}{folder_hour}", "%Y%m%d%H")

                # Skip if the folder timestamp is older than or equal to last_loaded
                if file_timestamp <= last_loaded:
                    continue

                # Load data into DataFrame
                df = pd.read_csv(file_path)
                if df.empty:
                    print(f"No data in {file_path}, skipping.")
                    continue

                # Get existing data from staging for comparison
                existing_data_query = f"SELECT * FROM {table}"
                existing_data = pd.read_sql(existing_data_query, conn)
                
                # Identify new and updated records
                if not existing_data.empty:
                    merged = df.merge(existing_data, on='id', how='left', suffixes=('', '_existing'))
                    # Extract new and updated data
                    original_columns = [col for col in merged.columns if not col.endswith('_existing')]
                    new_data = merged[merged['updated_at_existing'].isna()][original_columns]
                    updated_data = merged[(~merged['updated_at_existing'].isna()) & 
                                          (merged['updated_at'] != merged['updated_at_existing'])][original_columns]
                else:
                    new_data = df
                    updated_data = pd.DataFrame()

                # Bulk insert new data
                if not new_data.empty:
                    new_data.to_sql(f'{table}', engine, index=False, if_exists='append', method='multi')
                    print(f"Inserted {len(new_data)} new rows into {table}.")

                # Update existing records
                if not updated_data.empty:
                    for _, row in updated_data.iterrows():
                        update_query = f"""
                        UPDATE {table}
                        SET {', '.join([f"{col} = %s" for col in df.columns if col != 'id'])}
                        WHERE id = %s
                        """
                        update_params = tuple(row[col] for col in df.columns if col != 'id') + (row['id'],)
                        conn.execute(update_query, update_params)
                    print(f"Updated {len(updated_data)} rows in {table}.")

    conn.close()
