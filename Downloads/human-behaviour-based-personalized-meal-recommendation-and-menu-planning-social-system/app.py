import pandas as pd

df = pd.read_csv("./Data/dataset.csv",compression="gzip")

indian_food_df = pd.read_csv("./Data/IndianFoodDatasetCSV.csv")

print(df.columns)
print(indian_food_df.columns)


print(df.loc[1])

print(indian_food_df.loc[1])