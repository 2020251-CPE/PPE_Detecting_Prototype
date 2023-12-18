from flask import jsonify
from dotenv import load_dotenv
import psycopg2.extras
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

def connect():
    conn = psycopg2.connect(
        host= os.getenv('DB_HOST'),
        database= os.getenv('DB_NAME'),
        user= os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        sslmode='require',
        )
    return conn

def upload_metadata(filename,fileLoc,datetime,array):
    '''Uploads Screenshot Metadata to postgres Database (NeonDB)'''
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            query='INSERT INTO ppe_log (photoName,photoURL,dateAndTime,apronCount,bunnysuitCount,maskCount,glovesCount,gogglesCount,headcapCount) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s)',
            vars=(filename, fileLoc, datetime, array[0], array[1], array[2], array[3], array[4], array[5])
            )
        conn.commit()
        cur.close()
    except psycopg2.InterfaceError as e:
        print('{} - connection will be reset'.format(e))
        # Close old connection 
        if conn:
            if cur:
                cur.close()
            conn.close()
        conn = None
        cur = None
        #Reconnect
        conn = connect()
        conn.cursor()

def get_logs(options="today"):
    """Get Certain Queries"""
    try:
        conn = connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if options == "today":
            cur.execute(
                query='SELECT * FROM todayRows ORDER BY dateAndTime DESC'
            )
            rows = cur.fetchall()
            cur.close()
            return rows
        elif options == "all":
            cur.execute(
                query='SELECT photoName,photoURL,dateAndTime,apronCount,bunnysuitCount,maskCount,glovesCount,gogglesCount,headcapCount FROM ppe_log'
            )
            rows = cur.fetchall()
            cur.close()
            return rows
    except psycopg2.InterfaceError as e:
        print('{} - connection will be reset'.format(e))
        # Close old connection 
        if conn:
            if cur:
                cur.close()
            conn.close()
        conn = None
        cur = None
        #Reconnect
        conn = connect()
        conn.cursor()
    except Exception as e:
        return jsonify(error=str(e))