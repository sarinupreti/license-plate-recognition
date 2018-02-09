
import pymysql

numberplate ="BAA0272"

# Open database connection
db = pymysql.connect("localhost","testuser","test123","number_plate_recognition" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT * FROM information WHERE ID = '"+numberplate+"'"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      ID = row[0]
      OwnerName = row[1]
      Company = row[2]
      LicenseNumber = row[3]
      ManufactureDate = row[4]
      ChassisNo = row[5]
      # Now print fetched result
      print("ID=%s,OwnerName=%s,Company=%s,LicenseNumber=%s,ManufactureDate=%s, ChassisNo=%s" %
            (ID, OwnerName, Company, LicenseNumber, ManufactureDate, ChassisNo))
except:
    print("Error: unable to fecth data")

# disconnect from server
db.close()