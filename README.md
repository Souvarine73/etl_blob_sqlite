# Azure Function ETL: Gestión de Clientes

Este proyecto implementa un proceso ETL (Extract, Transform, Load) utilizando **Azure Functions** para gestionar datos de clientes. El flujo de trabajo incluye la generación de datos sintéticos, almacenamiento en blobs de Azure Storage, consolidación de los datos en un archivo maestro y su ingestión en una base de datos SQLite.

## Características principales

- **Generación de datos sintéticos:** Crea un conjunto de datos aleatorio con información de clientes (ID, teléfono, código de país, edad y fecha de creación).
- **Almacenamiento en Azure Blob Storage:** Los datos se cargan como archivos CSV en un contenedor de Azure Blob Storage.
- **Consolidación de datos:** Descarga y combina todos los blobs del contenedor, eliminando duplicados según la última fecha de creación.
- **Ingestión en SQLite:** Los datos consolidados se almacenan en una base de datos SQLite, actualizando los registros existentes en caso de conflicto.

---

## Estructura del Proyecto

### 1. **Archivo `bbdd_sqlite.py`**
Gestiona la base de datos SQLite:
- Crea la tabla `clientes` si no existe, con las siguientes columnas:
  - `cliente_id`: Identificador único del cliente.
  - `telefono`: Número de teléfono.
  - `codigo_pais`: Código del país.
  - `edad`: Edad del cliente.
  - `fecha_creacion`: Marca de tiempo de la creación del registro.

### 2. **Archivo `carga_datos_blob.py`**
Funciones para la generación y carga de datos en Azure Blob Storage:
- **`creacion_dataframe(batch_size)`**: Genera un DataFrame con datos sintéticos.
- **`cargar_config(path)`**: Lee la configuración desde un archivo `local.settings.json`.
- **`carga_blob(df, CONN, container_name, blob_name)`**: Carga un DataFrame como archivo CSV en Azure Blob Storage.

### 3. **Archivo `function_app.py`**
Define la Azure Function que orquesta el flujo ETL:
- **Extracción:** Genera datos sintéticos y los almacena como blobs.
- **Transformación:** Descarga y combina todos los blobs en un único DataFrame, asegurando que solo se mantenga el registro más reciente por cliente.
- **Carga:** Inserta o actualiza los registros en la base de datos SQLite usando un comando `UPSERT`.

---

## Requisitos

- **Python** >= 3.8
- **Dependencias:** Ver archivo `requirements.txt`

### Configuración del entorno

1. **Archivo `local.settings.json`:**
   Este archivo contiene la configuración necesaria para la conexión a Azure Blob Storage. Ejemplo:

   ```json
   {
       "IsEncrypted": false,
       "Values": {
           "AzureWebJobsStorage": "",
           "FUNCTIONS_WORKER_RUNTIME": "python",
           "connection_string": "DefaultEndpointsProtocol=https;AccountName=<ACCOUNT_NAME>;AccountKey=<ACCOUNT_KEY>;EndpointSuffix=core.windows.net"
       }
   }
