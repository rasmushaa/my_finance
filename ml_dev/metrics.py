

import pandas as pd
import numpy as np

def get_statistics(y_predicted: list, y_test: list, accepted_error: int):
    def get_accuracy(df_group):
        events = df_group.shape[0]
        trues = df_group.loc[df_group['acceptable'] == True].shape[0]
        return trues / events

    errors = []
    labels = []
    for i, row in enumerate(y_predicted):
        try:
            errors.append(int(list(row.keys()).index(y_test[i])))
            labels.append(y_test[i])
        except ValueError:
            pass
    df_errors = pd.DataFrame(zip(labels, errors), columns=['actual_y', 'order'])

    df_accuracy = df_errors.copy()
    df_accuracy['acceptable'] = df_accuracy['order'] <= accepted_error
    df_accuracy = df_accuracy.groupby(['actual_y']).apply(lambda x: get_accuracy(x)).rename('accuracy').reset_index()
    
    df_stats = df_errors.groupby('actual_y').agg(count=('order', 'count'),
                                            place_avg=('order', np.mean),
                                            place_q90=('order', lambda x: np.percentile(x, 90)),
                                            place_q50=('order', lambda x: np.percentile(x, 50))
                                            ).reset_index()
    
    df_stats = pd.merge(df_accuracy, df_stats, left_on='actual_y', right_on='actual_y')
    df_stats = df_stats.sort_values(by='count', ascending=False).reset_index(drop=True)

    w_accuracy = np.average(df_stats['accuracy'].values, weights=df_stats['count'].values) # Weighted accuracy
    return w_accuracy, df_stats