import datetime
from fabric import Connection

with open('password.txt') as f:
    password = f.read()

connection = Connection(host='127.0.0.1', user='euc', connect_kwargs={'password': password})

def install_mysql():
    connection.run('sudo apt-get update')
    connection.run('sudo apt-get install -y mysql-server')

def create_database(db_name, db_password):
    connection.run(f"mysql -u root -p{db_password} -e 'CREATE DATABASE IF NOT EXISTS {db_name};'")

def run_sql_dump(db_name, dump_path, db_password):
    connection.run(f"mysql -u root -p{db_password} {db_name} < {dump_path}")

if __name__ == '__main__':
    install_mysql()
    db_name = 'graph_db'  # Matches .env DATABASE_URI
    db_password = 'euctech'  # Matches .env root password
    dump_path = 'analysis.sql'  # Uses the generated SQL dump for your app
    create_database(db_name, db_password)
    run_sql_dump(db_name, dump_path, db_password)
