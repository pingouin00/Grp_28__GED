from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

class DocumentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = KNeighborsClassifier(n_neighbors=3)

    def fit(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict(self, text):
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]
