import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

class DatabaseManager:
    def __init__(self, host, user, password, db_name):
        self.conn = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.cursor.execute(f"USE {db_name}")
    
    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS EmployeePerformance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT,
                departament VARCHAR(255),
                performance_score FLOAT,
                years_with_company INT,
                salary FLOAT
            )
        """)
        self.conn.commit()

    def insert_data(self, data):
        insert_query = """
            INSERT INTO EmployeePerformance (employee_id, departament, performance_score, years_with_company, salary)
            VALUES (%s, %s, %s, %s, %s)
        """
        for _, row in data.iterrows():
            self.cursor.execute(insert_query, (
                row['employee_id'],
                row['departament'],
                row['performance_score'],
                row['years_with_company'],
                row['salary']
            ))
        self.conn.commit()

    def fetch_data(self, query):
        return pd.read_sql(query, self.conn)
    
    def close(self):
        self.cursor.close()
        self.conn.close()

class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def calculate_statistics(self):
        return self.df.groupby('departament').agg({
            'performance_score': ['mean', 'median', 'std'],
            'salary': ['mean', 'median', 'std'],
            'employee_id': 'count'
        })

    def calculate_correlations(self):
        correlation_years_performance = self.df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
        correlation_salary_performance = self.df[['salary', 'performance_score']].corr().iloc[0, 1]
        return correlation_years_performance, correlation_salary_performance

    def display_statistics(self, stats):
        print("Estadísticas por departamento:\n", stats)

    def display_correlations(self, correlation_years_performance, correlation_salary_performance):
        print("\nCorrelación entre años con la compañía y puntaje de rendimiento:", correlation_years_performance)
        print("Correlación entre salario y puntaje de rendimiento:", correlation_salary_performance)

class DataVisualizer:
    def __init__(self, df):
        self.df = df

    def plot_histogram(self):
        departments = self.df['departament'].unique()
        for dept in departments:
            plt.figure()
            self.df[self.df['departament'] == dept]['performance_score'].hist(bins=10)
            plt.title(f'Histograma del Performance Score - {dept}')
            plt.xlabel('Performance Score')
            plt.ylabel('Frecuencia')
            plt.show()

    def plot_scatter(self, x, y, x_label, y_label, title):
        plt.figure()
        plt.scatter(self.df[x], self.df[y])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

def main():
    db_manager = DatabaseManager(host='localhost', user='root', password='', db_name='CompanyData')
    db_manager.create_table()

    data = pd.read_csv('data.csv')
    db_manager.insert_data(data)

    df = db_manager.fetch_data("SELECT * FROM EmployeePerformance")

    analyzer = DataAnalyzer(df)
    stats = analyzer.calculate_statistics()
    analyzer.display_statistics(stats)

    correlation_years_performance, correlation_salary_performance = analyzer.calculate_correlations()
    analyzer.display_correlations(correlation_years_performance, correlation_salary_performance)

    visualizer = DataVisualizer(df)
    visualizer.plot_histogram()
    visualizer.plot_scatter('years_with_company', 'performance_score', 'Años con la compañía', 'Puntaje de rendimiento', 'Años con la compañía vs. Puntaje de rendimiento')
    visualizer.plot_scatter('salary', 'performance_score', 'Salario', 'Puntaje de rendimiento', 'Salario vs. Puntaje de rendimiento')

    db_manager.close()

if __name__ == "__main__":
    main()