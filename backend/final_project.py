import sys
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import sqlite3
import io
import imageio

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('SELECT csvFile FROM files2')
data = cursor.fetchone()
with open('food_df.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(
        [str(value, 'utf-8') if isinstance(value, bytes) else value for value in data])

with open('food_df.csv', 'r') as input_file, open('output.csv', 'w') as output_file:
    lines = input_file.readlines()
    if lines:
        lines[0] = lines[0][1:]
    if lines and lines[-1].strip() == '"':
        lines.pop()

    output_file.writelines(lines)
arg = sys.argv[0]
print(arg)

cursor.execute('Delete from images')
conn.commit()
conn.close()


superstore_df = pd.read_csv('output.csv', quoting=csv.QUOTE_NONE)
superstore_df_cleaned = superstore_df.dropna()
# column_names = superstore_df.columns.to_numpy()
for column in superstore_df_cleaned.columns:
    plt.figure(figsize=(8, 6))
    sns.histplot(superstore_df_cleaned[column], kde=True)
    print(column)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    service_name = column+" Distribution"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            image_data BLOB,
            service varchar(20)
        )
    ''')
    cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
                   (image_data.read(), service_name))
    conn.commit()
    conn.close()
    # plt.show()
sys.stdout.flush()
# plt.show()

# for column in superstore_df.columns:
#     plt.figure(figsize=(8, 6))
#     plt.pie(superstore_df[column])
#     plt.title(f'Distribution of {column}')
#     plt.xlabel(column)
#     plt.ylabel('Frequency')
#     plt.show()

# if "Age" in column_names:
#     plt.figure(figsize=(12, 6))
#     plt.subplot(1, 2, 1)
#     sns.histplot(data=superstore_df_cleaned, x='Age',
#                  bins=20, kde=True, color='blue')
#     plt.title('Distribution of Age (Year_Birth)')
#     plt.xlabel('Age')
#     plt.ylabel('Frequency')
#     plt.subplot(1, 2, 2)
#     sns.boxplot(data=superstore_df_cleaned, x='Age', color='red')
#     plt.title('Box Plot of Age')
#     plt.xlabel('Age')
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Customer Age Distribution"

#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')

#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("age Image saved to the database.")

# if "Income" in column_names:
#     plt.figure(figsize=(16, 8))
#     plt.subplot(1, 2, 1)
#     sns.histplot(superstore_df_cleaned['Income'],
#                  bins=20, kde=True, color='orange')
#     plt.title('Distribution of Income')
#     plt.xlabel('Income')
#     plt.ylabel('Frequency')
#     plt.subplot(1, 2, 2)
#     sns.histplot(
#         superstore_df_cleaned['MntFishProducts'], bins=20, kde=True, color='brown')
#     plt.title('Distribution of Spending on Fish Products')
#     plt.xlabel('Spending on Fish Products')
#     plt.ylabel('Frequency')

#     # Adjust layout spacing
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Customer Income Distribution"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Create a table to store images (if it doesn't exist)
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()

#     # Close the database connection
#     conn.close()

#     print("customer income Image saved to the database.")

# if "MntMeatProducts" in column_names:
#     plt.figure(figsize=(10, 6))
#     sns.violinplot(data=superstore_df_cleaned,
#                    x=superstore_df_cleaned['MntMeatProducts'])
#     plt.title('Distribution of Spending on Meat Products')
#     plt.xlabel('Spending on Meat Products')
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Meat Spending Distribution"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("meat spending Image saved to the database.")

# if "marital_Married" in column_names:
#     color_palette = sns.color_palette('pastel')
#     plt.figure(figsize=(10, 6))  # Increased figsize
#     sns.countplot(data=superstore_df_cleaned,
#                   x='marital_Married', palette=color_palette)
#     plt.title('Distribution of Marital married customers')
#     plt.xlabel('Marital Status')
#     plt.ylabel('Frequency')
#     plt.xticks([0, 1], ['Unmarried', 'Married'])
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Maratial Status Distribution"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Maratial status Image saved to the database.")

# if "marital_Divorced" in column_names:
#     color_palette = sns.color_palette('pastel')
#     plt.figure(figsize=(10, 6))  # Increased figsize
#     sns.countplot(data=superstore_df_cleaned,
#                   x='marital_Divorced', palette=color_palette)
#     plt.title('Distribution of Divorced customers')
#     plt.xlabel('Marital Status')
#     plt.ylabel('Frequency')
#     plt.xticks([0, 1], ['Not Divorced', 'Divorced'])
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Maratial Status Divorced"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Maratial status Divorced Image saved to the database.")

# if "marital_Single" in column_names:
#     color_palette = sns.color_palette('pastel')
#     plt.figure(figsize=(10, 6))  # Increased figsize
#     sns.countplot(data=superstore_df_cleaned,
#                   x='marital_Single', palette=color_palette)
#     plt.title('Distribution of Divorced customers')
#     plt.xlabel('Marital Status')
#     plt.ylabel('Frequency')
#     plt.xticks([0, 1], ['Not Single', 'Single'])
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Maratial Status Single"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Maratial status Single Divorced Image saved to the database.")

# if "Complain" in column_names:
#     color_palette = sns.color_palette('pastel')  # Choose a color palette
#     plt.figure(figsize=(8, 6))  # Increased figsize
#     sns.countplot(data=superstore_df_cleaned,
#                   x='Complain', palette=color_palette)
#     plt.title('Distribution of Complains')
#     plt.xlabel('Complain')
#     plt.ylabel('Frequency')
#     plt.xticks([0, 1], ['No', 'Yes'])
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Complain Distribution"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("complain distributon Image saved to the database.")

# if "Income" and "Complain" in column_names:
#     plt.figure(figsize=(12, 6))  # Increased figsize
#     sns.barplot(y='Income', x='Complain', data=superstore_df_cleaned)
#     plt.title('Income Of the customers with complain')
#     plt.xlabel('complains')
#     plt.ylabel('Income')
#     plt.xticks(rotation=45)
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Income Distribution Over Complain "

#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("complain and income distributon Image saved to the database.")

# if "MntFishProducts" and "MntMeatProducts" in column_names:
#     color_palette = sns.color_palette(['red', 'blue'])
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(data=superstore_df_cleaned, x='MntFishProducts',
#                     y='MntMeatProducts', color=color_palette[0])
#     plt.title('Scatter Plot: Spending on Fish Products vs. Meat Products')
#     plt.xlabel('Spending on Fish Products')
#     plt.ylabel('Spending on Meat Products')
#     sns.regplot(data=superstore_df_cleaned, x='MntFishProducts',
#                 y='MntMeatProducts', scatter=False, color=color_palette[1])
#     plt.legend(['Data Points', 'Regression Line'])
#     plt.tight_layout()

#     service_name = "Distribution Fish And Meat Product"
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')

#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Distribution Fish And Meat Product Image saved to the database.")

# if "MntMeatProducts" and "Income" in column_names:
#     color_palette = sns.color_palette(['purple', 'green'])
#     plt.figure(figsize=(12, 8))
#     plt.subplot(2, 1, 1)
#     sns.boxplot(data=superstore_df_cleaned,
#                 x=superstore_df_cleaned['MntMeatProducts'], y='Income', palette=color_palette)
#     plt.title(
#         'Box Plot: Distribution of Income across Amount spent on meat products')
#     plt.xlabel('Education Level')
#     plt.ylabel('Income')

#     plt.subplot(2, 1, 2)
#     sns.boxplot(data=superstore_df_cleaned, x='Complain',
#                 y='Recency', palette=color_palette)
#     plt.title('Box Plot: Relationship between Complain and Recency')
#     plt.xlabel('Complain')
#     plt.ylabel('Recency')
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Distribution of Income across Amount spent on meat products"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Distribution_of_Income_across_Amount_spent_on_meat_products Image saved to the database.")

# if "Kidhome" and "MntFruits" and "Teenhome" in column_names:
#     color_palette = sns.color_palette(['purple', 'green', 'blue'])
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='Kidhome', y='MntFruits', hue='Teenhome',
#                 data=superstore_df_cleaned, palette=color_palette)
#     plt.title('Grouped Bar Chart: Spending Behaviors based on Kidhome and Teenhome')
#     plt.xlabel('Kidhome')
#     plt.ylabel('Spending on Fruits')
#     plt.legend(title='Teenhome')
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Spending Behaviors based on Kidhome and Teenhome"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Spending_Behaviors_based_on_Kidhome_and_Teenhome Image saved to the database.")

# if "NumWebPurchases" and "NumWebVisitsMonth" in column_names:
#     plt.figure(figsize=(10, 8))
#     correlation_matrix = superstore_df_cleaned[[
#         'NumWebPurchases', 'NumWebVisitsMonth']].corr()
#     sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
#     plt.title('Correlation Heatmap: No. of WebPurchases vs No. of WebVisitsMonth')
#     plt.xlabel('Variable')
#     plt.ylabel('Variable')

#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "No of WebPurchases vs No. of WebVisitsMonth"

#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')

#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("No_f_WebPurchases_vs_No_of_WebVisitsMonth Image saved to the database.")

# if "Kidhome" and "MntFruits" and "Teenhome" in column_names:
#     color_palette = sns.color_palette(['purple', 'green', 'blue'])
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='Kidhome', y='MntFruits', hue='Teenhome',
#                 data=superstore_df_cleaned, palette=color_palette)
#     plt.title('Grouped Bar Chart: Spending Behaviors based on Kidhome and Teenhome')
#     plt.xlabel('Kidhome')
#     plt.ylabel('Spending on Fruits')
#     plt.legend(title='Teenhome')
#     plt.tight_layout()
#     image_data = io.BytesIO()
#     plt.savefig(image_data, format='png')
#     image_data.seek(0)
#     service_name = "Spending Behaviors based on Kidhome and Teenhome"
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS images (
#             id INTEGER PRIMARY KEY,
#             image_data BLOB,
#             service varchar(20)
#         )
#     ''')
#     cursor.execute('INSERT INTO images (image_data,service) VALUES (?,?)',
#                    (image_data.read(), service_name))
#     conn.commit()
#     conn.close()
#     print("Spending_Behaviors_based_on_Kidhome_and_Teenhome Image saved to the database.")
# plt.show()
# sys.stdout.flush()
