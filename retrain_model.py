import pandas as pd
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv("final_data.csv")

# Get features and target
X = df[['PM2.5', 'NO2', 'CO', 'SO2', 'O3']]
y = df['AQI']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a Decision Tree Regressor model
regressor = DecisionTreeRegressor(random_state=42)
regressor.fit(X_train, y_train)

# Save the model
data = {"model": regressor}
with open('model.pkl', 'wb') as file:
    pickle.dump(data, file)

print("Model trained and saved successfully!") 