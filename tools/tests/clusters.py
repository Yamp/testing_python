import pickle

import psycopg2
import seaborn as sns
from sklearn.cluster import KMeans

from tools.db.dbtools import get_frame

sns.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from stop_words import get_stop_words


class Ml:
    stop_words = get_stop_words('russian')

    dbc = {'dbname': 'opt', 'user': 'opt', 'password': 'koradmin', 'host': 'srv-pg-test'}

    def __init__(self, n_clusters) -> None:
        super().__init__()
        self.n_clusters = n_clusters

    def connect_to_db(self):
        self.conn = psycopg2.connect(**self.dbc)

    def load_from_db(self):
        print('get data from db')
        self.connect_to_db()
        self.load_tovs_from_db()
        self.X = self.tovs_frm['problem']

    def load_tovs_from_db(self):
        sql = """
        select s.f_text_problem problem from sd_registry s where s.f_date between '01/01/20' and '31/01/20'
        """
        self.tovs_frm = get_frame(sql, connection=self.conn)

    def define_model(self):
        tfidf = TfidfVectorizer(analyzer='word', stop_words=Ml.stop_words, ngram_range=(1, 2))
        self.model = make_pipeline(tfidf, KMeans(n_clusters=self.n_clusters))

    def fit(self):
        print('start fit')
        self.model.fit(self.X)

    def predict_for_test_data(self):
        print('predict_for_test_data')
        self.y_pred = self.model.predict(self.X)
        self.predictions = [round(value) for value in self.y_pred]


if __name__ == '__main__':
    ml = Ml(n_clusters=10)
    ml.load_from_db()
    ml.define_model()
    ml.fit()
    ml.predict_for_test_data()

    s = set(ml.predictions)
    for cls in s:
        if cls == 0:
            continue

        print(f'cls: {cls}-------------------------------------------')
        npp = 0
        for i, p in enumerate(ml.predictions):
            if cls == p:
                npp += 1
                print(npp, ml.X.array[i])
