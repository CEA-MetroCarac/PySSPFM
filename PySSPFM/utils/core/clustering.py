"""
Module containing clustering functions
"""

import time
import numpy as np
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import pairwise_distances


def curve_clustering(curve_data, num_clusters=3, method='kmeans',
                     verbose=False):

    """
    Perform K-Means or Gaussian Mixture Model (GMM) clustering on curve data.

    Parameters
    ----------
    curve_data : numpy.ndarray
        Curve data for clustering.
    num_clusters : int, optional
        Number of clusters to create. Default is 3.
    method : str, optional
        Method for clustering: 'kmeans' or 'gmm'. Default is 'kmeans'.
    verbose : bool, optional
        Activation key for verbosity.

    Returns
    -------
    cluster_labels : list
        Cluster indices for each data point
    cluster_info : list
        Information about each cluster.
    inertia : float
        For K-Means : Inertia (within-cluster sum of squares).
        For GMM : Bayesian Information Criterion.
    cluster_centers: numpy.ndarray
        Coordinates of cluster centers.
    """

    start_time = time.time()

    if method == 'kmeans':
        # Apply K-Means clustering
        clusters = KMeans(
            n_clusters=num_clusters, random_state=0, n_init=20).fit(curve_data)
        cluster_labels = clusters.labels_
        # Calculate intra-cluster inertia (within-cluster sum of squares)
        inertia = clusters.inertia_
        # Calculate cluster centers
        cluster_centers = clusters.cluster_centers_
    else:
        # Apply GMM clustering
        clusters = GaussianMixture(
            n_components=num_clusters, random_state=0).fit(curve_data)
        cluster_labels = clusters.predict(curve_data)
        # Calculate Bayesian Information Criterion called inertia
        inertia = clusters.bic(curve_data)
        # Calculate cluster means
        cluster_centers = clusters.means_

    execution_time = time.time() - start_time
    if verbose:
        print("\nExecution time:", execution_time, "seconds")

    # Count the number of points in each cluster
    cluster_counts = np.bincount(cluster_labels)

    # Calculate pairwise distances between cluster centers
    distances = pairwise_distances(cluster_centers, metric='euclidean')

    # Reference cluster (position 0) = cluster with maximum of points
    arg_ref = np.argmax(cluster_counts)
    # Other cluster sorted with distance of the reference cluster
    sorted_indices = [arg_ref] + list(np.argsort(distances[arg_ref]))[1:]

    # Change of cluster_labels with sorted indexs
    cluster_labels = [sorted_indices.index(i) for i in cluster_labels]

    # All cluster info
    cluster_info = []
    for i in range(num_clusters):
        target = np.sort(distances[i])[1]
        near_clust_index = list(distances[i]).index(target)
        near_clust_name = chr(65 + sorted_indices.index(near_clust_index))
        # [0]: distance ref, [1]: distance near, [2]: name near,
        # [3]: nb of points, [4]: clust name
        tab = [distances[arg_ref][i],
               distances[i][near_clust_index],
               near_clust_name,
               cluster_counts[i],
               chr(65 + sorted_indices.index(i))]
        cluster_info.append(tab)
    # sort cluster_info with distance of the reference cluster
    sort_tab = np.argsort([line[0] for line in cluster_info])
    cluster_info = [cluster_info[arg] for arg in sort_tab]

    return cluster_labels, cluster_info, inertia, cluster_centers


def cbar_map(colors, numb_cluster, method_str):
    """
    Generate a colormap and colorbar labels for clustering visualization.

    Parameters
    ----------
    colors : list of tuple
        List of RGB color tuples.
    numb_cluster : int
        Number of clusters.
    method_str : str
        String representation of the clustering method.

    Returns
    -------
    cmap : matplotlib.colors.ListedColormap
        Colormap.
    cbar_lab : dict
        Dictionary of colorbar labels.
    """

    # Create a ListedColormap using the provided colors
    cmap = mcolors.ListedColormap(colors)

    # Generate colorbar labels
    lab_clust = list(range(numb_cluster))
    x1 = min(lab_clust)
    x2 = max(lab_clust)
    y1 = x1 + (numb_cluster - 1) / (numb_cluster * 2)
    y2 = x2 - (numb_cluster - 1) / (numb_cluster * 2)
    slope = (y2 - y1) / (x2 - x1)
    offset = y1 - x1 * slope
    coordinate = [slope * elem + offset for elem in lab_clust]
    cbar_lab = {f"Clustering ({method_str})": [[chr(65+i) for i in lab_clust],
                                               coordinate]}

    return cmap, cbar_lab
