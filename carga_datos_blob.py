from azure.storage.blob import BlobServiceClient
import pandas as pd
import random
from datetime import datetime
import json
import logging

def cargar_config(path: str) -> str:
    try:
        with open(path, 'r') as f:
            config = json.load(f)
            return config["Values"]["connection_string"]
    except Exception as e:
        logging.info(f'Error al cargar la configuracion: {e}')

# Creacion del dataframe 
def creacion_dataframe(batch_size: int = 20)-> pd.DataFrame:
    data = {
        "cliente_id": [f"CLT{random.randint(1000, 9999)}" for _ in range(batch_size)],
        "telefono": [random.randint(600000000, 699999999) for _ in range(batch_size)],
        "codigo_pais": [random.choice(["ES", "US", "FR", "DE", "IT"]) for _ in range(batch_size)],
        "edad": [random.randint(18, 75) for _ in range(batch_size)],
        "fecha_creacion": datetime.now()
    }
    return pd.DataFrame(data)

def carga_blob(df: pd.DataFrame, CONN: str, container_name: str, blob_name: str)-> None:

    try:
    # Creamos el cliente de Azurite
        blob_service_client = BlobServiceClient.from_connection_string(CONN)

        # Creamos contenedor si no existe y el blob
        contenedor_cliente = blob_service_client.get_container_client(container_name)
        if not contenedor_cliente.exists():
            contenedor_cliente.create_container()
        blob_cliente = contenedor_cliente.get_blob_client(blob_name)

        # Cargamos el csv
        blob_cliente.upload_blob(df.to_csv(index=False))
        logging.info(f"carga del csv {blob_name} satisfactoria")

    except Exception as e:
        logging.info(f"Error al subir el archivo CSV: {e}")