import logging
import azure.functions as func
from carga_datos_blob import *
import io
import sqlite3

app = func.FunctionApp()

@app.timer_trigger(schedule="*/20 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def etl_blob_sqlddbb(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    # Conexion a Azurite y campos para crear el blob
    config_file = 'local.settings.json'
    container_name = "clientes"
    blob_name = f"clientes_{str(datetime.now().strftime('%Y%m%d_%H%M%S'))}.csv"

    # Creamos el string de conexin
    CONNECTION_STRING = cargar_config(config_file)


    # Generamos un nuevo blob
    df = creacion_dataframe()
    carga_blob(df, CONNECTION_STRING, container_name, blob_name)

    # Descargamos los blobs y los ingestamos en sqlite
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    # Conexión con el contenedor
    contenedor_cliente = blob_service_client.get_container_client(container_name)

    # Lista donde almacenaremos los nombres de los blobs
    dataframes = []

    # Iteramos sobre los blobs
    for blob in contenedor_cliente.list_blob_names():
        logging.info(f"Descargando blob: {blob}")
        blob_cliente = contenedor_cliente.get_blob_client(blob)

        # Descargamos el contenido del blob
        blob_stream = blob_cliente.download_blob().readall()

        # Convertimos a un df
        df = pd.read_csv(io.StringIO(blob_stream.decode("utf-8")))
        dataframes.append(df)

    if dataframes:
        # Concatenamos los dataframes
        df_final = pd.concat(dataframes, ignore_index=True)
        # En el caso dee que hubiese mas de un registro para un cliente nos quedamos con el que tenga la fecha mas actual
        df_final["fecha_creacion"] = pd.to_datetime(df_final["fecha_creacion"])
        df_final = df_final.loc[df_final.groupby('cliente_id')['fecha_creacion'].idxmax()].reset_index(drop=True)
        df_final["fecha_creacion"] = df_final["fecha_creacion"].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
        logging.info("Todos los blobs concatenados")

    else:
        logging.info("No se encontraron blobs en el contenedor")
    
    try:
    # conectamos con la bbdd
        conn = sqlite3.connect("clientes_ddbb.db")

        # Creamos el cursor
        cursor = conn.cursor()

        # upsert
        sql = '''
            INSERT INTO clientes (cliente_id, telefono, codigo_pais, edad, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(cliente_id)
            DO UPDATE SET
                telefono = excluded.telefono,
                codigo_pais = excluded.codigo_pais,
                edad = excluded.edad,
                fecha_creacion = excluded.fecha_creacion
        '''
        # Crear una lista de valores en formato (?,?,?,?)
        values = [
            (row['cliente_id'], row['telefono'], row['codigo_pais'], row['edad'], row['fecha_creacion'])
            for _, row in df_final.iterrows()
        ]

        # Ingestamos los datos en la BBDD
        
        logging.info("iniciando ingesta...")
        cursor.executemany(sql, values)
        conn.commit()
        conn.close()
        logging.info(f"Procesados {len(values)} registros con éxito.")
        
    except Exception as e:
        logging.info(f"error en la ejecucion: {e}")