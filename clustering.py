import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import umap

def cluster_songs(features_df, n_clusters=5):
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features_df)

    # k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    labels = kmeans.fit_predict(X_scaled)

    # UMAP dimensionality reduction
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=0)
    embedding = reducer.fit_transform(X_scaled)

    clustered_df = features_df.copy()
    clustered_df["cluster"] = labels
    clustered_df["umap_x"] = embedding[:,0]
    clustered_df["umap_y"] = embedding[:,1]

    return clustered_df