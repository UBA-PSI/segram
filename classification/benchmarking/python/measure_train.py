from joblib import dump, load
import time, os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle5 as pickle

def text_splitter(text):
    return text.split(" ")

myseed = 42
path = "./train/"
train_files = os.listdir(path)

for file in train_files:
    name = file.split(".")[0]
    with open(path+file, "rb") as f:
        predict_df = pickle.load(f)
    print(name)

    # begin time when creating feature vector
    start = time.monotonic()
    # vectorizer and transformer
    vectorizer = TfidfVectorizer(tokenizer=text_splitter, ngram_range=(1, 3), use_idf=False,
                             sublinear_tf=False, norm='', smooth_idf=False)
    # feature w. timing
    X = vectorizer.fit_transform(predict_df['dns_seq'])
    y = predict_df["app_name"]

    # random forest model creation
    rfc = RandomForestClassifier(n_jobs=1, random_state=myseed)
    rfc.fit(X, y)
    end_training_time = time.monotonic()
    training_duration = end_training_time - start
    print("Duration Training: ", training_duration, "\n")
    dump(vectorizer, f'./vectorizers/{name}.joblib')
    dump(rfc, f'./models/rfc_{name}.joblib')
