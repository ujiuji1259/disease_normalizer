import pickle
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix, vstack
from tqdm import tqdm
import MeCab


class MeCabTokenizer(object):
    def __init__(self):
        self.mecab = MeCab.Tagger('-Owakati')

    def tokenize(self, word):
        words = self.mecab.parse(word).rstrip().split(' ')
        return words

class DNorm(object):
    def __init__(self, dictionary, model_path):
        self.tokenizer = MeCabTokenizer()
        self.norms = [d.name for d in dictionary]
        self.norm2idx = {d.name: idx for idx, d in enumerate(dictionary)}
        self.dict = {d.name: d for d in dictionary}

        if model_path is None:
            self.tfidf = TfidfVectorizer(analyzer=self.tokenizer.tokenize, use_idf=True, stop_words=None)
            self.train_tfidf(self.norms)
            d_num = len(self.tfidf.get_feature_names())
            self.W = csr_matrix(([1]*d_num, ([i for i in range(d_num)], [i for i in range(d_num)])), shape=(d_num, d_num))
        else:
            self.load_model(model_path)

        self.norms_vec = self.tfidf.transform(self.norms)

    def get_negative_vec(self, x_vec, y):
        idx = self.norm2idx[y]
        if idx == 0:
            neg_vecs = self.norms_vec[1:]
        elif idx == len(self.norms) - 1:
            neg_vecs = self.norms_vec[:-1]
        else:
            neg_vecs = vstack([self.norms_vec[:idx], self.norms_vec[idx+1:]])

        sims = self.calc_score(x_vec, neg_vecs)
        rank = sims.argmax()
        return neg_vecs[rank]

    def calc_avg_rank(self, x, y):
        pred = self.predict(x, k=-1)
        rank = 0
        cnt = 0
        zero = 0
        for pp, t in zip(pred, y):
            for idx, p in enumerate(pp):
                if p == t or idx > 100:
                    break

            rank += idx
            cnt += 1
        return rank / cnt

    def calc_score(self, v1, v2):
        return (v1.dot(self.W)).dot(v2.T)

    def predict(self, x, k=1):
        x = self.tfidf.transform(x)
        sims = self.calc_score(x, self.norms_vec).toarray()
        rank = sims.argsort(axis=1)[:, ::-1][:, :k]
        return [[self.norms[r] for r in rr] for rr in rank], [sims[idx, rr] for idx, rr in enumerate(rank)]

    def train(self, X, Y, val_x, val_y, eta):
        val_score = [float("inf"), 1e10]
        x_vec = self.tfidf.transform(X)
        y_vec = self.tfidf.transform(Y)
        val_x_vec = self.tfidf.transform(val_x)
        val_y_vec = self.tfidf.transform(val_y)

        while val_score[-1] < val_score[-2]:
            idxs = [i for i in range(len(X))]
            random.shuffle(idxs)
            for idx in tqdm(idxs):
                input_x = x_vec[idx]
                input_y = y_vec[idx]
                y = Y[idx]
                neg_vec = self.get_negative_vec(input_x, y)
                self.update(input_x, input_y, neg_vec, eta)
            score = self.calc_avg_rank(val_x, val_y)
            val_score.append(score)
            print('average rank of validation set : ', score)

    def update(self, m, x_p, x_n, eta):
        neg_score = self.calc_score(m, x_n)
        neg_score = 0 if len(neg_score.data) == 0 else neg_score.data[0]
        pos_score = self.calc_score(m, x_p)
        pos_score = 0 if len(pos_score.data) == 0 else pos_score.data[0]
        score = pos_score - neg_score
        if score < 1:
            self.W = self.W + eta * (m.T.dot(x_p) - m.T.dot(x_n))


    def save_model(self, path):
        d = {}
        self.tfidf.set_params(analyzer="word")
        d["tfidf"] = self.tfidf
        d["W"] = self.W

        with open(path, 'wb') as f:
            pickle.dump(d, f)

    def load_model(self, path):
        with open(path, 'rb') as f:
            model = pickle.load(f)

        self.tfidf = model["tfidf"]
        self.tfidf.set_params(analyzer=self.tokenizer.tokenize)

        self.W = model["W"]

    def train_tfidf(self, dataset):
        self.tfidf.fit(dataset)
