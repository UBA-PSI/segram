from joblib import dump, load
import time, os, math
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle5 as pickle

# this file was used to measure the classification time of segram


def create_dns_sequences(prep_df):
    predict_df = pd.DataFrame()
    predict_df['app_name'] = prep_df['app_name']
    predict_df['tls_sizes'] = prep_df.tls_sizes
    predict_df['times'] = prep_df.tls_sizes_times
    predict_df['dns_seq'] = predict_df.apply(lambda x: join_lists(x.tls_sizes, x.times), axis=1)
    predict_df['dns_seq'] = [' '.join(map(str, seq)) for seq in predict_df['dns_seq']]
    return predict_df


def join_lists(tls_sizes0, times0):
    result = []
    for index, elems in enumerate(zip(times0, tls_sizes0)):
        if index > 0:
            gap = int(math.log(1 + (float(elems[0]) * 1000), 2))
            if gap >= 5:
                result.append("G" + str(gap))
        result.append(elems[1])
    return result


def split_text(x):
    return x.split(" ")


myseed = 42
path = "./test/"
test_files = os.listdir(path)
for file in test_files:
    name = file.split(".")[0]
    print(name)
    with open(path+file, "rb") as f:
        test_df = pickle.load(f)
    rfc = load(f'./models/rfc_{name}.joblib')
    vectorizer = load(f'./vectorizers/{name}.joblib')

    # begin time at creating dns sequences for new instances
    predict_instances = create_dns_sequences(test_df)
    start = time.monotonic()
    X_test = vectorizer.transform(predict_instances['dns_seq'])
    duration_vector = time.monotonic()

    y_pred = rfc.predict(X_test)
    end = time.monotonic()
    duration = end - start
    y_test = predict_instances['app_name']
    print("Duration Classification: ", duration, "s")
    print("Duration Build Vector: ", duration_vector - start, "s")
    print("Duration RFC: ", end - duration_vector, "s")
    print("Accuracy", "%0.3f" % accuracy_score(y_test, y_pred))
    print("\n")
