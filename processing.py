import pickle
import numpy as np

def get_prediction(qty, receive_time, output_today, output_time, supply_volume):
    with open("models/model_y1.pkl", "rb") as f:
        model_y1 = pickle.load(f)

    with open("models/model_y2.pkl", "rb") as f:
        model_y2 = pickle.load(f)

    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    
    params = np.array([[receive_time], [output_time], [qty], [supply_volume], [output_today]])
    params = scaler.transform(params)

    y1 = model_y1.predict(params)
    y2 = model_y2.predict(params)

    return {"delivery_day": y1, "ride_number": y2}