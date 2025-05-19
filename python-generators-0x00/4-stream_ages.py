import mysql.connector
from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for (age,) in cursor:
            yield float(age)
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error streaming ages: {err}")

def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()