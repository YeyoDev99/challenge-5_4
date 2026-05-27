"""
clustering_utils.py — Reusable helpers for K-Means, DBSCAN, and Hierarchical.
Group 4 — Challenge 5 — Universidad Distrital Francisco José de Caldas
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                              calinski_harabasz_score)
import matplotlib.pyplot as plt

RANDOM_STATE = 42


def kmeans_sweep(X, k_range=range(2, 13), seeds=(42, 7, 123), n_init=10):
    """Return DataFrame with inertia and silhouette (mean±std) for each k."""
    rows = []
    for k in k_range:
        sil_runs = [
            silhouette_score(
                X, KMeans(n_clusters=k, init='k-means++', n_init=n_init,
                           random_state=s).fit_predict(X))
            for s in seeds
        ]
        inertia = KMeans(n_clusters=k, init='k-means++', n_init=n_init,
                         random_state=RANDOM_STATE).fit(X).inertia_
        rows.append({'k': k, 'inertia': inertia,
                     'sil_mean': np.mean(sil_runs),
                     'sil_std': np.std(sil_runs)})
    return pd.DataFrame(rows)


def plot_elbow_silhouette(df_sweep, save_path=None):
    """Plot elbow + silhouette curves; return best k."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(df_sweep['k'], df_sweep['inertia'], 'bo-', lw=2)
    ax1.set(xlabel='k', ylabel='Inertia (SSE)', title='K-Means Elbow Curve')
    ax1.grid(alpha=0.3)
    ax2.errorbar(df_sweep['k'], df_sweep['sil_mean'], yerr=df_sweep['sil_std'],
                 fmt='go-', lw=2, capsize=4, label='mean ± std')
    best_k = int(df_sweep.loc[df_sweep['sil_mean'].idxmax(), 'k'])
    ax2.axvline(best_k, color='red', linestyle='--', label=f'Best k={best_k}')
    ax2.set(xlabel='k', ylabel='Silhouette Score',
            title='Silhouette Score vs k')
    ax2.legend()
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    return best_k


def evaluate_labels(X, labels, algorithm_name=""):
    """Compute Silhouette, Davies-Bouldin, Calinski-Harabasz (excludes noise)."""
    mask = labels != -1
    X_eval, y_eval = X[mask], labels[mask]
    n_clusters = len(set(y_eval))
    if n_clusters < 2:
        print(f"{algorithm_name}: fewer than 2 clusters — metrics not defined.")
        return {}
    sil = silhouette_score(X_eval, y_eval)
    db  = davies_bouldin_score(X_eval, y_eval)
    ch  = calinski_harabasz_score(X_eval, y_eval)
    print(f"{algorithm_name:25s} | Silhouette={sil:.4f} | "
          f"Davies-Bouldin={db:.4f} | Calinski-Harabasz={ch:.1f}")
    return {'silhouette': sil, 'davies_bouldin': db, 'calinski_harabasz': ch}


def dbscan_sweep(X, eps_values, min_samples):
    """Sweep eps values for DBSCAN and return results DataFrame."""
    rows = []
    for eps in eps_values:
        labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X)
        n_clust = len(set(labels)) - (1 if -1 in labels else 0)
        noise_frac = (labels == -1).sum() / len(labels)
        metrics = evaluate_labels(X, labels, f"DBSCAN eps={eps:.4f}")
        rows.append({'eps': eps, 'min_samples': min_samples,
                     'n_clusters': n_clust, 'noise_frac': round(noise_frac, 4),
                     **{k: round(v, 4) for k, v in metrics.items()}})
    return pd.DataFrame(rows)
