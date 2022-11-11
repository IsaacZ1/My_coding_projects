import pandas as pd
import numpy as np

def load_and_clean_data(file_name):
    xl = pd.ExcelFile(file_name)
    dictionary = xl.parse('dictionary')
    dictionaryDF = dictionary.set_index('Country')

    summer = xl.parse('summer')
    summerDF = summer.iloc[1:]

    aTup = (dictionaryDF,summerDF)
    return aTup

def modify_dictionary(df_dict):
    capita = df_dict['Population']
    GDP = df_dict['GDP']
    df_dict['GDP per Capita'] = GDP / capita
    return df_dict

def modify_summer(df_summer):
    df_summer['Bronze'] = df_summer.apply(lambda row: int(row['Medal']=='Bronze'), axis = 1)

    df_summer['Silver'] = df_summer.apply(lambda row: int(row['Medal']=='Silver'), axis = 1)
    
    df_summer['Gold'] = df_summer.apply(lambda row: int(row['Medal']=='Gold'), axis = 1)
    
    df_summer['Place'] = df_summer.apply(lambda row:1 if row['Medal']=='Gold' else (2 if row['Medal'] == 'Silver' else 3), axis = 1)

    return df_summer
    

def null_counter(df_dict): # write in one line
    return len([i for i in df_dict['GDP per Capita'] if pd.isna(i)])

def medal_dataframe(df_summer):
    countryColumn = df_summer['Country']
    countryList = []
    for country in countryColumn:
        if country not in countryList:
            countryList.append(country)
    countryList = [i for i in countryList if str(i) != 'nan']
    sortedList = countryList.sort()
    bronzeList = []
    silverList = []
    goldList = []
    medalList = []
    for element in countryList:
        numBronze = df_summer.loc[df_summer["Country"] == element, "Bronze"].sum()
        numSilver = df_summer.loc[df_summer["Country"] == element, "Silver"].sum()
        numGold = df_summer.loc[df_summer["Country"] == element, "Gold"].sum()
        numMedals = numGold + numSilver + numBronze
        bronzeList.append(numBronze)
        silverList.append(numSilver)
        goldList.append(numGold)
        medalList.append(numMedals)
    df_medals = pd.DataFrame({"Country": countryList, "Bronze": bronzeList, "Silver": silverList, "Gold": goldList, "Total": medalList})
    df_medals = df_medals.set_index("Country")
    return df_medals

def medal_counter(df_medals, df_dict, medal_type, country):
    return df_medals.loc[df_dict.loc[country]["Code"]][medal_type]

def best_by_population(df_medals, df_dict, population):
    highScore = 0
    countryName = ""
    countryList = []
    for index, row in df_dict.iterrows():
        if row["Population"] < population:
            countryList.append(row["Code"])
    for index,row in df_medals.iterrows():
        if index in countryList:
            if df_medals.loc[index]["Total"] > highScore:
                highScore = float(df_medals.loc[index]["Total"])
                countryName = index
    return (countryName, highScore)

def best_by_discipline(df_summer, discipline):
    rows = df_summer[df_summer["Discipline"]== discipline]
    name = rows["Gold"].groupby(rows["Athlete"]).sum().idxmax()
    total = rows["Gold"].groupby(rows["Athlete"]).sum().max()
    return name,total

def average_medals(df_medals):
    df_medals.loc["Average"] = [df_medals["Bronze"].mean(),df_medals["Silver"].mean(),df_medals["Gold"].mean(),df_medals["Total"].mean()]
    return df_medals

def write_data(df_avg_medals, df_dict, file_name, sheet1_name, sheet2_name):
    pass

# Example ways to run and test your code
if __name__ == '__main__':
    df_dict, df_summer = load_and_clean_data("olympics.xlsx")
    #print(df_dict)
    #print(df_summer)
    df_dict = modify_dictionary(df_dict)
    #print(df_dict)
    df_summer = modify_summer(df_summer)
    #print(df_summer)
    null_count = null_counter(df_dict)
    #print(null_count)
    df_medals = medal_dataframe(df_summer)
    #print(df_medals)
    medal_counts = medal_counter(df_medals, df_dict, "Bronze", "Egypt")
    # print(medal_counts)
    best_pop = best_by_population(df_medals, df_dict, 10000000)
    # print(best_pop)
    best_disc = best_by_discipline(df_summer, "Swimming")
    # print(best_disc)
    df_medals = average_medals(df_medals)
    # print(df_medals)
    #write_data(df_avg_medals, df_dict, "olympics_stats.xlsx", "Medals", "Dictionary")
