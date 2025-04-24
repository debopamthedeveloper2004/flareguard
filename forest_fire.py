import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import pickle

# Load and prepare data
data = pd.read_csv("forest_fire.csv")
X = data[['Temperature', 'Humidity', 'Wind_Speed', 'Precipitation']]
y = data['Fire_Occurrence']

# Create pipeline with scaling and model
model = make_pipeline(
    StandardScaler(),
    RandomForestClassifier(n_estimators=100, random_state=42)
)

# Train model
model.fit(X, y)

# Save the trained model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
