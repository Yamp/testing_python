import pickle
import pprint
from pathlib import Path

import pandas as pd
import psycopg2
import seaborn as sns
import xgboost
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC

from tools.db.dbtools import get_frame

sns.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from stop_words import get_stop_words
import matplotlib.pyplot as plt
import numpy as np


class Ml:
    dir = Path('d:\\1')
    classes_file = dir / 'classes.pickle'
    groups_file = dir / 'groups.pickle'
    izgots_file = dir / 'izgots.pickle'
    model_file = dir / 'model_tovs.pickle'
    tovs_file = dir / 'tovs.csv'
    stop_words = get_stop_words('russian')

    dbc = {'dbname': 'opt', 'user': 'opt', 'password': 'koradmin', 'host': 'srv-pg-test'}

    test_tov_names = ['Жираф',
                      'Жгут Ж1', 'Вытяжка лоролр эжлдж', 'Часы настенные', 'Тарелка керамическая',
                      'Рюмка большая 333',
                      'Коврик для сушки посуды', 'Салатник 500 мл', 'Вварная шпилька M14 x 16',
                      'Caster swivel w/o brake',
                      'Вешалка стандарт', 'Вешалка на стену', 'Ложка Чайная Даша', 'Медвежонок Петя',
                      'Шкатулка керамическая',
                      'Кружка',
                      'Блюдо для блинов', '6/12 Набор кофейный 100мл', 'Кухонная вытяжка ELIKOR Альфа',
                      'Изделие декоративное ', 'Молоток дверной Соня', 'Набор коробок', 'Брелок бабочка',
                      'Блюдо на ножке 37см', 'Набор чайный 7/16', 'Жопа с ручкой', 'Страус в шляпе',
                      'Банкетка Грация', 'Банкетка Груша', 'Кофе', 'Чай индийский прима'
                      ]

    cls = 1
    izg = 2
    grp = 3

    def __init__(self, n=None, type=cls) -> None:
        super().__init__()
        self.n = n
        self.type = type

    def connect_to_db(self):
        self.conn = psycopg2.connect(**self.dbc)

    def load_from_db(self, is_save_to_file=True):
        print('get data from db')
        self.connect_to_db()
        self.load_classes_from_db(is_save_to_file)
        self.load_groups_from_db(is_save_to_file)
        self.load_izgots_from_db(is_save_to_file)
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

    def load_groups_from_file(self):
        with open(self.groups_file, 'rb') as f:
            self.classes = pickle.load(f)

    def load_izgots_from_file(self):
        with open(self.izgots_file, 'rb') as f:
            self.izgots = pickle.load(f)

    def load_classes_from_db(self, is_save_to_file=True):
        frm = get_frame("select f_cod, f_name from spr_clas", connection=self.conn)
        self.classes = {frm.iloc[i]['f_cod']: frm.iloc[i]['f_name'] for i in range(len(frm.values))}
        if is_save_to_file:
            with open(self.classes_file, 'wb') as f:
                pickle.dump(self.classes, f)

    def load_groups_from_db(self, is_save_to_file=True):
        frm = get_frame("select f_cod, f_name from spr_grp", connection=self.conn)
        self.groups = {frm.iloc[i]['f_cod']: frm.iloc[i]['f_name'] for i in range(len(frm.values))}
        if is_save_to_file:
            with open(self.groups_file, 'wb') as f:
                pickle.dump(self.groups, f)

    def load_izgots_from_db(self, is_save_to_file=True):
        frm = get_frame("select f_cod, f_name from spr_pro", connection=self.conn)
        self.izgots = {frm.iloc[i]['f_cod']: frm.iloc[i]['f_name'] for i in range(len(frm.values))}
        if is_save_to_file:
            with open(self.izgots_file, 'wb') as f:
                pickle.dump(self.izgots, f)

    def load_tovs_from_db(self, is_save_to_file=True):
        sql = """
        select /*distinct*/ r.f_name tov_name, r.f_class class_code
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
        if self.type == Ml.cls:
            self.y = self.tovs_frm['class_code']
        elif self.type == Ml.izg:
            self.y = self.tovs_frm['izgot_code']
        elif self.type == Ml.grp:
            self.y = self.tovs_frm['group_code']

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
        # tfidf = TfidfVectorizer(analyzer='word', stop_words=Ml.stop_words, ngram_range=(1,1))
        # tfidf.fit_transform(self.X)
        # feature_names = np.array(tfidf.get_feature_names())
        # l = [s for s in feature_names if s[0].isdigit() ]
        # tfidf = TfidfVectorizer(analyzer='word', stop_words=Ml.stop_words + l, ngram_range=(1,2))
        # self.model = make_pipeline(tfidf, Perceptron(shuffle=False))
        # self.model = make_pipeline(tfidf, LinearSVC(C=1))
        self.model = make_pipeline(tfidf, MultinomialNB(alpha=0.01))
        # XGBoost - base (CatBoost - Yandex, LightGBM - Microsoft)
        # self.model = make_pipeline(tfidf, OneVsRestClassifier(xgboost.XGBClassifier()))
        # self.model = xgboost.XGBClassifier()
        # self.model = make_pipeline(tfidf, PCA(n_components=2), SVC(kernel='linear', C=1))
        # self.model = make_pipeline(tfidf, TruncatedSVD(n_components=4), SVC(kernel='linear', C=1))
        # self.model = make_pipeline(TfidfVectorizer(), SVC(gamma='auto'))
        # self.model = make_pipeline(TfidfVectorizer(), DecisionTreeClassifier())
        # self.model = make_pipeline(TfidfVectorizer(), RandomForestClassifier(n_estimators=100, random_state=0))

    def define_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3,
                                                                                random_state=0)
        # self.X_test = self.X_test.map(lambda n: n.split(":")[0])

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

    def predict_for_tov_name(self, tov_name, is_variants=False):
        res = ''
        spr = self.classes
        if is_variants:
            def get_code(sorted_preds, npp):
                return self.model.classes_[sorted_preds[npp][0]]

            def get_prob(srt, npp):
                return round(srt[npp][1] * 100, 2)

            preds = self.model.predict_proba([tov_name])
            sorted_preds = sorted(enumerate(preds[0]), key=lambda x: -x[1])
            if self.type == Ml.cls:
                spr = self.classes
            elif self.type == Ml.izg:
                spr = self.izgots
            elif self.type == Ml.grp:
                spr = self.groups

            res = (f"{spr[get_code(sorted_preds, 0)]} -> {get_prob(sorted_preds, 0)}",
                   f"{spr[get_code(sorted_preds, 1)]} -> {get_prob(sorted_preds, 1)}",
                   f"{spr[get_code(sorted_preds, 2)]} -> {get_prob(sorted_preds, 2)}"
                   )
        else:
            pred = self.model.predict([tov_name])
            if self.type == Ml.cls:
                res = self.classes[pred[0]]
            elif self.type == Ml.izg:
                res = self.izgots[pred[0]]
            elif self.type == Ml.grp:
                res = self.groups[pred[0]]

        return res



if __name__ == '__main__':
    is_load_data_from_db = False
    is_load_model_from_file = True
    ml = Ml(n=None, type=Ml.cls)
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
        pprint.pprint((tov_name, ml.predict_for_tov_name(tov_name, is_variants=True)))
