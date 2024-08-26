import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Conexión a MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)
cursor = conn.cursor()

# Crear base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")

# Seleccionar la base de datos
cursor.execute("USE CompanyData")

# Eliminar la tabla si existe
cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS EmployeePerformance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    departament VARCHAR(255),
    performance_score FLOAT,
    years_with_company INT,
    salary FLOAT
)
""")

conn.commit()

# Poblar la tabla con datos ficticios (usando datos generados previamente en un CSV)
data = pd.read_csv('data.csv')

# Verificar columnas del CSV
print(data.head())
print(data.columns)

# Insertar datos en la tabla
insert_query = """
INSERT INTO EmployeePerformance (employee_id, departament, performance_score, years_with_company, salary)
VALUES (%s, %s, %s, %s, %s)
"""

for _, row in data.iterrows():
    cursor.execute(insert_query, (
        row['employee_id'],
        row['departament'],
        row['performance_score'],
        row['years_with_company'],
        row['salary']
    ))

conn.commit()

# Extraer datos usando pandas
query = "SELECT * FROM EmployeePerformance"
df = pd.read_sql(query, conn)

# Calcular estadísticas
stats = df.groupby('departament').agg({
    'performance_score': ['mean', 'median', 'std'],
    'salary': ['mean', 'median', 'std'],
    'employee_id': 'count'
})

# Calcular correlaciones
correlation_years_performance = df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
correlation_salary_performance = df[['salary', 'performance_score']].corr().iloc[0, 1]

# Imprimir estadísticas y correlaciones
print("Estadísticas por departamento:\n", stats)
print("\nCorrelación entre años con la compañía y puntaje de rendimiento:", correlation_years_performance)
print("Correlación entre salario y puntaje de rendimiento:", correlation_salary_performance)

# Visualización de datos
# Histograma del performance_score por departament
departments = df['departament'].unique()
for dept in departments:
    plt.figure()
    df[df['departament'] == dept]['performance_score'].hist(bins=10)
    plt.title(f'Histograma del Performance Score - {dept}')
    plt.xlabel('Performance Score')
    plt.ylabel('Frecuencia')
    plt.show()  # Muestra el gráfico sin guardar

# Gráfico de dispersión de years_with_company vs. performance_score
plt.figure()
plt.scatter(df['years_with_company'], df['performance_score'])
plt.title('Años con la compañía vs. Puntaje de rendimiento')
plt.xlabel('Años con la compañía')
plt.ylabel('Puntaje de rendimiento')
plt.show()  # Muestra el gráfico sin guardar

# Gráfico de dispersión de salary vs. performance_score
plt.figure()
plt.scatter(df['salary'], df['performance_score'])
plt.title('Salario vs. Puntaje de rendimiento')
plt.xlabel('Salario')
plt.ylabel('Puntaje de rendimiento')
plt.show()  # Muestra el gráfico sin guardar

# Cerrar conexiones
cursor.close()
conn.close()
