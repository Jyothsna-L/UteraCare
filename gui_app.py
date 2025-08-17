import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
import pickle
import pandas as pd
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

model_path = resource_path("pcod_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)
with open("pcod_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict():
    try:
        age = int(entry_age.get())
        height = float(entry_height.get())
        weight = float(entry_weight.get())
        unusual = entry_unusual.get().lower()

        unusual = 1 if unusual in ["yes", "1", "true"] else 0

        # BMI
        bmi = round(weight / ((height / 100) ** 2), 2)
        label_bmi_val.config(text=f"{bmi}")

        # input
        X_input = pd.DataFrame([[age, height, weight, unusual]],
                               columns=["Age", "Height", "Weight", "Unusual_Bleeding"])

        prediction = model.predict(X_input)[0]

        if prediction == 1:
            result = "High chance of PCOD"
        else:
            result = "Low chance of PCOD"

        recs = get_recommendations(age, bmi, unusual)

        messagebox.showinfo(
            "Prediction Result",
            f"{result}\n\nBMI: {bmi}\n\nLifestyle Recommendations:\n- " + "\n- ".join(recs)
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def get_recommendations(age, bmi, unusual_bleeding):
    recs = []
    if bmi < 18.5:
        recs.append("Increase calorie intake with a balanced diet.")
    elif 18.5 <= bmi <= 24.9:
        recs.append("Maintain your healthy weight with regular exercise.")
    else:
        recs.append("Adopt a low-carb diet and increase physical activity (30 mins daily).")

    if unusual_bleeding == 1:
        recs.append("Consult a gynecologist for irregular cycles and hormonal evaluation.")
    
    if age < 25:
        recs.append("Focus on building healthy long-term habits early.")
    else:
        recs.append("Consider regular health check-ups every 6 months.")
    
    return recs

# gui
root = tb.Window(themename="cosmo")
root.title("PCOD Detection System")
root.geometry("400x300")

# Title
title = tb.Label(root, text="PCOD Detection System", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

# Input frame
frame = tb.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# Age
tb.Label(frame, text="Age:").grid(row=0, column=0, sticky="w", pady=5)
entry_age = tb.Entry(frame, width=15)
entry_age.grid(row=0, column=1)

# Height
tb.Label(frame, text="Height (cm):").grid(row=1, column=0, sticky="w", pady=5)
entry_height = tb.Entry(frame, width=15)
entry_height.grid(row=1, column=1)

# Weight
tb.Label(frame, text="Weight (kg):").grid(row=2, column=0, sticky="w", pady=5)
entry_weight = tb.Entry(frame, width=15)
entry_weight.grid(row=2, column=1)

# Unusual bleeding
tb.Label(frame, text="Unusual Bleeding (yes/no):").grid(row=3, column=0, sticky="w", pady=5)
entry_unusual = tb.Entry(frame, width=15)
entry_unusual.grid(row=3, column=1)

# BMI display
tb.Label(frame, text="BMI:").grid(row=4, column=0, sticky="w", pady=5)
label_bmi_val = tb.Label(frame, text="--")
label_bmi_val.grid(row=4, column=1, sticky="w")

# Predict button
btn_predict = tb.Button(root, text="Predict", bootstyle="primary", command=predict)
btn_predict.pack(pady=15)

root.mainloop()



