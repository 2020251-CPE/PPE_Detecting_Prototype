from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
conn = psycopg2.connect(
        host= os.getenv('DB_HOST'),
        database= os.getenv('DB_NAME'),
        user= os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        sslmode='require',
        )

def upload_metadata(filename,fileLoc,datetime,array):
    '''Uploads Screenshot Metadata to postgres Database (NeonDB)'''
    cur = conn.cursor()
    cur.execute(
        query='INSERT INTO ppe_log (photoName,photoURL,dateAndTime,apronCount,bunnysuitCount,maskCount,glovesCount,gogglesCount,headcapCount) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s)',
        vars=(filename, fileLoc, datetime, array[0], array[1], array[2], array[3], array[4], array[5])
        )
    conn.commit()
    cur.close()

def get_logs(options="today"):
    """Get Certain Queries"""
    cur = conn.cursor()
    if options == "today":
        cur.execute(
            query='SELECT * FROM todayRows ORDER BY dateAndTime DESC'
        )
    elif options == "all":
        cur.execute(
            query='SELECT * FROM ppe_log'
        )