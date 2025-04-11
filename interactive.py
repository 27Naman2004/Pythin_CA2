import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
data = pd.read_excel("python.xlsx")


# Menu
print("\n📊 Choose an Objective to Visualize:\n")
print("1. Histogram of Pollutant Average")
print("2. Bar Chart - Avg Pollution by City")
print("3. Scatter Plot - Pollution by City and Type")
print("4. Top 10 Most Polluted Cities")
print("5. Box Plot - Outlier Detection")
print("6. Pie Chart - Pollution Types")
print("7. Correlation Heatmap")
print("8. IQR calculation")


choice = input("\nEnter your choice (1-8): ")

# data analysis and cleaning 

# Show first 5 rows
print("HEAD (First 5 rows):\n")
print(data.head(),"\n")

# Show last 5 rows
print("\nTAIL (Last 5 rows):\n")
print(data.tail(),"\n")

# General info about dataset
data.info()  


# Gernal Discription Of the DataDet
print("\nDATASET Discription:\n")
print(data.describe() ,"\n")

print("\nMissing values in each column:\n")
print(data.isnull().sum())

# Fill missing values in numeric columns with the average value (mean)
pollutant_min_mean = data['pollutant_min'].mean()
data['pollutant_min'] = data['pollutant_min'].fillna(pollutant_min_mean)

pollutant_max_mean = data['pollutant_max'].mean()
data['pollutant_max'] = data['pollutant_max'].fillna(pollutant_max_mean)

pollutant_avg = data['pollutant_avg'].mean()
data['pollutant_avg'] = data['pollutant_avg'].fillna(pollutant_avg)

# Remove duplicate rows if any are there
data = data.drop_duplicates()

# Objective 1
if choice == "1":
    plt.hist(data['pollutant_avg'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Pollutant Average Distribution')
    plt.xlabel('Pollutant Avg')
    plt.ylabel('Count')
    plt.grid(True)
    plt.show()

# Objective 2
elif choice == "2":
    city_avg = data.groupby('city')['pollutant_avg'].mean()
    plt.figure(figsize=(14, 6))
    plt.bar(city_avg.index, city_avg.values, color='orange')
    plt.title('City vs Pollution Average')
    plt.xlabel('City')
    plt.ylabel('Pollution Average')
    plt.xticks(rotation=75, ha='right')
    plt.show()

# Objective 3: Pollution Types in Top 20 Most Polluted Cities

elif choice == "3":
    city_avg = data.groupby('city')['pollutant_avg'].mean().sort_values(ascending=False)
    top_20_cities = city_avg.head(20).index  # get city names

    top20_data = data[data['city'].isin(top_20_cities)]

    plt.figure(figsize=(14, 6))

    for pol_type in top20_data['pollutant_id'].unique():
        pol_data = top20_data[top20_data['pollutant_id'] == pol_type]
        plt.scatter(pol_data['city'], pol_data['pollutant_avg'], label=pol_type)

    # Add labels and title
    plt.title('Pollution Type in Top 20 Most Polluted Cities')
    plt.xlabel('City')
    plt.ylabel('Pollutant Average')
    plt.xticks(rotation=90)
    plt.legend() 
    plt.tight_layout()
    plt.show()


# Objective 4
elif choice == "4":
    city_avg = data.groupby('city')['pollutant_avg'].mean()
    top_10 = city_avg.sort_values()[-10:]  # no ascending=False
    plt.bar(top_10.index, top_10.values, color='red')
    plt.title('Top 10 Polluted Cities')
    plt.xlabel('City')
    plt.ylabel('Avg Pollution')
    plt.xticks(rotation=45)
    plt.show()

# Objective 5
elif choice == "5":
    plt.boxplot(data['pollutant_avg'], vert=False)
    plt.title('Pollutant Avg - Outlier Check')
    plt.xlabel('Pollutant Avg')
    plt.grid(True)
    plt.show()

# Objective 6
elif choice == "6":
    pollution_type = data['pollutant_id'].value_counts()
    plt.figure(figsize=(6, 6))
    slices, texts = plt.pie(pollution_type, labels=None)
    for i in range(len(pollution_type)):
        plt.text(slices[i].get_center()[0]*0.6,
                 slices[i].get_center()[1]*0.6,
                 str(pollution_type.values[i]),
                 ha='center', va='center')
    plt.legend(pollution_type.index, title="Pollutants", loc="best")
    plt.title('Pollution Types')
    plt.show()

# Objective 7
elif choice == "7":
    small = data[['pollutant_min', 'pollutant_max', 'pollutant_avg']]
    corr = small.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation between Pollutant Levels')
    plt.show()
    
elif choice == "8":
    
    # Calculate 25th and 75th percentile using NumPy
    Q1 = np.percentile(data['pollutant_avg'], 25)
    Q3 = np.percentile(data['pollutant_avg'], 75)

    # Calculate IQR
    IQR = Q3 - Q1

    # Calculate lower and upper bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter data to get outliers only
    outliers = data[(data['pollutant_avg'] < lower_bound) | (data['pollutant_avg'] > upper_bound)]

    # Show outlier values
    print("\n📌 Outlier values based on 'pollutant_avg':\n")
    print(outliers[['city', 'pollutant_id', 'pollutant_avg', 'last_update']])

    # Filter data to remove outliers
    data_no_outliers = data[(data['pollutant_avg'] >= lower_bound) & (data['pollutant_avg'] <= upper_bound)]

    # Plot histogram after removing outliers
    plt.figure(figsize=(8, 6))
    sns.histplot(data_no_outliers['pollutant_avg'], kde=True, color='green')
    plt.title('Pollutant Average Distribution (Outliers Removed)')
    plt.xlabel('Pollutant Average')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    

else:
    print("Invalid choice! Please enter a number between 1 and 7.")
