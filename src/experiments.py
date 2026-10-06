"""Execução por fold e agregação somente de combinações completas."""
import json
import warnings
from time import perf_counter

import numpy as np
import pandas as pd
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)
from threadpoolctl import threadpool_limits

from src.pipelines import FEATURES, METRICS, build_pipeline


def run_experiment(X, y, splits, configs):
    rows = []
    for config in configs:
        for fold, (train, test) in enumerate(splits, 1):
            row = {**config, 'fold': fold, 'status': 'failed', 'error': '',
                   'warnings': '', 'n_features_before': X.shape[1],
                   'n_features_after': np.nan, 'selected_features': '',
                   'pca_variance': np.nan, **{m: np.nan for m in METRICS}}
            start = perf_counter()
            caught = []
            try:
                with warnings.catch_warnings(record=True) as caught, threadpool_limits(limits=1):
                    warnings.simplefilter('always')
                    warnings.filterwarnings('error', category=UndefinedMetricWarning)
                    if y.iloc[train].nunique() != 2 or y.iloc[test].nunique() != 2:
                        raise ValueError('Treino ou teste contém apenas uma classe; AUC indefinida.')
                    pipeline = build_pipeline(config)
                    pipeline.fit(X.iloc[train], y.iloc[train])
                    predicted = pipeline.predict(X.iloc[test])
                    positive = list(pipeline.classes_).index(1)
                    scores = pipeline.predict_proba(X.iloc[test])[:, positive]
                    values = {
                        'accuracy': accuracy_score(y.iloc[test], predicted),
                        'precision': precision_score(y.iloc[test], predicted, pos_label=1),
                        'recall': recall_score(y.iloc[test], predicted, pos_label=1),
                        'f1': f1_score(y.iloc[test], predicted, pos_label=1),
                        'auc': roc_auc_score(y.iloc[test], scores),
                    }
                    if not all(np.isfinite(v) for v in values.values()):
                        raise ValueError('Métrica não finita.')
                    reducer = pipeline.named_steps['reduction']
                    row['n_features_after'] = pipeline.named_steps['knn'].n_features_in_
                    if config['reduction'] == 'kbest8':
                        row['selected_features'] = json.dumps(
                            np.array(FEATURES)[reducer.get_support()].tolist())
                    elif config['reduction'] == 'pca95':
                        row['pca_variance'] = reducer.explained_variance_ratio_.sum()
                    row.update(values)
                    row['status'] = 'ok'
            except Exception as exc:
                row['error'] = f'{type(exc).__name__}: {exc}'
            finally:
                row['warnings'] = ' | '.join(str(w.message) for w in caught)
                row['seconds'] = perf_counter() - start
                rows.append(row)
        print(f"{config['combination']}: {sum(r['status'] == 'ok' for r in rows[-5:])}/5 folds válidos")
    return pd.DataFrame(rows)


def summarize(folds):
    rows = []
    keys = ['combination', 'imputation', 'scale', 'reduction']
    for config, group in folds.groupby(keys, sort=False):
        complete = (len(group) == 5 and group['fold'].nunique() == 5
                    and group['status'].eq('ok').all()
                    and np.isfinite(group[METRICS].to_numpy()).all())
        row = dict(zip(keys, config))
        row.update(status='complete' if complete else 'failed',
                   valid_folds=int(group['status'].eq('ok').sum()),
                   seconds_total=group['seconds'].sum(),
                   error=' | '.join(group.loc[group['status'] != 'ok', 'error']))
        for metric in METRICS:
            row[f'{metric}_mean'] = group[metric].mean() if complete else np.nan
            row[f'{metric}_std'] = group[metric].std(ddof=1) if complete else np.nan
        row['n_features_before'] = group['n_features_before'].iloc[0]
        row['n_features_after_min'] = group['n_features_after'].min() if complete else np.nan
        row['n_features_after_max'] = group['n_features_after'].max() if complete else np.nan
        rows.append(row)
    return pd.DataFrame(rows)
