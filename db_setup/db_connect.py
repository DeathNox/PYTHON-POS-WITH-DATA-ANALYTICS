import mysql.connector

db = mysql.connector.connect (
      
      
      host = "localhost",
      user = "root",
      password = "root",
      database = "pos_cafe"
      
)

mycursor = db.cursor()