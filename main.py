import mysql.connector
import pandas as pd

# Conexión a MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='tu_usuario',
    password='tu_contraseña'
)
cursor = conn.cursor()

# Crear base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")

# Seleccionar la base de datos
cursor.execute("USE CompanyData")

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS EmployeePerformance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    department VARCHAR(255),
    performance_score FLOAT,
    years_with_company INT,
    salary FLOAT
)
""")
import pandas as pd

# Cargar datos ficticios desde un archivo CSV
data = pd.read_csv('employee_performance_data.csv')

# Insertar datos en la tabla
conn = mysql.connector.connect(
    host='localhost',
    user='tu_usuario',
    password='tu_contraseña',
    database='CompanyData'
)
cursor = conn.cursor()

for _, row in data.iterrows():
    cursor.execute("""
    INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
    VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cursor.close()
conn.close()
