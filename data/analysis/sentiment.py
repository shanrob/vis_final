import csv
import random
from os import path

import pandas as pd
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

import sklearn.linear_model
import sklearn.tree
import sklearn.metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate

import normalize

def load_twitter():
    twitter_train = pd.read_csv("../twitter/training_twitter.csv", encoding="ISO-8859-1", header=None)
    twitter_test = pd.read_csv("../twitter/test_twitter.csv", encoding="ISO-8859-1", header=None)
    return twitter_train, twitter_test


def sample_twitter_train(twitter_train, num_samples=150000):
    return random.sample(range(0, twitter_train.shape[0]), num_samples)


def twitter_x(tweet_sample, twitter_train, twitter_test):
    twitter_train_x = np.array(twitter_train.iloc[tweet_sample].drop([0], axis=1))
    twitter_test_x = np.array(twitter_test.drop([0], axis=1))
    return twitter_train_x, twitter_test_x


def twitter_y(tweet_sample, twitter_train, twitter_test):
    twitter_train_y = np.array(twitter_train.drop([1, 2, 3, 4, 5], axis=1))[tweet_sample].reshape(len(tweet_sample,), )
    twitter_test_y = np.array(twitter_test.drop([1, 2, 3, 4, 5], axis=1))

    twitter_train_y = np.where(twitter_train_y == 4, 1, twitter_train_y)
    twitter_train_y = np.where(twitter_train_y == 2, 1, twitter_train_y)

    twitter_test_y = np.where(twitter_test_y == 4, 1, twitter_test_y)
    twitter_test_y = np.where(twitter_test_y == 2, 1, twitter_test_y)

    return twitter_train_y, twitter_test_y


def normalize_twitter_train_x(twitter_train_x):
    if path.exists("normalized_twitter_train_x.csv"):
        normalized_twitter_train_x = pd.read_csv("normalized_twitter_train_x.csv")
        normalized_twitter_train_x = normalized_twitter_train_x['0'].values.astype('U')
        return np.array(normalized_twitter_train_x).ravel().tolist()
    else:
        normalized_twitter_train_x = normalize.preprocess_text(twitter_train_x[:,4])
        pd.DataFrame(normalized_twitter_train_x).to_csv("normalized_twitter_train_x.csv", index=False)

    return normalized_twitter_train_x


def normalize_twitter_test_x(twitter_test_x):
    if path.exists("normalized_twitter_test_x.csv"):
        normalized_twitter_test_x = pd.read_csv("normalized_twitter_test_x.csv")
        normalized_twitter_test_x = normalized_twitter_test_x['0'].values.astype('U')
        return np.array(normalized_twitter_test_x).ravel().tolist()
    else:
        normalized_twitter_test_x = normalize.preprocess_text(twitter_test_x[:,4])
        pd.DataFrame(normalized_twitter_test_x).to_csv("normalized_twitter_test_x.csv", index=False)


    return normalized_twitter_test_x


def make_vector(text, vectorizer=None):
    if vectorizer == None:
        vectorizer = CountVectorizer(ngram_range=(1,2), max_features=3000) #min_df = 0?

    # call `fit` to build the vocabulary
    vectorizer.fit(text)

    # call `transform` to convert text to a bag of words
    x = vectorizer.transform(text)

    return x, vectorizer


def evaluate_logistic_grid(x_train, y_train):
    # the grid of parameters to search over
    alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    n_grams = [1, 2, 3]
    max_features = [None, 1000, 1500, 2000, 2500, 3000]

    # Find the best value for alpha and min_df, and the best classifier
    best_alpha = None
    max_loglike = -np.inf
    best_n_gram = None
    best_max_feature = None

    kf = KFold(n_splits=5, shuffle=False, random_state=1)

    for alpha in alphas:
        for n_gram in n_grams:
            for max_feature in max_features:
                vectorizer = CountVectorizer(ngram_range=(1, n_gram), max_features=max_feature)
                x, vect = make_vector(x_train, vectorizer)
                clf = sklearn.linear_model.LogisticRegression(C=alpha, solver='liblinear').fit(x, y_train)
                cv_results = cross_validate(clf, x, y_train, cv=kf, return_train_score=True)

                if np.mean(cv_results['test_score']) > max_loglike:
                    max_loglike = np.mean(cv_results['test_score'])
                    best_alpha = alpha
                    best_n_gram = n_gram
                    best_max_feature = max_feature

    return best_alpha, max_loglike, best_n_gram, best_max_feature


def train_logistic(train_x, train_y):
    return evaluate_logistic_grid(train_x, train_y)


def evaluate_logistic(alpha, x_train, y_train, x_test, y_test):
    clf = sklearn.linear_model.LogisticRegression(C=alpha, solver='liblinear').fit(x_train, y_train)
    clf_tr_proba = clf.predict_proba(x_train)
    clf_te_proba = clf.predict_proba(x_test)

    log_loss_tr = sklearn.metrics.log_loss(y_train, clf_tr_proba)

    return clf, log_loss_tr, clf_tr_proba, clf_te_proba


def predict_logistic(clf, x_train):
    return clf.predict_proba(x_train)


def main():
    script = pd.read_csv("all_scripts.csv")
    lines = script['Line'].values.tolist()

    normalized_text = normalize.preprocess_text(lines)

    with open('parks_normalized.csv', 'w') as parks_normalized:
        wr = csv.writer(parks_normalized, quoting=csv.QUOTE_ALL)
        wr.writerow(normalized_text)

    all_words = []
    for text in normalized_text:
        all_words += word_tokenize(text)

    fdist = FreqDist(all_words)
    print(fdist)

    top = pd.DataFrame(list(fdist.items()), columns=["Word", "Frequency"])

    twitter_train, twitter_test = load_twitter()
    tweet_sample = sample_twitter_train(twitter_train)
    twitter_train_x, twitter_test_x = twitter_x(tweet_sample, twitter_train, twitter_test)
    twitter_train_y, twitter_test_y = twitter_y(tweet_sample, twitter_train, twitter_test)

    normalized_twitter_train_x = normalize_twitter_train_x(twitter_train_x)
    normalized_twitter_test_x = normalize_twitter_test_x(twitter_test_x)
    #
    # best_alpha, max_loglike, best_n_gram, best_max_feature = evaluate_logistic_grid(normalized_twitter_train_x,
    #                                                                                 twitter_train_y)
    #
    # print("Best alpha: " + str(best_alpha))
    # print("Max loglike: " + str(max_loglike))
    # print("Best n-gram: " + str(best_n_gram))
    # print("Best max feature: " + str(best_max_feature))

    vectorizer = CountVectorizer(ngram_range=(1, 2))
    x, vect = make_vector(normalized_twitter_train_x, vectorizer)
    x_T = vect.transform(normalized_twitter_test_x)

    clf, log_loss_tr, clf_tr_proba, clf_te_proba = evaluate_logistic(0.1, x, twitter_train_y, x_T, twitter_test_y)

    # acc, tpr, tnr, ppv, npv = util.calc_perf_metrics_for_threshold(twitter_train_y.ravel(), clf_tr_proba[:,1], 0.5)
    #
    # print("Accuracy: " + str(acc))
    #
    # acc, tpr, tnr, ppv, npv = util.calc_perf_metrics_for_threshold(twitter_test_y.ravel(), clf_te_proba[:,1], 0.5)
    #
    # print("Accuracy: " + str(acc))

    x_parks_T = vect.transform(normalized_text)
    clf_proba_parks = predict_logistic(clf, x_parks_T)

    sentiment = []
    for elem in clf_proba_parks[:, 1]:
        if elem > 0.45 and elem < 0.55:
            sentiment_type = 'Neutral'
        elif elem >= 0.55:
            sentiment_type = 'Positive'
        else:
            sentiment_type = 'Negative'
        sentiment.append(sentiment_type)

    script['Sentiment'] = sentiment

    script.to_csv('scripts_with_sentiment.csv', index=False)


if __name__ == "__main__":
    main()