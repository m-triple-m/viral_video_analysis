import pandas as pd
import numpy as np
import json


class Processor:

    def __init__(self, path, category_path):
        
        try:
            self.df = pd.read_csv(path)
            self.df["description"] = self.df["description"].fillna(value="")

            with open(category_path) as f:
                self.categories = json.load(f)["items"]

        except Exception as e:
            print('error reading dataset...')

    def getTitleLength(self):
        self.df["title_length"] = self.df["title"].apply(lambda x: len(x))
        return self.df

    def getVideosData(self):
        return self.df

    def getCategoryNames(self):
        cat_dict = {}
        for cat in self.categories:
            cat_dict[int(cat["id"])] = cat["snippet"]["title"]
        self.df['category_name'] = self.df['category_id'].map(cat_dict)

        cdf = self.df["category_name"].value_counts().to_frame().reset_index()
        cdf.rename(columns={"index": "category_name", "category_name": "No_of_videos"}, inplace=True)
        print(cdf.columns)

        return cdf