"""
Module containing clustering functions
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.metrics import pairwise_distances

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.figure import plot_graph


def data_clustering(data, num_clusters=3, method='kmeans', verbose=False):

    """
    Perform K-Means or Gaussian Mixture Model (GMM) clustering on data.

    Parameters
    ----------
    data : numpy.ndarray
        Data for clustering.
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
            n_clusters=num_clusters, random_state=0, n_init=20).fit(data)
        cluster_labels = clusters.labels_
        # Calculate intra-cluster inertia (within-cluster sum of squares)
        inertia = clusters.inertia_
        # Calculate cluster centers
        cluster_centers = clusters.cluster_centers_
    else:
        # Apply GMM clustering
        clusters = GaussianMixture(
            n_components=num_clusters, random_state=0).fit(data)
        cluster_labels = clusters.predict(data)
        # Calculate Bayesian Information Criterion called inertia
        inertia = clusters.bic(data)
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


def plot_clustering_centroids(data_y, numb_cluster, cluster_labels,
                              cluster_info, centers, colors, figname=None):
    """
    Plot clustering centroids

    Parameters
    ----------
    data_y: numpy.ndarray
        Data points
    numb_cluster: int
        Number of clusters
    cluster_labels: list
        Cluster labels for each data point
    cluster_info: list
        Information about each cluster
    centers: numpy.ndarray
        Centroids of the clusters
    colors: list
        List of colors for each cluster
    figname: str, optional
        Name of the saved figure (default is None)

    Returns
    -------
    list
        List containing the generated figure
    """
    # Create fig and graph
    fig, ax = plt.subplots(figsize=get_setting("figsize"))
    fig.sfn = "clusters_centroids" if figname is None else figname
    plot_dict_1 = {
        'title': 'Clusters with Centroids',
        'x lab': 'Feature 1', 'y lab': 'Feature 2',
        'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_graph(ax, [], [], plot_dict=plot_dict_1)

    # Plot data
    for index in range(numb_cluster):
        cluster_data = data_y[np.array(cluster_labels) == index]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1],
                    c=[colors[index]],
                    label=f'Cluster {cluster_info[index][4]}')

    # Plot centers
    plt.scatter(centers[:, 0], centers[:, 1],
                marker='x', color='black', label='Centroids')
    ax.legend()

    return [fig]


def plot_all_vector_clustering(x_vectors, y_vectors, numb_cluster,
                               cluster_labels, cluster_info, colors,
                               figname=None):
    """
    Plot all vectors with clustering information

    Parameters
    ----------
    x_vectors: list
        List of x-coordinate vectors
    y_vectors: list
        List of y-coordinate vectors
    numb_cluster: int
        Number of clusters
    cluster_labels: list
        Cluster labels for each data point
    cluster_info: list
        Information about each cluster
    colors: list
        List of colors for each cluster
    figname: str, optional
        Name of the saved figure (default is None)

    Returns
    -------
    list
        List containing the generated figure
    """

    labels = [f'Cluster {cluster_info[i][4]}, {cluster_info[i][3]} points, '
              f'near dist ({cluster_info[i][2]}) : {cluster_info[i][1]:.2e}, ' 
              f'ref (A) dist : {cluster_info[i][0]:.2e}'
              for i in range(numb_cluster)]

    legend_handles = [Patch(color=colors[i], label=labels[i])
                      for i in range(numb_cluster)]

    # Create graph
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = "clustering_best_vectors" if figname is None else figname
    plot_dict_1 = {
        'title': 'Clustering: Best Vectors',
        'x lab': 'Voltage', 'y lab': 'Y Axis',
        'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_graph(ax, [], [], plot_dict=plot_dict_1)

    # Plot all vectors
    for i, (elem_x, elem_y) in enumerate(zip(x_vectors, y_vectors)):
        plt.plot(elem_x, elem_y, color=colors[cluster_labels[i]])

    ax.legend(handles=legend_handles)

    return [fig]


def plot_avg_vector_clustering(x_avg_vector, y_avg_vectors, numb_cluster,
                               cluster_info, colors, figname=None):
    """
    Plot average vectors by cluster

    Parameters
    ----------
    x_avg_vector: list
        X-coordinates of average vectors
    y_avg_vectors: list
        Y-coordinates of average vectors for each cluster
    numb_cluster: int
        Number of clusters
    cluster_info: list
        Information about each cluster
    colors: list
        List of colors for each cluster
    figname: str, optional
        Name of the saved figure (default is None)

    Returns
    -------
    list
        List containing the generated figure
    """
    # Create graph
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = "clustering_average_vectors" if figname is None else figname
    plot_dict_3 = {
        'title': 'Average Vector by Cluster',
        'x lab': 'Voltage', 'y lab': 'Y Axis',
        'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_graph(ax, [], [], plot_dict=plot_dict_3)

    # Plot average vectors
    for index in range(numb_cluster):
        label = f'Cluster {cluster_info[index][4]}'
        plt.plot(x_avg_vector, y_avg_vectors[index],
                 label=label, color=colors[index])
    ax.legend()

    return [fig]


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


def data_pca(data, dimension=2):
    """
    Perform PCA on data

    Parameters
    ----------
    data: numpy.ndarray
        Data for PCA.
    dimension: int, optional
        Dimension of PCA output (default is 2)

    Returns
    -------
    processed_data: numpy.ndarray
        Transformed data after PCA
    """
    # Creating the PCA object
    pca = PCA(n_components=dimension)

    # Fitting the model to the data and transforming the data
    processed_data = pca.fit_transform(data)

    return processed_data


def plot_pca_plane(processed_data, label_clust=None, colors=None,
                   centers=None, figname=None):
    """
    Plot PCA plane, for 2D PCA analysis, with possible clustering results
    performed after PCA analysis

    Parameters
    ----------
    processed_data: numpy.ndarray
        Transformed data after PCA
    label_clust: numpy.ndarray or None, optional
        Cluster labels for each data point (default is None)
    colors: list or None, optional
        List of colors associated to cluster indice (default is None)
    centers: numpy.ndarray or None, optional
        Centers of the clusters (default is None)
    figname: str, optional
        Name of the saved figure (default is None)

    Returns
    -------
    list
        List containing the generated figure
    """

    # Create fig and graph
    fig, ax = plt.subplots(figsize=get_setting("figsize"))
    fig.sfn = "clusters_centroids" if figname is None else figname
    plot_dict_1 = {
        'title': 'Representation of Transformed Data after PCA',
        'x lab': 'Principal Component 1', 'y lab': 'Principal Component 2',
        'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_graph(ax, [], [], plot_dict=plot_dict_1)

    pc1, pc2 = processed_data[:, 0], processed_data[:, 1]

    # Plot point and annotate
    for i, (x, y) in enumerate(zip(pc1, pc2)):
        color = colors[label_clust[i]] if (colors is not None and
                                           label_clust is not None) else "blue"
        ax.scatter(x, y, color=color)
        # ax.text(x, y, f'{i + 1}', fontsize=9)

    # Plot centers
    if centers is not None:
        center_1, center_2 = centers[:, 0], centers[:, 1]
        ax.scatter(center_1, center_2, marker="x", color="k")

    return [fig]
