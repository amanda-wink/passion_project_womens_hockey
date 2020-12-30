import pandas as pd

loop = 1
for year in range(2008, 2019):
    url = 'http://www.eurohockey.com/stats/league/' + str(year) + '/488-cwhl.html'
    print(url)
    dataframes = pd.read_html(url, header=0)
    df = dataframes[0]
    df.drop(index=len(df) - 1, inplace=True)
    df2 = df[['Player name', 'Pos', 'Team', 'GP', 'G', 'A', 'P', 'PIM', '+/-']]
    df2.insert(0, 'Season', [year] * len(df))
    df2.insert(1, 'League', ['CWHL'] * len(df))
    if loop == 1:
        final=df2
    else:
        final = pd.concat([final, df2], ignore_index=True)
    loop += 1
    print(str(year) + ' was added.')
final.to_csv('cwhl.csv', index=False)