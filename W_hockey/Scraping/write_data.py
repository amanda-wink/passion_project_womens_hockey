import os
from sqlalchemy import create_engine

def connect_sql():
    """
    Connects to SQL. Requires a username and password being set in your env.
    :return: Connection to SQL
    """
    user = os.getenv('MYSQL_user')
    pw = os.getenv('MYSQL')
    str_sql = 'mysql+mysqlconnector://' + user + ':' + pw + '@localhost/'
    engine = create_engine(str_sql)
    return engine

def write_sql(dataframe, engine, table):
    """
    Writes to SQL a database hockey and a table rosters.
    :param dataframe: Dataframe to be written
    :param engine: Connection to SQL
    :return: None
    """
    dataframe.to_sql(con=engine, schema='w_hockey', name=table, if_exists='replace', index=False)
    engine.dispose()
    print('Written to SQL.')

def write_csv(dataframe, name):
    """
    Writes to a csv.
    :param dataframe: Dataframe to be written
    :return: None
    """
    dataframe.to_csv(str(name) + '.csv', index=False)
    print('Written to csv.')


