import pickle
import numpy as np

class Predictor:

    def __init__(self, model_folder):
        self.viewModel = pickle.load(open(model_folder+'/viewPredictor.sav', 'rb'))
        self.likeModel = pickle.load(open(model_folder+'/likePredictor.sav', 'rb'))
        self.commentModel = pickle.load(open(model_folder+'/commentPredictor.sav', 'rb'))

    def predictViews(self, values):
        # print(values)
        return  int(self.viewModel.predict(np.array([values]))[0])

    def predictLikes(self, values):
        # print(values)
        return  int(self.likeModel.predict(np.array([values]))[0])

    def predictComments(self, values):
        # print(values)
        return  int(self.commentModel.predict(np.array([values]))[0])

if __name__ == "__main__":
    result = predict('models/randomForestClassifier.sav', [24, 3342, 886, 336, False, False, False])
    print(result)