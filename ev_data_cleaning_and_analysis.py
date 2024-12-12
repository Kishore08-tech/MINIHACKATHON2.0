import pandas as pd
EV_Maker_by_place=pd.read_csv("/content/drive/MyDrive/Mini Hackathon 2.0/EV Maker by Place.csv")
#checking for duplicates
print(EV_Maker_by_place.duplicated().sum())
#removing duplicates
EV_Maker_by_place.drop_duplicates(inplace=True)
print(EV_Maker_by_place.duplicated().sum())
#checking for null values
print(EV_Maker_by_place.isnull().sum())

Operational_PC=pd.read_csv("/content/drive/MyDrive/Mini Hackathon 2.0/OperationalPC.csv")
#checking for duplicates
print(Operational_PC.duplicated().sum())
#No dupliactes found
#checking for null values
print(Operational_PC.isnull().sum())

Vehicle_class=pd.read_csv("/content/drive/MyDrive/Mini Hackathon 2.0/Vehicle Class - All.csv")
#CHecking for duplicates
print(Vehicle_class.duplicated().sum())
#No duplicates found
#checking for null values
print(Vehicle_class.isnull().sum())

ev_cat_01_24=pd.read_csv("/content/drive/MyDrive/Mini Hackathon 2.0/ev_cat_01-24.csv")
#Checking for duplicates
print(ev_cat_01_24.duplicated().sum())
#No dupliactes found
#checking for null values
print(ev_cat_01_24.isnull().sum())

ev_sales_by_makers = pd .read_csv("/content/drive/MyDrive/Mini Hackathon 2.0/ev_sales_by_makers_and_cat_15-24.csv")
#Checking for duplicates
print(ev_sales_by_makers.duplicated().sum())
#no duplicates found
#checking for null values
print(ev_sales_by_makers.isnull().sum())

# Creating a function for detecting outliers
def outlier(df, ft):
    Q1 = df[ft].quantile(0.25)
    Q3 = df[ft].quantile(0.75)
    print(Q3)
    # Calculating Interquartile Range (IQR)
    IQR = Q3 - Q1
    print(IQR)
    # Setting limits for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Storing the indexes which contain outliers in a list
    ls = df.index[(df[ft] < lower_bound) | (df[ft] > upper_bound)]  # Add parentheses
    return ls

#Number of EV makers in each state
EV_Maker_by_place.groupby('State')['EV Maker'].count().sort_values(ascending=False)

#number of EV makers for each place
EV_Maker_by_place.groupby('Place')['EV Maker'].count().sort_values(ascending=False)

# Total sales for each year for each category
sales_by_category = ev_sales_by_makers.groupby('Cat').sum().loc[:, '2015':'2024']
print(sales_by_category)


#Top 10 EV selling companies and their market shares
ev_sales_by_makers['Total_Sales'] = ev_sales_by_makers.loc[:, '2015':'2024'].sum(axis=1)
top_makers = ev_sales_by_makers[['Maker', 'Total_Sales']].sort_values(by='Total_Sales', ascending=False)
ev_sales_by_makers['Market Share']=(ev_sales_by_makers['Total_Sales']/ev_sales_by_makers['Total_Sales'].sum())*100
print(  ev_sales_by_makers[['Maker','Total_Sales','Market Share']].sort_values(by='Market Share', ascending=False).head(10).to_string(index=False))
ev_sales_by_makers.to_csv('ev_sales_by_makers.csv', index=False)
from google.colab import files
files.download('ev_sales_by_makers.csv')

#dropping the first row because it contains only zeros
ev_cat_01_24_cleaned = ev_cat_01_24.drop(0)
#Total number of EV manufactured in each year 

#Converting the date column to datetime format
ev_cat_01_24_cleaned['Date'] = pd.to_datetime(ev_cat_01_24_cleaned['Date'], format='%d/%m/%y')

# Extracting the year from the 'Date' column
ev_cat_01_24_cleaned['Year'] = ev_cat_01_24_cleaned['Date'].dt.year

# Total number of EV produced each year
ev_cat_01_24_cleaned['Total_EV_Produced'] = ev_cat_01_24_cleaned.iloc[ :,1:-1].sum(axis=1)
total_ev_manufactured_per_year = ev_cat_01_24_cleaned.groupby('Year')['Total_EV_Produced'].sum()
#calculating percentage growth
print(total_ev_manufactured_per_year)
epct_change=total_ev_manufactured_per_year.pct_change()*100
print(epct_change.to_markdown())



# Total EV produced
total_ev_produced = ev_cat_01_24_cleaned['Total_EV_Produced'].sum()

# Calculating percentage contribution of each category 
for category in ev_cat_01_24_cleaned.columns[1:16]:
    category_sum = ev_cat_01_24_cleaned[category].sum()
    percentage_contribution = (category_sum / total_ev_produced) * 100
    print(category,":",category_sum,":",percentage_contribution.round(4))

#Total chargers across all states
total_chargers = Operational_PC['No. of Operational PCS'].sum()
print("Total chargers across all states:", total_chargers)

#Percentage of chargers present in each state
Operational_PC['Percentage Contribution'] = (Operational_PC['No. of Operational PCS'] / total_chargers) * 100
print(Operational_PC[['State', 'Percentage Contribution']].round(2).sort_values(by='Percentage Contribution', ascending=False).to_string(index=False))

# Calculate the percentage contribution of each class in total registration
print(Vehicle_class['Total Registration'].sum())
Vehicle_class["Perc contribution"]=(Vehicle_class['Total Registration']/Vehicle_class['Total Registration'].sum())*100
print(Vehicle_class[['Vehicle Class','Perc contribution']])



