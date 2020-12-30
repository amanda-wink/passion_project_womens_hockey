import pandas as pd
import os
from sqlalchemy import create_engine

def connect_sql():
    user = os.getenv('MYSQL_user')
    pw = os.getenv('MYSQL')
    str_sql = 'mysql+mysqlconnector://' + user + ':' + pw + '@localhost/hockey'
    engine = create_engine(str_sql)
    return engine

def read_file():
    NWHL_all = pd.read_csv('Data/nwhl_games_all.csv')
    print('File read in successfully')
    return(NWHL_all)

def reformat(dataframe):
    #rename columns
    dataframe.rename(columns={'position': 'Pos', 'A1': 'A', 'A2': 'A1', 'PTS': 'P', 'PrPTS': 'P1', 'PPA1': 'PPA',
                             'PPA2': 'PPA1', 'SHA1': 'SHA', 'SHA2': 'SHA1'}, inplace=True)
    #reformat
    NWHL_all_format = dataframe[
        ['Season', 'Player', 'Team', 'Pos', 'game_id', 'G', 'A', 'A1', 'P', 'P1', 'PPG', 'PPA', 'PPA1', 'SHG',
         'SHA', 'SHA1', 'PIM', 'Blk']]
    #Insert two rows (League and Games Played)
    NWHL_all_format.insert(1, 'League', ['NWHL'] * len(NWHL_all_format))
    NWHL_all_format.insert(5, 'GP', [None] * len(NWHL_all_format))
    #column headings
    columns = NWHL_all_format.columns.tolist()
    columns.pop(6)
    column_slice = columns[6:]

    #List of unique years
    years = NWHL_all_format['Season'].unique()
    years.tolist()
    for year in years:
        NWHL_all_format_year = NWHL_all_format[NWHL_all_format['Season'] == year]
        #List of unique players
        player_name = NWHL_all_format_year['Player'].unique()
        player_name.tolist()
        for name in player_name:
            df = NWHL_all_format_year[NWHL_all_format_year['Player'] == name]
            #Getting data that does not change over rows
                #Name, Position, etc.
            player_stat = df.iloc[0][0:5]
            player_stat2 = player_stat.tolist()
            #Counting games played
            gp = len(df['game_id'].unique())
            player_stat2.append(gp)
            #Calculate the season stats from the game stats
            for col in column_slice:
                val = df[col].sum()
                player_stat2.append(val)
            #Create a series of  the list/row
            player_stat3 = pd.Series(player_stat2, index=columns)
            NWHL_all_format = NWHL_all_format.append(player_stat3, ignore_index=True)
    #Delete individual game data by finding rows wtih Games played as None
    NWHL_final = NWHL_all_format[NWHL_all_format['GP'].notnull()]
    print(NWHL_final.head(20))
    print(NWHL_final.shape)
    print(NWHL_final.tail(20))
    return NWHL_final

def write_sql(dataframe, engine):

    dataframe.to_sql(name='nwhl_stats', con=engine, schema='hockey', if_exists='replace', index=False)
    engine.dispose()

def write_csv(dataframe):
    dataframe.to_csv('nwhl_all_stats2.csv')
    print('Done')

if __name__ == "__main__":
    #con = connect_sql()
    df = read_file()
    NWHL_data = reformat(df)
    #write_sql(NWHL_data, con)
    write_csv(NWHL_data)