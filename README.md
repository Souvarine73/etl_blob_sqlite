# Azure Function ETL: Gestión de Clientes

Este proyecto implementa un flujo ETL (Extract, Transform, Load) utilizando **Azure Functions** para gestionar datos de clientes. El flujo incluye la generación de datos sintéticos, almacenamiento en Azure Blob Storage, consolidación de información y su ingestión en una base de datos SQLite.

## 🚀 Características principales

- **Generación de datos sintéticos**: Creación de registros ficticios con ID, teléfono, país, edad y fecha.
- **Almacenamiento en Azure Blob Storage**: Almacena los datos generados como archivos CSV en un contenedor.
- **Consolidación de datos**: Descarga y combina los datos de múltiples blobs, eliminando duplicados basados en la fecha de creación más reciente.
- **Ingestión en SQLite**: Inserta o actualiza los datos procesados en una base de datos SQLite local.

---

## 📂 Estructura del Proyecto

### `bbdd_sqlite.py`
Gestiona la base de datos SQLite:
- Crea la tabla `clientes` con las siguientes columnas:
  - `cliente_id`: Identificador único.
  - `telefono`: Número de teléfono.
  - `codigo_pais`: Código del país.
  - `edad`: Edad del cliente.
  - `fecha_creacion`: Marca de tiempo del registro.

### `carga_datos_blob.py`
Funciones para trabajar con datos y blobs:
- **`creacion_dataframe(batch_size=20)`**: Genera un DataFrame con datos sintéticos.
- **`cargar_config(path)`**: Carga la cadena de conexión desde `local.settings.json`.
- **`carga_blob(df, CONN, container_name, blob_name)`**: Sube un DataFrame como CSV a Azure Blob Storage.

### `function_app.py`
Orquesta el flujo ETL:
- Genera datos y los sube como blobs.
- Descarga y consolida blobs en un único DataFrame.
- Inserta o actualiza los datos consolidados en SQLite.

---

## 🛠️ Requisitos

- **Python**: >= 3.8
- **Dependencias**: Ver archivo `requirements.txt`.

---

## ⚙️ Configuración del entorno

1. Crea un archivo `local.settings.json` con tu cadena de conexión de Azure Blob Storage:

   ```json
   {
       "IsEncrypted": false,
       "Values": {
           "AzureWebJobsStorage": "",
           "FUNCTIONS_WORKER_RUNTIME": "python",
           "connection_string": "DefaultEndpointsProtocol=https;AccountName=<ACCOUNT_NAME>;AccountKey=<ACCOUNT_KEY>;EndpointSuffix=core.windows.net"
       }
   }

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt

## 🚀 Cómo usar

1. Prepara el entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows

2. Inicializa la base de datos SQLite:
   ```bash
   python bbdd_sqlite.py

3. Ejecuta la Azure Function:
   ```bash
   func start

4. Resultados:
   - Los datos consolidados se guardarán en clientes_ddbb.db.
   - Los logs detallarán el progreso de la ejecución.

## 📝 Notas
   - Azure Blob Storage: El contenedor clientes se creará automáticamente si no existe.
   - Ejecución periódica: El disparador cron ejecuta la función cada 20 segundos (schedule="*/20 * * * * *"), feel free to play around con el tiempo.
   - Manejo de conflictos: Los registros existentes en SQLite se actualizan si cambian los datos.