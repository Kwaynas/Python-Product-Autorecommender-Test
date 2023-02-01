# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:37:42 2023

@author: cdcaq
"""
import pickle
from flask import Flask, request, json, jsonify
import numpy as np
import pandas as pd
import ast
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from thefuzz import fuzz
from thefuzz import process
import math
import json
import requests

 
data = pd.read_csv('Raw Database.csv')
data['Description'] = data['Description'].str.strip()
data = data[~data['InvoiceNo'].str.contains('C')]

items = data['Description'][data['Country'] =="Portugal"].unique()

basket_Por = (data[data['Country'] =="Portugal"]
        .groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('InvoiceNo'))

basket_Por = pd.get_dummies(basket_Por).astype(bool)

frq_items_Por = apriori(basket_Por, min_support = 0.04, use_colnames = True)
rules_Por = association_rules(frq_items_Por, metric ="lift", min_threshold = 1)
rules_Por = rules_Por.sort_values(['confidence', 'lift'], ascending =[False, False])


app = Flask(__name__)
 
@app.route('/productreco', methods=['POST'])
def predict():
    entry = request.json
    
    # get the rules for this antecedent
    antecedent = entry['Description']
    max_results = entry['MaxRes']
    rules = rules_Por
    temp = set()
    temp.add(antecedent)
    
    preds = rules[rules['antecedents'] == temp]
    try:
        value = preds['confidence'].iloc[:max_results].unique().mean()
    finally:
        pass
    # a way to convert a frozen set with one element to string
    preds = preds['consequents'].apply(iter).apply(next)
    pred_list = dict.fromkeys('a', list(preds.iloc[:max_results].unique()))
    pred_list['b'] = value
    return jsonify(pred_list)




# def predict():
#     #---get the features to predict---
#     features = request.json
 
#     #---create the features list for prediction---
#     features_list = [features["Glucose"],
#                      features["BMI"],
#                      features["Age"]]
 
#     #---get the prediction class---
#     prediction = loaded_model.predict([features_list])
 
#     #---get the prediction probabilities---
#     confidence = loaded_model.predict_proba([features_list])
 
#     #---formulate the response to return to client---
#     response = {}
#     response['prediction'] = int(prediction[0])
#     response['confidence'] = str(round(np.amax(confidence[0]) * 100 ,2))
 
#     return  jsonify(response)



 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)