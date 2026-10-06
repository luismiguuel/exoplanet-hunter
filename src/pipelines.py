"""Espaço fixo de pré-processamento da Entrega 2 (sem otimização do kNN)."""
from itertools import product

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

FEATURES = [
    'koi_period', 'koi_impact', 'koi_duration', 'koi_depth',
    'koi_prad', 'koi_teq', 'koi_steff', 'koi_slogg',
    'koi_srad', 'koi_insol', 'koi_model_snr', 'koi_kepmag',
]
SEED = 42
BASELINE = 'median__none__none'
METRICS = ['accuracy', 'precision', 'recall', 'f1', 'auc']


def combinations():
    configs = [dict(combination=f'{i}__{s}__{r}', imputation=i, scale=s, reduction=r)
               for i, s, r in product(['mean', 'median'],
                                     ['none', 'standard', 'minmax', 'robust'],
                                     ['none', 'pca95', 'kbest8'])]
    assert len(configs) == len({c['combination'] for c in configs}) == 24
    return configs


def build_pipeline(config):
    scalers = {'none': 'passthrough', 'standard': StandardScaler(),
               'minmax': MinMaxScaler(), 'robust': RobustScaler()}
    reducers = {'none': 'passthrough',
                'pca95': PCA(n_components=0.95, svd_solver='full', whiten=False),
                'kbest8': SelectKBest(score_func=f_classif, k=8)}
    return Pipeline([
        ('imputation', SimpleImputer(strategy=config['imputation'], keep_empty_features=True)),
        ('scale', scalers[config['scale']]),
        ('reduction', reducers[config['reduction']]),
        ('knn', KNeighborsClassifier(n_neighbors=7, p=2, metric='minkowski',
                                    weights='uniform', algorithm='brute', n_jobs=1)),
    ])
