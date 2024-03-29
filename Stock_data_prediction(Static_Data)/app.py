"""
@Author: Rikesh Chhetri
@Date: 2021-09-12 
@Last Modified by: Rikesh Chhetri
@Last Modified time: 2021-09-12 10:03:30
@Title : Program Aim perform the plotting of Stock Data Prediction using Flask And HighChartJs
"""

from flask import Flask, request, render_template,make_response
import json
from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegressionModel
from datetime import datetime
spark= SparkSession.builder.appName('Stock Data processing').getOrCreate()


app = Flask(__name__)
model = LinearRegressionModel.load("stock_data_model")
data = spark.read.parquet("test_data")
prediction = model.transform(data)
output = prediction.toPandas()
count = len(output["time"])
index_count = 0

def getData():
    global count
    if index_count <= count:
        print(index_count)
        return int(datetime.strptime(output.loc[index_count, "time"], '%Y-%m-%d %H:%M:%S').strftime('%s')) * 1000, output.loc[index_count, "close"], output.loc[index_count, "prediction"]
  

@app.route('/data', methods=["GET", "POST"])
def data():
    global index_count
    date, Close, prediction = getData()
    data = [date, Close, prediction]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    index_count+=1
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    data = spark.read.parquet("test_data")
    prediction = model.transform(data)
    output = prediction.toPandas()

    return render_template('index.html',tables=[output.to_html(classes='data', header="true")]) 

if __name__ == "__main__":

    app.run(host="0.0.0.0",port=8080)
    
    
