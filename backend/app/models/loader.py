from keras.models import load_model
import pickle


def load_model_ann_ult_score():
    ann = load_model('app/models/ann-ult-score.h5')
    return ann

def load_model_linear_regression():
    return pickle.load(open('app/models/linear-reg.pkl', 'rb'))

def load_model_rfr_general_score():
    return pickle.load(open('app/models/rfr-general-score.pkl', 'rb'))

