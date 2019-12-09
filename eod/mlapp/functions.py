import random
import pandas as pd

dangerous = ["Ethanol"]
def predict_class(dataframe):
    smell_classes = ["Air", "Vinegar", "Acetone", "Ethanol"]
    smell_class = random.choice(smell_classes)

    if smell_class in dangerous:
        return smell_class, "Dangerous"
    else:
        return smell_class, "Normal"
