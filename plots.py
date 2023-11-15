import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = pd.read_csv('milknew.csv')

milk_data = data
# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating subplots
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 15))

# List of numeric and categorical columns for plotting
numeric_columns = ['pH', 'Temprature', 'Colour']
categorical_columns = ['Taste', 'Odor', 'Fat ', 'Turbidity', 'Grade']

# Plotting distributions of numeric columns
for i, col in enumerate(numeric_columns):
    sns.histplot(milk_data[col], ax=axes[i, 0], kde=True)

# Plotting countplots for categorical columns
for i, col in enumerate(categorical_columns):
    sns.countplot(x=col, data=milk_data, ax=axes[i // 2, (i % 2) + 1])

# Adjusting the layout
plt.tight_layout()

# Show the plots
plt.show()
# Function to plot boxplot for numerical features against the Grade
def plot_boxplot(df, feature):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Grade', y=feature, data=df)
    plt.title(f'Boxplot of {feature} by Milk Quality Grade')
    plt.show()

# Plotting boxplots for some numerical features
plot_boxplot(milk_data, 'pH')
plot_boxplot(milk_data, 'Temprature')

# Function to plot countplot for categorical features against the Grade
def plot_countplot(df, feature):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=feature, hue='Grade', data=df)
    plt.title(f'Count of {feature} by Milk Quality Grade')
    plt.show()

# Plotting countplots for some categorical features
plot_countplot(milk_data, 'Taste')
plot_countplot(milk_data, 'Odor')

