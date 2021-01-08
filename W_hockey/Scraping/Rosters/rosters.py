import os
from sqlalchemy import create_engine
import tabula
import pandas as pd

teams = ['beauts', 'pride', 'riveters', 'toronto', 'whale', 'whitecaps']

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

def pdf_read(list):
    """
    Loops through the pdfs of each team and gathers the information from
    the table for each team into a dataframe.
    x is the right boundary of each column.
    Length is the overall length of the table.
    Unfortunately, not all the pdfs are the same resulting in x and length
    needing to be different between the teams.
    :param list: list of team names/pdf names
    :return: dataframe of information from all teams
    """
    loop = 1
    for team in list:
        if team in list[:3] or team == 'whale':
            x = [53.35, 112, 133, 160, 201, 236, 290]
            length = 618.5
            if team == 'beauts':
                length = 645
            elif team == 'whale':
                x.pop()
                x.append(304)
                length = 650
        else:
            x = [55, 122, 145, 172, 215, 249]
            if team == 'toronto':
                x.append(350)
            elif team == 'whitecaps':
                x.append(304)
                length = 580
        df = tabula.read_pdf(team + '.pdf', pages=1, area=[202.13, 38.5, length, 468.87], columns=x, guess=False)
        #tabula.read_pdf results in a list of dataframes. A for loop is used
        #to get an individual dataframe
        roster = df[0]
        roster.insert(2, 'team', [team] * len(roster))
        if loop == 1:
            final_roster = roster
        else:
            final_roster = pd.concat([final_roster, roster], ignore_index=True)
        loop += 1
        print(str(team) + ' added.')
    return final_roster

def write_sql(dataframe, engine):
    """
    Writes to SQL a database hockey and a table rosters.
    :param dataframe: Dataframe to be written
    :param engine: Connection to SQL
    :return: None
    """
    dataframe.to_sql(con=engine, schema='hockey', name='rosters', if_exists='replace', index=False)
    engine.dispose()
    print('Written to SQL.')

def write_csv(dataframe):
    """
    Writes to a csv.
    :param dataframe: Dataframe to be written
    :return: None
    """
    dataframe.to_csv('rosters.csv', index=False)
    print('Written to csv.')

def clean(df):
    """
    Cleans the dataframe by replacing team with official team names and replacing nulls with 'unknown'

    :param df: Dataframe of roster data
    :return: Dataframe cleaned
    """
    df.replace({'team': {'beauts': 'Buffalo Beauts', 'pride': 'Boston Pride', 'riveters': 'Metropolitan Riveters',
                         'toronto': 'Toronto Toronto', 'whale':'Connecticut Whale', 'whitecaps':'Minnesota Whitecaps'}},
               inplace=True)
    df2 = df.fillna('unknown')
    return df2

if __name__ == "__main__":
    con = connect_sql()
    roster = pdf_read(teams)
    #dataframe = pd.read_csv('rosters.csv')
    roster = clean(dataframe)
    write_sql(roster, con)
    write_csv(roster)
