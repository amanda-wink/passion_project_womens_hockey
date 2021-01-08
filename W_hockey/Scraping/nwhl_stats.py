import pandas as pd
from write_data import connect_sql, write_sql, write_csv

def get_nwhl_data(year_start, year_end, type):
    """
    Scrapes nwhl stats from eurohockey between year_start and year_end.
    Creates a dataframe that gets written to SQL and a csv.
    Type 1 - regular season
    Type 2 - playoffs

    Note: the website categorizes a season by the year of the second half.
        For example, 2015-2016 season is the year 2016
    :param year_start: Int representing first year of data you want
    :param year_end: Int representing last year of data you want
    :return: dataframe of all stats between year_start and year_end
    """
    loop = 1
    for year in range(year_start, year_end):
        url = 'http://www.eurohockey.com/stats/league/2018/1405-nwhl.html?season=' + str(year) + '&type=' + str(type) + '&position=0&nationality=0'
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



def get_goalie_stats(year_start, year_end, type):
    """
    Scrapes nwhl goalie stats from eurohockey between year_start and year_end.
    Creates a dataframe that gets written to SQL and a csv.
    Type 1 - regular season
    Type 2 - playoffs

    Note: the website categorizes a season by the year of the second half.
        For example, 2015-2016 season is the year 2016
    :param year_start: Int representing first year of data you want
    :param year_end: Int representing last year of data you want
    :return: dataframe of all stats between year_start and year_end
    """
    loop = 1
    for year in range(year_start, year_end):
        url = 'http://www.eurohockey.com/stats/league/2016/1405-nwhl.html?season=' + str(year) + '&type=' + str(type) + '&position=1&nationality=0'
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

    #regular season skater stats
    stats = get_nwhl_data(2016, 2020, 1)
    write_sql(stats, con, 'nwhl_stats')
    write_csv(stats, 'csv/nwhl')
    #regular season goalie stats
    goalie_stats = get_goalie_stats(2016, 2020)
    write_sql(goalie_stats, con, 'nwhl_goalies')
    write_csv(goalie_stats, 'csv/nwhl_goalies')
    #playoff skater stats
    playoff_stats = get_nwhl_data(2017, 2019, 2)
    write_sql(playoff_stats, con, 'nwhl_playoffs')
    write_csv(playoff_stats, 'csv/nwhl_playoffs')
    #playoff goalie stats
    g_playoff_stats = get_goalie_stats(2017, 2019, 2)
    write_sql(goalie_stats, con, 'nwhl_playoffs_g')
    write_csv(g_playoff_stats, 'csv/nwhl_playoffs_g')
    """
    # write to sql from csv
    stats_reg = pd.read_csv('csv/nwhl.csv')
    write_sql(stats_reg, con, 'nwhl_stats')
    stats_p = pd.read_csv('csv/nwhl_playoffs.csv')
    write_sql(stats_p, con, 'nwhl_playoffs')
    stats_reg_g = pd.read_csv('csv/nwhl_goalies.csv')
    write_sql(stats_reg_g, con, 'nwhl_goalies')
    stats_p_g = pd.read_csv('csv/nwhl_playoffs_g.csv')
    write_sql(stats_p_g, con, 'nwhl_playoffs_g')
    """