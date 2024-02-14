import platform
import psutil
from flask import Flask, render_template, redirect
import socket
import getpass
import mysql.connector

# Function to establish database connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ryanlion20&",
            database="cybersecurity"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to insert system information into the database
def insert_system_info(info):
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO Cybersecurity (User_System, User_Node, User_Release, User_Version, User_Machine, User_Processor, Cpu_Usage, Memory_Usage, Local_Ip, Username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                info['System'], info['Node'], info['Release'], info['Version'], info['Machine'], info['Processor'],
                info['CPU Usage (%)'], info['Memory Usage (%)'], info['Local IP'], info['Username']
            )
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            print("System information inserted into the database successfully.")
    except mysql.connector.Error as e:
        print(f"Error inserting system information into database: {e}")

# Function to get the current username
def get_current_username():
    try:
        username = getpass.getuser()
        return username
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to get the local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to collect system information
def collect_system_info():
    info = {}

    info['System'] = platform.system()
    info['Node'] = platform.node()
    info['Release'] = platform.release()
    info['Version'] = platform.version()
    info['Machine'] = platform.machine()
    info['Processor'] = platform.processor()[:20]

    info['CPU Usage (%)'] = psutil.cpu_percent(interval=1)
    info['Memory Usage (%)'] = psutil.virtual_memory().percent
    info['Local IP'] = get_local_ip()
    info['Username'] = get_current_username()

    return info

app = Flask(__name__)

@app.route('/')
def index():
    system_info = collect_system_info()
    insert_system_info(system_info)  # Insert system information into the database
    print(system_info)
    return render_template('index.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
