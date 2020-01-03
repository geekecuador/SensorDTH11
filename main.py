import Adafruit_DHT
import time
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4 

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temperatura={0:0.1f}C  Humedad={1:0.1f}%".format(temperature,humidity))
        try:
            connection = mysql.connector.connect(host='sensores.cwh4gmknqdm0.us-west-2.rds.amazonaws.com',
                                         database='sensores',
                                         user='',
                                         password='s')

            # INSERT INTO mydb.sensor (temperatura, humedad, fecha) VALUES ('4.4', '4', '2020-01-03 01:34:15')
            humidity = str(humidity)
            temperature = str(temperature)
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            mySql_insert_query = """INSERT INTO mydb.sensor (temperatura, humedad, fecha) 
                           VALUES 
                           ('{}', '{}', {}, ) """.format(humidity,temperature,date)

            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()
            print(cursor.rowcount, "Lectura guardada")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))

        finally:
            if (connection.is_connected()):
                connection.close()
                print("MySQL connection is closed")
    else:
        print("Sensor se encuentra fallando")
    time.sleep(20)





