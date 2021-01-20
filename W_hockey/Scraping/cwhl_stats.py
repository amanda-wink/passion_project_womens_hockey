import pandas as pd
from write_data import connect_sql, write_sql, write_csv

def get_cwhl_data(year_start, year_end, type):
    """
    Scrapes cwhl stats from eurohockey between year_start and year_end.
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
        url = 'http://www.eurohockey.com/stats/league/2019/488-cwhl.html?season=' + str(year) + '&type=' + str(type) + '&position=0&nationality=0'
        dataframes = pd.read_html(url, header=0)
        df = dataframes[0]
        df.drop(index=len(df) - 1, inplace=True)
        df.rename(columns={'Player name': 'Player'}, inplace=True)
        df2 = df[['Player', 'Pos', 'Team', 'GP', 'G', 'A', 'P', 'PIM', '+/-']]
        df2.insert(0, 'Season', [year - 1] * len(df))
        df2.insert(1, 'League', ['CWHL'] * len(df))
        if loop == 1:
            final=df2
        else:
            final = pd.concat([final, df2], ignore_index=True)
        loop += 1
        print(str(year - 1) + ' was added.')
    return final


def get_goalie_stats(year_start, year_end, type):
    """
    Scrapes cwhl goalie stats from eurohockey between year_start and year_end.
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
        url = 'http://www.eurohockey.com/stats/league/2016/488-cwhl.html?season=' + str(
            year) + '&type=' + str(type) + '&position=1&nationality=0'
        dataframes = pd.read_html(url, header=0)
        df = dataframes[0]
        df.drop(index=len(df) - 1, inplace=True)
        df.rename(columns={'Player name': 'Player'}, inplace=True)
        df2 = df[['Player', 'Team', 'GP', 'MIN', 'AVG', 'PER', 'SO', 'G', 'A', 'PIM']]
        df2.insert(0, 'Season', [year - 1] * len(df))
        df2.insert(1, 'League', ['CWHL'] * len(df))
        if loop == 1:
            final_g = df2
        else:
            final_g = pd.concat([final_g, df2], ignore_index=True)
        loop += 1
        print(str(year - 1) + ' was added.')
    return final_g

#def clean_skater(dataframe):


if __name__ == "__main__":
    con = connect_sql()
    """
    #regular season skater stats
    stats = get_cwhl_data(2008, 2020, 1)
    write_sql(stats, con, 'cwhl_stats')
    write_csv(stats, 'csv/cwhl')
    #goalie regular season stats
    goalie_stats = get_goalie_stats(2011, 2020)
    write_sql(goalie_stats, con, 'cwhl_goalies')
    write_csv(goalie_stats, 'csv/cwhl_goalies')
    #playoff skater stats
    playoff_stats = get_cwhl_data(2016, 2017, 2)
    playoff_stats2 = get_cwhl_data(2018, 2019, 2)
    final_p_stats = pd.concat([playoff_stats, playoff_stats2], ignore_index=True)
    write_sql(final_p_stats, con, 'cwhl_playoffs')
    write_csv(final_p_stats, 'csv/cwhl_playoffs')
    #playoff goalie stats
    g_playoff_stats = get_goalie_stats(2016, 2017, 2)
    g_playoff_stats2 = get_goalie_stats(2018, 2019, 2)
    final_pg_stats = pd.concat([g_playoff_stats, g_playoff_stats2], ignore_index=True)
    write_sql(final_pg_stats, con, 'cwhl_playoffs_g')
    write_csv(final_pg_stats, 'csv/cwhl_playoffs_g')
    """
    #write to sql from csv
    stats_reg = pd.read_csv('csv/cwhl.csv')
    write_sql(stats_reg, con, 'cwhl_stats')
    stats_p = pd.read_csv('csv/cwhl_playoffs.csv')
    write_sql(stats_p, con, 'cwhl_playoffs')
    stats_reg_g = pd.read_csv('csv/cwhl_goalies.csv')
    write_sql(stats_reg_g, con, 'cwhl_goalies')
    stats_p_g = pd.read_csv('csv/cwhl_playoffs_g.csv')
    write_sql(stats_p_g, con, 'cwhl_playoffs_g')
