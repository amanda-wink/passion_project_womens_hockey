import pandas as pd

loop = 1
for year in range(2016, 2020):
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
final.to_csv('nwhl.csv', index=False)