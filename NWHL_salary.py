import pandas as pd
import os
from sqlalchemy import create_engine, Table

user = os.getenv('MYSQL_user')
pw = os.getenv('MYSQL')
str_sql = 'mysql+mysqlconnector://' + user + ':' + pw + '@localhost/w_hockey'
engine = create_engine(str_sql)

def read_file():
    NWHL_salary = pd.read_excel('W_hockey/Data/Salaries.xlsx', sheet_name='Sheet2')
    print('File read in successfully')
    return(NWHL_salary)

def get_data(dataframe):
    dataframe[['Last', 'First']] = dataframe.Name.str.split(', ', expand=True)
    dataframe.insert(1, 'Player', dataframe[['First', 'Last']].agg(' '.join, axis=1))
    dataframe.drop(columns=['Name', 'First', 'Last' ], inplace=True)
    NWHL_salary = dataframe[['Season', 'Player', 'Team', 'Salary']]
    return(NWHL_salary)

def write_sql(dataframe):
    dataframe.to_sql(name='salary', con=engine, if_exists='replace', index=False)
    engine.dispose()

if __name__ == "__main__":
    df = read_file()
    NWHL_sal = get_data(df)
    write_sql(NWHL_sal)