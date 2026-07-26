# Import necessary libraries
from flask import Flask, request, jsonify  # For creating the Flask API
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation

# Initialize the Flask application
sales_predictor_api = Flask("Sales Predictor for the Store")

# Load the trained machine learning model
model = joblib.load("tuned_xgb_model.joblib")

# Define a route for the home page (GET request)
@sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@sales_predictor_api.post('/v1/sales')
def predict_sales_price():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()
    print(property_data)
    # Extract relevant features from the JSON data
    sample = {
        'Store_Id': property_data['Store_Id'],
        'Store_Type': property_data['Store_Type'],
        'Product_Type': property_data['Product_Type'],
        'Product_MRP': property_data['Product_MRP'],
        'Product_Weight': property_data['Product_Weight'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales_price = model.predict(input_data)[0]

    # Convert predicted_sales_price to Python float
    predicted_sales_price = round(float(predicted_sales_price), 2)
    # The conversion above is needed as model predictions are NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_sales_price})


# Define an endpoint for batch prediction (POST request)
@sales_predictor_api.post('/v1/salesbatch')
def predict_sales_price_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame
    predicted_sales_prices = model.predict(input_data).tolist()

    # Round predicted prices
    predicted_prices = [round(float(price), 2) for price in predicted_sales_prices]

    # Create a dictionary of predictions with product IDs as keys
    product_ids = input_data['Product_Id'].tolist()  # 'Product_Id' is the product ID column
    output_dict = dict(zip(product_ids, predicted_prices))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_predictor_api.run(debug=True)
