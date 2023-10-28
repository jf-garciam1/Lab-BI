from joblib import load

class Model:

    def __init__(self):
        self.model = load("assets/tratamientoD.joblib")

    def make_predictions(self, data):
        X_tfidf = self.model.named_steps['tfidf'].transform(data["Textos_espanol"])

        data['sdg']  = self.model.named_steps['svm_model'].predict(X_tfidf)

        return data
