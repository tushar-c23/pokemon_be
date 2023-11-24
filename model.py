import pandas as pd
import pickle

def predict_legendaryStatus(pokemon):
    pkl_filename = "pipeline.pkl"

    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)

    prediction = model.predict(pokemon)[0].item()

    return prediction