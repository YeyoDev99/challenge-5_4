# CHECKLIST.md — Challenge 5, Group 4

## Dataset
- Name: NCES CCD Public Elementary/Secondary School Universe Survey SY 2022-23
- Source: https://nces.ed.gov/ccd/files.asp
- Total records: 99,528 open public schools
- Records after preprocessing: 95,332
- Features (11): log_enrollment, pct_free_reduced_lunch, pct_white, pct_hispanic, pct_black, pct_asian, pct_multirace, student_teacher_ratio, is_charter, is_virtual, school_level_enc
- Sampling: K-Means final on full dataset. DBSCAN on n=15,000. Hierarchical on n=5,000.

## Hyperparameter Configurations
- K-Means: n_clusters=6, MiniBatchKMeans, init=k-means++, n_init=20, random_state=42
- DBSCAN: eps=1.2111, min_samples=16
- Hierarchical: n_clusters=6, linkage=ward, applied on n=5,000 sample

## Metrics (best config)
| Algorithm    | Silhouette | Davies-Bouldin | Calinski-Harabasz | Sample |
|---|---|---|---|---|
| K-Means      | 0.2384 | 1.4366 | 2493.1 | n=15,000 eval |
| DBSCAN       | 0.2415 | 1.4979 | 2159.9 | n=15,000 |
| Hierarchical | 0.2511 | 1.3067 | 837.2 | n=5,000 |

## Algorithm Comparison
K-Means produced the most interpretable clusters with k=6 profiles such as
high-poverty elementary schools, diverse suburban schools, and charter schools.
Hierarchical confirmed cluster stability. DBSCAN identified anomalous schools as noise.
Recommendation: K-Means for segmentation; DBSCAN as anomaly-detection layer.

## Seeds: random_state=42 (stability checked with seeds 7, 123)
