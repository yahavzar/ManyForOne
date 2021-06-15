import pandas as pd
from DB.frequency import *
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from collections import Counter


def load_data_from_db():
    rows = Frequency.query.statement
    df = pd.read_sql(rows, db.engine)
    df = df.drop(['id'], axis=1)
    return df


def create_X(df):
    N = df['recipient'].nunique()
    M = df['donor'].nunique()

    user_mapper = dict(zip(np.unique(df["recipient"]), list(range(N))))
    donor_mapper = dict(zip(np.unique(df["donor"]), list(range(M))))
    donor_inv_mapper = dict(zip(list(range(M)), np.unique(df["donor"])))

    user_index = [user_mapper[i] for i in df['recipient']]
    donor_index = [donor_mapper[i] for i in df['donor']]

    X = csr_matrix((df["counter"], (donor_index, user_index)), shape=(M, N))

    return X, donor_mapper, donor_inv_mapper


def find_similar_donors(donor_id, X, k, donor_mapper, donor_inv_mapper, metric='cosine', show_distance=False):
    neighbour_ids = []

    donor_ind = donor_mapper[donor_id]
    donor_vec = X[donor_ind]
    k += 1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    if isinstance(donor_vec, (np.ndarray)):
        donor_vec = donor_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(donor_vec, return_distance=show_distance)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(donor_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


def get_top_k_similar_to_donor(donor_id, k=3):
    df = load_data_from_db()
    X_matrix, donor_mapper, donor_inv_mapper = create_X(df)
    similar_ids_euclidean, similar_ids_cosine, similar_ids_manhattan = [], [], []
    top_k = k
    while k > 0:
        try:
            similar_ids_euclidean = find_similar_donors(donor_id=donor_id, X=X_matrix, k=k, donor_mapper=donor_mapper,
                                                        donor_inv_mapper=donor_inv_mapper, metric="euclidean")
            similar_ids_cosine = find_similar_donors(donor_id=donor_id, X=X_matrix, k=k, donor_mapper=donor_mapper,
                                                     donor_inv_mapper=donor_inv_mapper, metric="cosine")
            similar_ids_manhattan = find_similar_donors(donor_id=donor_id, X=X_matrix, k=k, donor_mapper=donor_mapper,
                                                        donor_inv_mapper=donor_inv_mapper, metric="manhattan")
            k = 0
        except ValueError:
            k -= 1

    similar_ids_counter = Counter(similar_ids_euclidean + similar_ids_cosine + similar_ids_manhattan)
    k_most_common = [i for i, j in similar_ids_counter.most_common(top_k)]
    return k_most_common


def get_user_recommendations(user_email, requests_list, latest_count=3):
    requests_list = sorted(requests_list, key=lambda x: x.date, reverse=True)
    latest_donors = set([r.donor for r in requests_list[:latest_count]])
    recommendations = []
    for donor in latest_donors:
        recommendations.extend(get_top_k_similar_to_donor(donor_id=donor))
    return list(set(recommendations))
