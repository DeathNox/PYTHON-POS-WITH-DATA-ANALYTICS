import mysql.connector

def get_employee_sales_performance():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "pos_new"
        )
        cursor = connection.cursor()

        # Query to fetch employee sales performance
        query = """
        SELECT u.first_name AS cashier_name, SUM(s.sub_total) AS total_sales
        FROM tbl_sales s
        JOIN tbl_users u ON s.cashier_name = u.user_id
        GROUP BY u.first_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
