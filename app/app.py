import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Loading data
df = pd.read_csv('../data/avito_clean.csv')  # or the filtered dataset

# Loading the trained models
linear_model = joblib.load("models/linear_model.pkl")
rf_model = joblib.load("models/random_forest_model.pkl")
dt_model = joblib.load("models/decision_tree_model.pkl")
kn_model = joblib.load("models/knn_model.pkl")

# Streamlit screen layout
st.title("Estimation du prix de voiture pour les annonces d'avito 🚗💰")
st.write("L'estimation du prix est basé seulement sur la marque, modéle, type de carburant et l'age de voiture. Le kilométrage de voiture est n'est pas pris en consideration.")
st.space()
st.space()

# Storing the infos needed
brands = sorted(df['marque'].dropna().unique())
brand = st.selectbox("Marque", brands)

models = sorted(df[df['marque'] == brand]['modele'].dropna().unique())
model = st.selectbox("Modéle", models)

years = sorted(df['annee'].dropna().unique(), reverse=True)
year = st.selectbox("Année", years)

fuel_types = df['carburant'].dropna().unique()
fuel = st.selectbox("Type de carburant", fuel_types)

st.space()

# Predicting the price
if st.button("Estimer le prix"):
    car_df = pd.DataFrame([{
        'marque': brand,
        'modele': model,
        'car_age': 2026 - year,
        'carburant': fuel
        # 'kilometrage': mileage
    }])

    # Predictions
    line_pred = linear_model.predict(car_df)[0]
    rf_pred = rf_model.predict(car_df)[0]
    dt_pred = dt_model.predict(car_df)[0]
    kn_pred = kn_model.predict(car_df)[0]
    mean_price = (line_pred + rf_pred + dt_pred + kn_pred) / 4
    max_price = mean_price + 0.1 * mean_price
    min_price = mean_price - 0.1 * mean_price
    st.subheader("Prix éstimé:")
    st.write(f"Vous devez payer entre: {round(min_price):,} DH et {round(max_price):,} DH.")
st.space()
# showing results
if st.checkbox("Afficher le resultat par model:"):
    car_df = pd.DataFrame([{
        'marque': brand,
        'modele': model,
        'car_age': 2026 - year,
        'carburant': fuel
        # 'kilometrage': mileage
    }])

    line_pred = linear_model.predict(car_df)[0]
    rf_pred = rf_model.predict(car_df)[0]
    dt_pred = dt_model.predict(car_df)[0]
    kn_pred = kn_model.predict(car_df)[0]
    mean_price = (line_pred + rf_pred + dt_pred + kn_pred) / 4
    max_price = mean_price + 0.1 * mean_price
    min_price = mean_price - 0.1 * mean_price

    st.write(f"**Modéle Rgression linéere:** {round(line_pred):,} DH")
    st.write(f"**Modéle Random Forest:** {round(rf_pred):,} DH")
    st.write(f"**Modéle Decision Tree:** {round(dt_pred):,} DH")
    st.write(f"**Modéle K-Nearest Neighbors:** {round(kn_pred):,} DH")

    st.space()
# Showing additinal data about the price of the model chosen through the years 
if st.checkbox("Afficher les prix de ce modéle selon l'année:"):
    st.write(f"fluctuation du prix de {brand} {model}:")
    prices = df.dropna(subset=['modele', 'annee'])
    prices = prices[(prices['marque'] == brand) & (prices['modele'] == model)]
    prices = prices.groupby('annee')['prix'].median().sort_index()
    st.line_chart(prices)

st.space()
st.space()


# Some statistics of the market
st.title("**Statistiques du marché:**")
st.space()

st.write("Les marques les plus annoncés (Top 10):")
top_brands = df['marque'].value_counts().head(10)
st.bar_chart(top_brands)
st.space()

st.write("Les marques les plus annoncés (Top 10):")
top_models = df['modele'].value_counts().head(10)
st.bar_chart(top_models)
st.space()

st.write("Les ville avec le nombre d'annonces (Top 15):")
top_cities = (df['ville'].value_counts().sort_values(ascending=False).head(15))
st.bar_chart(top_cities)
st.space()

st.write("Ratio de type de transmission:")
transmissions = df['transmission'].dropna().value_counts()
fig, ax = plt.subplots()
ax.pie(transmissions, labels=transmissions.index, autopct='%1.1f%%', startangle=180)
ax.axis('equal')
st.pyplot(fig)

st.write("Ratio de type de carbirant:")
fuel = df['carburant'].dropna().value_counts()
fig, ax = plt.subplots()
ax.pie(fuel, labels=fuel.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)
