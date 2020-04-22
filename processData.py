import pandas as pd
import numpy as np
import json


class Processor:

    def __init__(self, path):
        try:
            self.df = pd.read_csv(path)
            self.df["description"] = self.df["description"].fillna(value="")
        except Exception as e:
            print('error reading dataset...')

    def getVideosData(self):
        return self.df