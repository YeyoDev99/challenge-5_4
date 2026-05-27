"""
preprocessing.py — Feature engineering and cleaning utilities for CCD clustering.
Group 4 — Challenge 5 — Universidad Distrital Francisco José de Caldas
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

LEVEL_MAP = {
    'Elementary': 0, 'Prekindergarten': 0,
    'Middle': 1,
    'High': 2, 'Secondary': 2,
    'Other': 3, 'Not reported': 3, 'Ungraded': 3,
}

FEATURE_COLS = [
    'log_enrollment',
    'pct_free_reduced_lunch',
    'pct_white', 'pct_hispanic', 'pct_black', 'pct_asian', 'pct_multirace',
    'student_teacher_ratio',
    'is_charter',
    'is_virtual',
    'school_level_enc',
]


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features to the merged master dataframe."""
    out = df.copy()
    total = out['TOTAL_ENROLLMENT'].replace(0, np.nan)
    out['pct_free_reduced_lunch'] = out['FRPL_COUNT'] / total
    out['pct_white']     = out.get('n_white', 0)     / total
    out['pct_hispanic']  = out.get('n_hispanic', 0)  / total
    out['pct_black']     = out.get('n_black', 0)     / total
    out['pct_asian']     = out.get('n_asian', 0)     / total
    out['pct_multirace'] = out.get('n_multirace', 0) / total
    out['student_teacher_ratio'] = (
        out['TOTAL_ENROLLMENT'] / out['TEACHERS'].replace(0, np.nan)
    ).clip(upper=200)
    out['is_charter']       = (out['CHARTER_TEXT'] == 'Yes').astype(int)
    out['is_virtual']       = out['VIRTUAL'].isin(
        ['FULLVIRTUAL', 'SUPPVIRTUAL']).astype(int)
    out['school_level_enc'] = out['LEVEL'].map(LEVEL_MAP).fillna(3)
    out['log_enrollment']   = np.log1p(out['TOTAL_ENROLLMENT'])
    return out


def prepare_matrix(df: pd.DataFrame, min_features: int = 8):
    """Return cleaned feature matrix, cleaned df, and fitted scaler."""
    df_clean = df.dropna(subset=FEATURE_COLS, thresh=min_features).copy()
    for col in FEATURE_COLS:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean[FEATURE_COLS])
    return df_clean, X_scaled, scaler


def apply_pca(X_scaled, variance_threshold=0.90, random_state=42):
    """Reduce dimensions retaining variance_threshold of total variance."""
    pca_full = PCA(random_state=random_state)
    pca_full.fit(X_scaled)
    cumvar = np.cumsum(pca_full.explained_variance_ratio_)
    n = int(np.searchsorted(cumvar, variance_threshold)) + 1
    pca = PCA(n_components=n, random_state=random_state)
    X_pca = pca.fit_transform(X_scaled)
    print(f"PCA: {n} components → "
          f"{pca.explained_variance_ratio_.sum()*100:.1f}% variance retained")
    return X_pca, pca
