import random
import pickle
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
import pandas as pd

dangerous = ["Ethanol"]

def predict_class(df):
    pickle_in = open("tsfresh.pickle","rb")
    filtered_fc_parameters = pickle.load(pickle_in)
    X_final_features = extract_features(df,
                     column_id='id', column_sort='time',
                     kind_to_fc_parameters=filtered_fc_parameters,
                     impute_function= impute)
    scaler = pickle.load(open('scaler.sav','rb'))
    X_real = scaler.transform(X_final_features)
    X_real = pd.DataFrame(X_real)
    X_real.columns = X_final_features.keys()
    model = pickle.load(open('model.sav','rb'))
    y_pred_filtered = model.predict(X_real)
    smell_class = y_pred_filtered[0]
    if smell_class in dangerous:
        return smell_class, "Dangerous"
    else:
        return smell_class, "Normal"
