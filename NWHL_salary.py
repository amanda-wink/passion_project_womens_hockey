import pandas as pd
import os
from sqlalchemy import create_engine, Table

user = os.getenv('MYSQL_user')
pw = os.getenv('MYSQL')
str_sql = 'mysql+mysqlconnector://' + user + ':' + pw + '@localhost/hockey'
engine = create_engine(str_sql)

def read_file():
    NWHL_salary = pd.read_excel('Data/Salaries.xlsx', sheet_name='Sheet2')
    print('File read in successfully')
    return(NWHL_salary)

def get_data(dataframe):
    NWHL_salary = dataframe[['Season', 'Name', 'Team', 'Salary']]
    return(NWHL_salary)

def write_sql(dataframe):
    dataframe.to_sql(name='salary', con=engine, schema='hockey', if_exists='replace', index=False)
    engine.dispose()

if __name__ == "__main__":
    df = read_file()
    NWHL_sal = get_data(df)
    write_sql(NWHL_sal)