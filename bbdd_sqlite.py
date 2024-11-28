import sqlite3

def creacion_tabla() -> None:
    # Conectamos con la ddbb
    try:
        conn = sqlite3.connect("clientes_ddbb.db")

        # creamos un cursor
        cursor = conn.cursor()

        # Crear la tabla "clientes" si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                cliente_id TEXT PRIMARY KEY,
                telefono INTEGER NOT NULL,
                codigo_pais TEXT NOT NULL,
                edad INTEGER NOT NULL
            )
        ''')

        # Confirmar los cambios
        conn.commit()

        # Cerrar la conexión
        conn.close()

        print("Tabla creada exitosamente o ya existente.")
    
    except Exception as e:
        print(f"No se pudo crear la tabla: {e}")

creacion_tabla()