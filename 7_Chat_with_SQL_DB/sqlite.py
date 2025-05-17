import sqlite3

# Connect to sqllite
connection = sqlite3.connect("student.db")

# Create cursor object to insert record, create teable
cursor = connection.cursor()

# Create the table
table_info = """
create table STUDENT (NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

# Insert records
cursor.execute("""insert into STUDENT values('Mayura', 'Data Science', 'A', 90)""")
cursor.execute("""insert into STUDENT values('Krish', 'Data Science', 'B', 100)""")
cursor.execute("""insert into STUDENT values('Mukesh', 'Data Science', 'A', 86)""")
cursor.execute("""insert into STUDENT values('Jacob', 'Devops', 'A', 50)""")
cursor.execute("""insert into STUDENT values('Dipesh', 'Devops', 'A', 35)""")

# Display all the records
print("The inserted records are")
data = cursor.execute("""select * from STUDENT""")

for row in data:
    print(row)

# Commit your changes in the database
connection.commit()
connection.close()