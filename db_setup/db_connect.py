import mysql.connector

db = mysql.connector.connect (
      
      
      host = "localhost",
      user = "root",
      password = "password",
      database = "pos_new"
      
)

mycursor = db.cursor()