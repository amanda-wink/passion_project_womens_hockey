import pandas as pd
from write_data import connect_sql, write_sql, write_csv

def get_cwhl_data(year_start, year_end):
    """
    Scrapes cwhl stats from eurohockey between year_start and year_end.
    Creates a dataframe that gets written to SQL and a csv.

    :param year_start: Int representing first year of data you want
    :param year_end: Int representing last year of data you want
    :return: dataframe of all stats between year_start and year_end
    """
    loop = 1
    for year in range(2008, 2020):
        url = 'http://www.eurohockey.com/stats/league/' + str(year) + '/488-cwhl.html'
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

if __name__ == "__main__":
    con = connect_sql()
    stats = get_cwhl_data(2008, 2020)
    write_sql(stats, con, 'cwhl_stats')
    write_csv(stats, 'cwhl')
