import psycopg2
import json
import os
from typing import Optional

class sqlManager:
    def __init__(self):
        self.dbname = os.getenv("DBNAME")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host=os.getenv("HOST")
        self.port=os.getenv("PORT")

    def _get_sql(self) -> psycopg2.extensions.connection:
        """
        internal function to get sql connection

        Returns:
            psycopg2.extensions.connection: SQL connection
        """

        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return conn
    
    def _make_call(self, query: str, query_data: dict=False, fetch: bool=False) -> Optional[dict]:
        """
        internal function to make an SQL call

        Args:
            query (str): SQL query, can be segmented to use query_data as well
            query_data (dict, optional): SQL query data if %s or similar was used
            fetch (bool, optional): Returns cur.fetchall() if True. default is False 
        Returns:
            fetch (dict | None): fetch data
        """

        conn = self._get_sql()
        cur = conn.cursor()

        if query_data == False:
            cur.execute(query)
        else:
            cur.execute(query, query_data)
        
        if fetch != False:
            data = cur.fetchall()

        conn.commit()
        cur.close()
        conn.close()
        
        if fetch != False:
            return data
    
    def postGameData(self, data: dict) -> None:
        """
        sends python dictionaries to a SQL database.

        Args:
            data (dict): python dictionary to be uploaded
        """

        query = "INSERT INTO json_data (data) VALUES (%s)"

        self._make_call(query, [json.dumps(data)])

