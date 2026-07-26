import streamlit as st
import pandas as pd
import requests
# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Store Sales Price Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Store_Id = st.selectbox("Store ID", ["OUT001", "OUT002", "OUT003", "OUT004"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type2", "Departmental Store", "Supermarket Type1", "Food Mart"])
Product_Type = st.selectbox("Product Type", ["Frozen Foods", "Dairy", "Canned","Baking Goods", "Health and Hygiene", "Snack Foods", "Meat", "Household", "Hard Drinks","Fruits and Vegetables", "Breads", "Soft Drinks", "Breakfast", "Others","Starchy Foods","Seafood"])
Product_MRP = st.number_input("Product MRP", min_value=1, step=1, value=2)
Product_Weight = st.number_input("Product Weight")
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Store_Id': Store_Id,
    'Store_Type': Store_Type,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Price (in dollars)']
        st.success(f"Predicted Sales Price (in dollars): {prediction}")
    else:
        st.error(f"Unable to connect to the prediction API.: {input_data.to_dict(orient='records')[0]}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
