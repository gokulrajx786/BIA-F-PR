# -*- coding: utf-8 -*-
"""NEW.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_fnCH-ScwniJvrXxlI1N35JKgLosYabB
"""




!pip install streamlit

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score

# Streamlit UI
st.title("Automated Data Analysis and Machine Learning Pipeline")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
    st.write("### Preview of the Uploaded Dataset:")
    st.write(data.head())

    # Data Cleaning Options
    st.sidebar.title("Data Cleaning Options")
    if st.sidebar.checkbox("Handle Missing Values"):
        impute_method = st.sidebar.selectbox("Imputation Method", ["Mean", "Median", "Drop"])
        for col in data.select_dtypes(include=np.number).columns:
            if data[col].isnull().sum() > 0:
                if impute_method == "Mean":
                    data[col].fillna(data[col].mean(), inplace=True)
                elif impute_method == "Median":
                    data[col].fillna(data[col].median(), inplace=True)
                elif impute_method == "Drop":
                    data.dropna(inplace=True)

    if st.sidebar.checkbox("Remove Duplicates"):
        data.drop_duplicates(inplace=True)

    if st.sidebar.checkbox("Convert Categorical to Numeric"):
        encoder = LabelEncoder()
        for col in data.select_dtypes(include=["object"]).columns:
            data[col] = encoder.fit_transform(data[col])

    st.write("### Cleaned Dataset Preview:")
    st.write(data.head())

    # Exploratory Data Analysis (EDA)
    st.sidebar.title("Exploratory Data Analysis")
    if st.sidebar.checkbox("Show Summary Statistics"):
        st.write(data.describe())

    if st.sidebar.checkbox("Correlation Matrix"):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Visualization
    st.sidebar.title("Visualization")
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Histogram", "Scatter Plot", "Box Plot"])
    if plot_type == "Histogram":
        column = st.sidebar.selectbox("Select Column", data.columns)
        fig = px.histogram(data, x=column)
        st.plotly_chart(fig)
    elif plot_type == "Scatter Plot":
        x_axis = st.sidebar.selectbox("X-axis", data.columns)
        y_axis = st.sidebar.selectbox("Y-axis", data.columns)
        fig = px.scatter(data, x=x_axis, y=y_axis)
        st.plotly_chart(fig)
    elif plot_type == "Box Plot":
        column = st.sidebar.selectbox("Select Column", data.columns)
        fig = px.box(data, y=column)
        st.plotly_chart(fig)

    # Machine Learning Model Selection
    st.sidebar.title("Machine Learning")
    task_type = st.sidebar.radio("Select Task", ["Classification", "Regression"])
    target_column = st.sidebar.selectbox("Select Target Column", data.columns)
    X = data.drop(columns=[target_column])
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    if task_type == "Classification":
        model = RandomForestClassifier()
    else:
        model = RandomForestRegressor()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    st.write("### Model Performance")
    if task_type == "Classification":
        st.write("Accuracy:", accuracy_score(y_test, y_pred))
        st.text("Classification Report:\n" + classification_report(y_test, y_pred))
    else:
        st.write("Mean Squared Error:", mean_squared_error(y_test, y_pred))
        st.write("R-squared Score:", r2_score(y_test, y_pred))

    st.write("### Actual vs Predicted Plot")
    fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Actual', 'y': 'Predicted'}, title="Actual vs Predicted Values")
    st.plotly_chart(fig)

with open("requirements.txt", "w") as f:
    f.write("streamlit\npandas\nnumpy\nscikit-learn\nplotly")
from google.colab import files
files.download("requirements.txt")

