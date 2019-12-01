import random
import pandas as pd

def predict_class(dataframe):
    smell_classes = ["Air", "Lime", "Vodka", "Beer", "Vinegar", "Wine", "Acetone", "Ethanol", "Isopropanol"]
    smell_class = random.choice(smell_classes)

    if smell_class == "Isopropanol":
        return smell_class, "Dangerous"
    else:
        return smell_class, "Normal"
