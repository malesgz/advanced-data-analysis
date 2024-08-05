import mysql.connector
import pandas as pd

# Conexión a MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='',
    password=''
)
cursor = conn.cursor()

# Crea base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")

# Selecciona la base de datos
cursor.execute("USE CompanyData")

# Crea tabla
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

# Carga datos ficticios desde un archivo CSV
data = pd.read_csv('employee_performance_data.csv')

# Inserta datos en la tabla
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
