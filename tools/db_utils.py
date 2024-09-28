import os
import time
import psycopg2 as pg


class PGConn:
    def __init__(self, retry=True):
        try:
            self.conn = pg.connect(dbname='postgres',
                          user=os.getenv("NYX_USER"), password=os.getenv("NYX_PASSWORD"),
                          host=os.getenv("NYX_HOST"), port=os.getenv("NYX_PORT"))
        except Exception as e:
            if e == pg.OperationalError and retry:
                print("Database connection failed. The container may not yet be ready to accept connections."
                            " Retrying in 30 seconds...")
                time.sleep(30)
                self.__init__(retry=False)

        # Check if database exists and create it if it doesn't
        if not self.check_database_exists(os.getenv("NYX_DB")):
            self.create_database(os.getenv("NYX_DB"))

        self.conn.close()

        self.conn = pg.connect(dbname='postgres',
                               user=os.getenv("NYX_USER"), password=os.getenv("NYX_PASSWORD"),
                               host=os.getenv("NYX_HOST"), port=os.getenv("NYX_PORT"))

    def check_database_exists(self, db_name):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            return cursor.fetchone()

    def create_database(self, db_name):
        self.conn.rollback()
        self.conn.autocommit = True

        with self.conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {db_name}")

        self.conn.autocommit = False