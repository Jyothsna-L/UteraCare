import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import numpy as np

# Load dataset
df = pd.read_csv("C:/Users/Asus/Downloads/PCOD dataset.csv")

# Convert categorical "Unusual_Bleeding" into numeric (yes=1, no=0)
df["Unusual_Bleeding"] = df["Unusual_Bleeding"].map({"yes": 1, "no": 0})

# Select only the 5 features
X = df[["Age", "Height", "Weight", "Unusual_Bleeding"]].apply(pd.to_numeric, errors="coerce")
X = X.fillna(0)
y = ((df["BMI"] > 25) | (df["Unusual_Bleeding"] == 1)).astype(int)   # simple target rule

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model
with open("pcod_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained & saved as pcod_model.pkl")
