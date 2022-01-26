import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from dataProcess import rawText2fv

##creating a flask app and naming it "app"
app = Flask('app')
CORS(app)

@app.route('/test', methods=['GET'])
def test():
    response = jsonify({'Response': 'Pinging Model Application!!'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()    
    text = input_data["text"]
    
    fv_text, segmented_units = rawText2fv(text)
        
    with open('hardVoting.bin', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()
        
    predictions = model.predict(fv_text)

    text_units = [str(i) for i in segmented_units]

    result = {
        'predictions': list(zip(predictions.tolist(), text_units))
    }
    
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#Run local the app
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=9696)