# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 22:07:40 2022

@author: vadla
"""
# importing the necessary dependencies
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle


app = Flask(__name__) # initializing a flask app
model = pickle.load(open('CKD.pkl', 'rb')) #loading the model

@app.route('/')# route to display the home page
def home():
    return render_template('home.html') #rendering the home page
@app.route('/Prediction',methods=['POST','GET'])
def prediction():
    return render_template('indexnew.html')
@app.route('/Home',methods=['POST','GET'])
def my_home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])# route to show the predictions in a web UI
def predict():
    blood_urea = request.form["blood_urea"]
    blood_glucose_random = request.form["blood glucose random"]
    anemia = request.form["anemia"]
    coronary_artery_disease = request.form["coronary_artery_disease"]
    pus_cell = request.form["pus_cell"]
    red_blood_cells = request.form["red_blood_cells"]
    diabetesemellitus = request.form["diabetesemellitus"]
    pedal_edema = request.form["pedal_edema"]
    if(anemia == "YES"):
        anemia = 1
    if(anemia == "NO"):
        anemia = 0
    
    if(coronary_artery_disease == "YES"):
        coronary_artery_disease = 1
    if(coronary_artery_disease == "NO"):
        coronary_artery_disease = 0
    
    if(pus_cell == "abnormal"):
        pus_cell = 1
    if(pus_cell == "normal"):
        pus_cell = 0
        
    if(red_blood_cells == "abnormal"):
        red_blood_cells = 1
    if(red_blood_cells == "normal"):
        red_blood_cells = 0
        
    if(diabetesemellitus == "YES"):
        diabetesemellitus = 1
    if(diabetesemellitus == "NO"):
        diabetesemellitus = 0
    
    if(pedal_edema == "YES"):
        pedal_edema == 1
    if(pedal_edema == "NO"):
        pedal_edema == 0
    t = [[float(blood_urea),float(blood_glucose_random),str(anemia),str(coronary_artery_disease),str(pus_cell),str(red_blood_cells),str(diabetesemellitus),str(pedal_edema)]]
    print(t)
    payload_scoring = {"input_data": [{"field": [["blood_urea","blood glucose random","anemia","coronary_artery_disease","pus_cell","red_blood_cells","diabetesemellitus","pedal_edema"]], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3d42cf89-772b-4bc2-a87d-22e7f5559234/predictions?version=2022-08-02', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    if (pred == 0):
        print("you have kidney disease")
    else:
        print("you don't have any kidney disease")
    #reading the inputs given by the user
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    
    features_name = ['blood_urea', 'blood glucose random', 'anemia',
       'coronary_artery_disease', 'pus_cell', 'red_blood_cells',
       'diabetesmellitus', 'pedal_edema']
    
    df = pd.DataFrame(features_value, columns=features_name)
    
    # predictions using the loaded model file
    output = model.predict(df)

    # showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('result.html', prediction_text=output)

if __name__ == '__main__':
    # running the app
    app.run(debug=False)


