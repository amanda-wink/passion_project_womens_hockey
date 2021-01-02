import pandas as pd
from write_data import connect_sql, write_sql, write_csv

def get_nwhl_data(year_start, year_end):
    """
    Scrapes nwhl stats from eurohockey between year_start and year_end.
    Creates a dataframe that gets written to SQL and a csv.

    Note: the website categorizes a season by the year of the second half.
        For example, 2015-2016 season is the year 2016
    :param year_start: Int representing first year of data you want
    :param year_end: Int representing last year of data you want
    :return: dataframe of all stats between year_start and year_end
    """
    loop = 1
    for year in range(year_start, year_end):
        url = 'http://www.eurohockey.com/stats/league/' + str(year)+ '/1405-nwhl.html'
        dataframes = pd.read_html(url, header=0)
        df = dataframes[0]
        df.drop(index=len(df) - 1, inplace=True)
        df.rename(columns={'Player name': 'Player'}, inplace=True)
        df2 = df[['Player', 'Pos', 'Team', 'GP', 'G', 'A', 'P', 'PIM', '+/-']]
        df2.insert(0, 'Season', [year - 1] * len(df))
        df2.insert(1, 'League', ['NWHL'] * len(df))
        if loop == 1:
            final=df2
        else:
            final = pd.concat([final, df2], ignore_index=True)
        loop += 1
        print(str(year -1) + ' was added.')
    return final



def get_goalie_stats(year_start, year_end):
    """
    Scrapes nwhl goalie stats from eurohockey between year_start and year_end.
    Creates a dataframe that gets written to SQL and a csv.

    Note: the website categorizes a season by the year of the second half.
        For example, 2015-2016 season is the year 2016
    :param year_start: Int representing first year of data you want
    :param year_end: Int representing last year of data you want
    :return: dataframe of all stats between year_start and year_end
    """
    loop = 1
    for year in range(year_start, year_end):
        url = 'http://www.eurohockey.com/stats/league/2016/1405-nwhl.html?season=' + str(year) + '&type=1&position=1&nationality=0'
        dataframes = pd.read_html(url, header=0)
        df = dataframes[0]
        df.drop(index=len(df) - 1, inplace=True)
        df.rename(columns={'Player name': 'Player'}, inplace=True)
        df2 = df[['Player', 'Team', 'GP', 'MIN', 'AVG', 'PER','SO', 'G', 'A', 'PIM']]
        df2.insert(0, 'Season', [year - 1] * len(df))
        df2.insert(1, 'League', ['NWHL'] * len(df))
        if loop == 1:
            final_g = df2
        else:
            final_g = pd.concat([final_g, df2], ignore_index=True)
        loop += 1
        print(str(year - 1) + ' was added.')
    return final_g

if __name__ == "__main__":
    con = connect_sql()
    stats = get_nwhl_data(2016, 2020)
    write_sql(stats, con, 'nwhl_stats2')
    write_csv(stats, 'nwhl')
    goalie_stats = get_goalie_stats(2016, 2020)
    write_sql(goalie_stats, con, 'nwhl_goalies')
    write_csv(goalie_stats, 'nwhl_goalies')

