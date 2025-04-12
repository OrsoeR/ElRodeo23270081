import mysql.connector

def otorgar_privilegios():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="OrsoeR22"  # Deja el campo vacío si no tienes contraseña
            database="ElRodeo"
        )
        
        cursor = conexion.cursor()
        cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;")
        conexion.commit()
        print("Privilegios otorgados exitosamente")
        conexion.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Otorgar privilegios
otorgar_privilegios()
