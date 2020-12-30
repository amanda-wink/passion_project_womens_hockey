import pandas as pd

def read_file():
    NWHL_all = pd.read_csv('Data/nwhl_games_all.csv')
    print('File read in successfully')
    return(NWHL_all)

def get_data(dataframe):
    NWHL_2017 = pd.read_excel('Data/NWHL Skater and Team Stats 2017-18.xlsx', sheet_name='NWHL Skaters 201718')
    NWHL_2017.rename(columns={'Ht': 'Height', 'S': 'Shoots', 'Nat': 'Nationality'}, inplace=True)
    NWHL_personal = NWHL_2017[['Name', 'Height', 'Shoots', 'Nationality']]
    print(NWHL_personal.head(20))
    print(NWHL_personal.shape)

if __name__ == "__main__":
    df = read_file()
    get_data(df)