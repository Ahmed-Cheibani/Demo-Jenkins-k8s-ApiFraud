from flask import Flask
from flask_cors import CORS
from flask import Flask ,jsonify,request
from Adapter import Adapter 
from Fraud_detection import Fraud_detection
import os
import json
import warnings
warnings.filterwarnings('ignore')
app = Flask(__name__)
CORS(app)



@app.route('/',methods=['GET','POST'])
def all_categories():
    return jsonify( {"about":'Hello World!'})

@app.route('/transaction_fraud_detection',methods=['GET','POST'])
def predict_transaction():
    if(request.method=='POST'):
        transaction = adapter.read_data_andparse_to_df(request)
        transaction = fraud_detection.prepare_data(transaction)
        return fraud_detection.prediction(transaction)

@app.route('/transactions_fraud_detection',methods=['GET','POST'])
def predict_transactions():
    if(request.method=='POST'):
        result = {}
        predictions = []
        transactions = adapter.read_data_andparse_to_dfs(request)
        for elem in transactions:
            transaction = fraud_detection.prepare_data(elem)
            predictions.append(fraud_detection.prediction(transaction))
        result['predictions'] = predictions
        return json.dumps(result)

if __name__ == '__main__':
    
    adapter = Adapter()
    fraud_detection  = Fraud_detection()
    app.run(host='0.0.0.0',debug=False)