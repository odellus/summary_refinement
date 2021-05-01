import time
import sqlite3
import pandas as pd

# Set up sqllite3 db class.
class SummaryDB:
    '''
    A neat little DB class so we know it disconnects because __del__
    '''
    db_file = 'summaries.db'
    table_name = 'summaries'
    dt_pattern = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        '''
        Get a connection to self.db_file and create a cursor
        '''
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.get_or_create()

    def list_tables(self):
        qry = """
            SELECT name FROM
               (SELECT * FROM sqlite_master UNION ALL
                SELECT * FROM sqlite_temp_master)
            WHERE type='table'
            ORDER BY name;
        """
        return [x for x in self.cursor.execute(qry)]

    def get_or_create(self):
        tables = self.list_tables()
        if len(tables) < 1:
            self.create_table()

    def save(self):
        '''
        Have to do this after everything apparently.
        '''
        self.connection.commit()

    def create_table(self):
        '''
        Creates a table named self.table_name: default-> autolector.
        '''
        qry = f'''CREATE TABLE {self.table_name}
                 (   date text,
                     article_id text,
                     article_text text,
                     summary text,
                     entry_src text,
                     rouge real,
                     meteor real
                 )'''
        self.cursor.execute(qry)

    def insert(self, article_id, article_text, summary):
        '''
        Insert question, context, answer, and timestamp into the table.
        '''
        date = time.strftime(self.dt_pattern)
        qry = f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?, ?)"
        entry_src = 'COMPUTER'
        rouge, meteor = None, None
        entry = (date, article_id, article_text, summary, entry_src, rouge, meteor)
        self.cursor.execute(qry, entry)
        self.save()

    def update(self, article_id, article_text, summary, rouge, meteor):
        '''
        '''
        date = time.strftime(self.dt_pattern)
        qry = f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?, ?)"
        entry_src = 'HUMAN'
        entry = (date, article_id, article_text, summary, entry_src, rouge, meteor)
        self.cursor.execute(qry, entry)
        self.save()

    def get_computer_summary(self, article_id):
        qry = f"SELECT article_text, summary FROM {self.table_name} WHERE article_id='{article_id}' AND entry_src='COMPUTER' LIMIT 1"
        row = [x for x in self.cursor.execute(qry)].pop()
        return row

    def get_all(self):
        '''
        Return all the rows in the self.table_name table.
        '''
        qry = f'SELECT * FROM {self.table_name}'
        rows = [x for x in self.cursor.execute(qry)]
        return rows

    def get_df(self):
        '''
        Return a pandas DataFrame of the self.table_name table.
        '''
        qry = f'SELECT * FROM {self.table_name}'
        df = pd.read_sql(qry, self.connection)
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date')

    def drop_table(self):
        '''
        Drop table self.table_name from database.
        '''
        qry = f"DROP TABLE {self.table_name}"
        self.cursor.execute(qry)

    def __del__(self):
        '''
        The whole reason we are using OOP. Close connection automatically.
        '''
        self.save()
        self.connection.close()
