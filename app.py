from flask import Flask, request, render_template
import pandas as pd

# Initialize Flask application
application = Flask(__name__)
app = application

# Load dataset
data_path = "Z:\\Data Science\\stock price prediction\\notebook\\data\\nifty 50.csv"  # Replace with your dataset file path
stock_data = pd.read_csv(data_path)

# Preprocess data: Ensure the 'Date' column is in datetime format
stock_data['Date'] = pd.to_datetime(stock_data['Date'])

# Route for the home page
@app.route('/')
def index():
    # Get unique stock names for the dropdown
    stock_names = stock_data['Stock Name'].unique()
    return render_template('index.html', stock_names=stock_names)

# Route for prediction (displaying close price)
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'GET':
        # Get unique stock names for the dropdown
        stock_names = stock_data['Stock Name'].unique()
        return render_template('home.html', stock_names=stock_names)

    elif request.method == 'POST':
        stock_name = request.form.get('stock_name')
        selected_date = request.form.get('date')

        try:
            # Filter the dataset for the selected stock name and date
            filtered_data = stock_data[
                (stock_data['Stock Name'] == stock_name) &
                (stock_data['Date'] == pd.to_datetime(selected_date))
            ]

            # Check if data exists for the selection
            if not filtered_data.empty:
                close_price = filtered_data['Close'].values[0]
                message = f"The close price for {stock_name} on {selected_date} is {close_price}."
            else:
                message = f"No data available for {stock_name} on {selected_date}."

        except Exception as e:
            message = f"An error occurred: {str(e)}"

        # Render the result
        return render_template('home.html', stock_names=stock_data['Stock Name'].unique(), message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
