import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
from urllib.parse import quote_plus

# -------------------- LOGGING --------------------
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# -------------------- DB CONNECTION --------------------
def get_engine():
    username = "root"
    password = quote_plus("anish123")
    host = "localhost"
    port = "3306"
    database = "inventory"

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )
    return engine

# -------------------- INGEST FUNCTION --------------------
def ingest_db(df, table_name, engine):
    try:
        df.to_sql(
            table_name,
            con=engine,
            if_exists="replace",  # change to 'append' if needed
            index=False
        )
        logging.info(f"{table_name} loaded successfully.")
        print(f"{table_name} loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading {table_name}: {e}")
        print(f"Error loading {table_name}: {e}")

# -------------------- LOAD DATA --------------------
def load_raw_data():
    start = time.time()
    engine = get_engine()

    data_path = "data"

    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            try:
                file_path = os.path.join(data_path, file)
                df = pd.read_csv(file_path)

                table_name = file.replace(".csv", "")

                logging.info(f"Ingesting {file}")
                ingest_db(df, table_name, engine)

            except Exception as e:
                logging.error(f"Error processing {file}: {e}")

    end = time.time()
    total_time = (end - start) / 60

    logging.info("------------ Ingestion Complete ------------")
    logging.info(f"Total Time Taken: {total_time:.2f} minutes")

# -------------------- MAIN --------------------
if __name__ == "__main__":
    load_raw_data()