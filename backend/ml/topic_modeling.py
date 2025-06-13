from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_topics(texts, n_topics=3):
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(texts)
    svd = TruncatedSVD(n_components=n_topics)
    svd.fit(X)
    return svd.components_
