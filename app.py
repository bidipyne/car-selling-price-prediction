from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    fuel_type_diesel = 0
    fuel_type_petrol = 0
    if request.method == 'POST':
        year = int(request.form['year'])
        present_price = float(request.form['price'])
        km_driven = int(request.form['km_driven'])
        owner = int(request.form['owner'])
        fuel_type = request.form['fuel_type']
        if fuel_type == 'Petrol':
            fuel_type_petrol = 1
        elif fuel_type == 'Diesel':
            fuel_type_diesel = 1
        year = 2020 - year
        trans_manual = request.form['trans_type']
        if trans_manual == 'Manual':
            trans_manual = 1
        else:
            trans_manual = 0
        seller_type_indivi = request.form['seller_type']
        if seller_type_indivi == 'Individual':
            seller_type_indivi = 1
        else:
            seller_type_indivi = 0
        prediction = model.predict([[present_price,km_driven,owner,year,fuel_type_diesel,
                                    fuel_type_petrol,seller_type_indivi,trans_manual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))

if __name__=="__main__":
    app.run(debug=True)