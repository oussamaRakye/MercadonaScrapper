import pandas as pd
file_name = "products3.csv"
file_name_output = "final_products3.csv"

df = pd.read_csv(file_name, sep=";")

df.drop_duplicates(subset=['title','quantity','price'], inplace=False)

# Write the results to a different file
df.to_csv(file_name_output)