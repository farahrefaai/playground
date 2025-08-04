 
from flask import Flask, request, jsonify
from uhashring import HashRing
import psycopg2
import hashlib
import os

app = Flask(__name__)


# Create hash ring (CONSISTENT HASHING)
# since we are working locally
# we will distinguish between the servers by ports
hr = HashRing(['5441', '5442', '5443'])

# DATABASE SHARDS CONFIGURATION
DATABASE_SERVERS = {
    '5441': {
    'host': '127.0.0.1',
    'port':'5441',
    'database':'postgres',
    'user': 'postgres',
    'password':  'mysecretpassword'
    },
    '5442': {
    'host': '127.0.0.1',
    'port':'5442',
    'database':'postgres',
    'user': 'postgres',
    'password':  'mysecretpassword'
    },
    '5443': {
    'host': '127.0.0.1',
    'port':'5443',
    'database':'postgres',
    'user': 'postgres',
    'password':  'mysecretpassword'
    }
}



def hash_sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def get_connection(server):
    """Get database connection"""
    conn = psycopg2.connect(**server)
    print("✅ Connection successful!")
    return conn

def get_db_cursor(conn):
    """Get database cursor"""
    cur = conn.cursor()
    return cur





@app.route('/url', methods=['GET'])
def handle_get():
    data = request.args
    url = data.get('urlId')
    # GET NODE FOR URL
    node = hr.get_node(url)
    print(f"the port for url {url} is {node}")

    #CONNECT TO SHARD
    connection = get_connection(DATABASE_SERVERS[node])
    cursor = get_db_cursor(connection)
    cursor.execute("""SELECT url FROM url_table WHERE URL_ID = %(urlId)s""",{"urlId":data['urlId']})
    records = cursor.fetchall()
    
    #RETURN RESPONSE
    return jsonify({"message": "GET request successful", "status": "ok", "record":records[0]})

@app.route('/url', methods=['POST'])
def handle_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        url = data['url']   
        # GET NODE FOR URL   
        node = hr.get_node(url)
        print(f"the port for url {url} is {node}")

        # HASH URL
        hashed_url = hash_sha256(url)
        urlId = hashed_url[0:5]

        #INSERT INTO DB
        connection = get_connection(DATABASE_SERVERS[node])
        cursor = get_db_cursor(connection)
        cursor.execute("""INSERT INTO URL_TABLE (URL, URL_ID) VALUES (%(url)s,%(urlId)s)""",{"url":url,"urlId":urlId})
        connection.commit()

        
        return jsonify({
            "message": "POST request successful",
            "received": data,
            "urlId": urlId,
            "node": node,
            "status": "ok"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)