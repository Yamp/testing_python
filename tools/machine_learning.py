import pickle
import pprint
from pathlib import Path

import pandas as pd
import psycopg2
import seaborn as sns
import xgboost
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

from tools.db.dbtools import get_frame

sns.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from stop_words import get_stop_words
import matplotlib.pyplot as plt


class Ml:
    dir = Path('d:\\1')
    classes_file = dir / 'classes.pickle'
    model_file = dir / 'model_tovs.pickle'
    tovs_file = dir / 'tovs.csv'
    stop_words = get_stop_words('russian')

    dbc = {'dbname': 'opt', 'user': 'opt', 'password': 'koradmin', 'host': 'srv-pg-test'}

    test_tov_names = ['Жираф', 'Жгут Ж1', 'Вытяжка лоролр эжлдж', 'Часы настенные', 'Тарелка керамическая',
                      'Рюмка большая 333',
                      'Коврик для сушки посуды', 'Салатник 500 мл', 'Вварная шпилька M14 x 16',
                      'Caster swivel w/o brake',
                      'Вешалка стандарт', 'Вешалка на стену', 'Ложка Чайная Даша', 'Медвежонок Петя',
                      'Шкатулка керамическая',
                      'Кружка',
                      'Блюдо для блинов', '6/12 Набор кофейный 100мл', 'Кухонная вытяжка ELIKOR Альфа',
                      'Изделие декоративное ', 'Молоток дверной Соня', 'Набор коробок', 'Брелок бабочка', 'Процессор']

    def __init__(self, n=None) -> None:
        super().__init__()
        self.n = n

    def connect_to_db(self):
        self.conn = psycopg2.connect(**self.dbc)

    def load_from_db(self, is_save_to_file=True):
        print('get data from db')
        self.connect_to_db()
        self.load_classes_from_db(is_save_to_file)
        self.load_tovs_from_db(is_save_to_file)
        self.make_train_data()

    def load_from_files(self):
        print('get data from files')
        self.load_classes_from_file()
        self.load_tovs_from_file()
        self.make_train_data()

    def load_tovs_from_file(self):
        self.tovs_frm = pd.read_csv(self.tovs_file)

    def load_classes_from_file(self):
        with open(self.classes_file, 'rb') as f:
            self.classes = pickle.load(f)

    def load_classes_from_db(self, is_save_to_file=True):
        frm = get_frame("select f_cod, f_name from spr_clas", connection=self.conn)
        self.classes = {frm.iloc[i]['f_cod']: frm.iloc[i]['f_name'] for i in range(len(frm.values))}
        if is_save_to_file:
            with open(self.classes_file, 'wb') as f:
                pickle.dump(self.classes, f)

    def load_tovs_from_db(self, is_save_to_file=True):
        sql = """
        select r.f_name || ' IZG' || r.f_plant || ' GRP' || r.f_group || ' PRC' || round(r.f_price, -1) tov_name, r.f_class class_code
        from rest r
        -- where r.f_cod between 0 and 50000
        """
        self.tovs_frm = get_frame(sql, connection=self.conn)
        if is_save_to_file:
            self.tovs_frm.to_csv(self.tovs_file)

    def make_train_data(self):
        if self.n is not None:
            self.tovs_frm = self.tovs_frm.sample(n=self.n)

        self.X = self.tovs_frm['tov_name']
        # self.X = self.transform_text(self.X)
        self.y = self.tovs_frm['class_code']

    def show_scatter(self):
        tfidf = TfidfVectorizer(analyzer='word', stop_words=Ml.stop_words, ngram_range=(1, 2))
        X = tfidf.fit_transform(self.X).todense()
        pca = PCA(n_components=2).fit(X)
        data2D = pca.transform(X)

        plt.scatter(data2D[:, 0], data2D[:, 1], c=ml.y, marker='o')
        # plt.scatter(data2D[:, 0], data2D[:, 1], c=['r' if i == 17 else 'b' for i in ml.y], marker='o')
        plt.show()


    # def transform_text(self, text_data):
    #     tfidf = TfidfVectorizer(analyzer='word', stop_words=self.stop_words, ngram_range=(1, 2))
    #     X = tfidf.fit_transform(text_data)
    #     return X
    #     # N = 100
    #     # индексы топ 10 столбцов с максимальной суммой элементов (в столбцах)
    #     # idx = np.ravel(X.sum(axis=0).argsort(axis=1))[::-1][:N]
    #     # top_10_words = np.array(tfidf.get_feature_names())[idx].tolist()
    #     # pprint.pprint(top_10_words)

    def define_model(self):
        tfidf = TfidfVectorizer(analyzer='word', stop_words=Ml.stop_words, ngram_range=(1, 2))
        self.model = make_pipeline(tfidf, MultinomialNB(alpha=0.01))
        # XGBoost - base (CatBoost - Yandex, LightGBM - Microsoft)
        # self.model = make_pipeline(tfidf, OneVsRestClassifier(xgboost.XGBClassifier()))
        # self.model = xgboost.XGBClassifier()
        # self.model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear', C=100))
        # self.model = make_pipeline(TfidfVectorizer(), SVC(gamma='auto'))
        # self.model = make_pipeline(TfidfVectorizer(), DecisionTreeClassifier())
        # self.model = make_pipeline(TfidfVectorizer(), RandomForestClassifier(n_estimators=100, random_state=0))

    def define_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3,
                                                                                random_state=0)

    def fit(self, is_save_to_file=True, is_load_from_file=False):
        print('start fit')
        if is_load_from_file:
            with open(self.model_file, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model.fit(self.X_train, self.y_train)
        if is_save_to_file:
            with open(self.model_file, 'wb') as f:
                pickle.dump(self.model, f)

    def predict_for_test_data(self):
        print('predict_for_test_data')
        self.y_pred = self.model.predict(self.X_test)
        self.predictions = [round(value) for value in self.y_pred]

    def check_accuracy(self):
        accuracy = accuracy_score(self.y_test, self.predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))

    def predict_for_tov_name(self, tov_name):
        pred = self.model.predict([tov_name])
        return self.classes[pred[0]]


if __name__ == '__main__':
    is_load_data_from_db = False
    is_load_model_from_file = False
    ml = Ml(n=None)
    if is_load_model_from_file:
        ml.load_classes_from_file()
        ml.fit(is_load_from_file=is_load_model_from_file)
    else:
        if is_load_data_from_db:
            ml.load_from_db()
        else:
            ml.load_from_files()
        ml.define_model()
        ml.define_data()
        ml.fit(is_load_from_file=is_load_model_from_file)
        ml.predict_for_test_data()
        ml.check_accuracy()
        # ml.show_scatter()

    for tov_name in ml.test_tov_names:
        pprint.pprint((tov_name, ml.predict_for_tov_name(tov_name)))
