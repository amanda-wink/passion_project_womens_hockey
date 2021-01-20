import os
from sqlalchemy import create_engine
import pandas as pd


def connect_sql():
    """
    Connects to SQL. Requires a username and password being set in your env.
    :return: Connection to SQL
    """
    #user = os.getenv('MYSQL_user')
    #pw = os.getenv('MYSQL')
    #str_sql = 'mysql+mysqlconnector://' + user + ':' + pw + '@localhost/w_hockey'
    p_user = os.getenv('p_user')
    str_sql = 'postgresql://' + p_user + ':postgres@localhost/w_hockey'
    engine = create_engine(str_sql)
    return engine

def get_table_html(dataframe):
    htable = '<table><tr><th>Player</th><th>Team</th>' \
             '<th>Games Played</th><th>Points</th></tr>'
    if len(dataframe) == 0:
        return '<div>No Statistics Available</div>'
    else:
        for index, row in dataframe.iterrows():
            new_row = '<tr>'
            new_row += '<td>' + str(row['Player']) + '</td><td>' + str(row['Team']) + '</td><td>' + str(
                row['GP']) + '</td><td>' + str(row['P']) + '</td>'
            new_row += '</tr>'
            htable += new_row
        htable += '</table>'
        return htable

def get_table_list(engine, table, league, year):
    league = '\'' + str(league) + '\''
    year = '\'' + str(year)+ '\''
    df = pd.read_sql('select "Player", "Team", "GP", "P" from ' + str(table) +
                                    ' where "Season" = ' + year + ' and "League" = ' + str(league) +
                                    ' and "GP" is not null order by "P" DESC LIMIT 5;', engine)
    return df

def get_all_table_list(con, year, table1, table2):
    nwhl = get_table_list(con, table1, 'NWHL', year)
    cwhl = get_table_list(con, table2, 'CWHL', year)
    if nwhl.empty and cwhl.empty:
        return None
    else:
        if nwhl.empty:
            all=cwhl
        elif cwhl.empty:
            all = nwhl
        else:
            all = pd.concat([nwhl, cwhl], ignore_index=True)
        all['P/G'] = all['P']/all['GP']
        all['P/G'] = all['P/G'].apply(lambda x: round(x,2))
        all_top = all.sort_values(by=['P/G'], ascending=False)
        return all_top.head(5)

def get_all_html(dataframe):
    if dataframe is None:
        return '<div>No Statistics Available</div>'
    else:
        htable_all = '<table><tr><th>Player</th><th>Team</th>' \
                 '<th>Games Played</th><th>Points</th><th>P/G</th></tr>'
        for index, row in dataframe.iterrows():
            new_row_h = '<tr>'
            new_row_h += '<td>' + str(row['Player']) + '</td><td>' + str(row['Team']) + '</td><td>' + str(row['GP']) + '</td><td>' + str(row['P']) + '</td><td>' + str(row['P/G']) + '</td>'
            new_row_h += '</tr>'
            htable_all += new_row_h
        htable_all += '</table>'
        return htable_all

def get_goalie_table(engine, table, league, year):
    league = '\'' + str(league) + '\''
    year = '\'' + str(year)+ '\''
    df = pd.read_sql('select "Player", "Team", "GP", "PER" from ' + str(table) +
                     ' where "Season" = ' + year + ' and "League" = ' + str(league) +
                     ' and "GP" is not null and "PER" is not null'
                     ' order by "PER" DESC LIMIT 5;', engine)
    return df

def get_goalie_html(dataframe):
    if len(dataframe) == 0:
        return '<div>No Statistics Available</div>'
    else:
        htable_all = '<table><tr><th>Player</th><th>Team</th>' \
                 '<th>Games Played</th><th>Save Percentage</th>'
        for index, row in dataframe.iterrows():
            new_row_h = '<tr>'
            new_row_h += '<td>' + str(row['Player']) + '</td><td>' + str(row['Team']) + '</td><td>' + str(int(row['GP'])) + '</td><td>' + str(round(row['PER'],2)) + '</td>'
            new_row_h += '</tr>'
            htable_all += new_row_h
        htable_all += '</table>'
        return htable_all


if __name__ =='__main__':
    con = connect_sql()
    df = get_goalie_table(con, 'nwhl_goalies', 'NWHL', 2015)
    print(df)