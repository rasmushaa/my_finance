

import numpy as np
import scipy.stats
import re


class NB():
    def __init__(self):
        self._y_encode = {}
        self._y_decode = {}
        self._X_encode = {}
        self._X_decode = {}
        self._priors = {}
        self._likelihoods = {}
        self._propabilities = {}

    def fit(self, str_features: np.array, float_features: np.array, y: np.array):
        def word_coder(values: list) -> dict:
            decode = {i: label for i, label in enumerate(set(values))}
            encode = {label: i for i, label in enumerate(set(values))}
            return encode, decode
        
        self._validate_data(str_features, float_features, y)

        nested_word_list = self._process_str_features(str_features)
        word_list = set(value for nested in nested_word_list for value in nested) # Unnest unique words

        self._X_encode, self._X_decode = word_coder(word_list)
        self._y_encode, self._y_decode = word_coder(y)

        X_float = float_features
        X_str = self._transform_X(str_features)
        y = self._transform_y(y)

        self._compute_priors(y)
        self._compute_likelihoods(X_str, y)
        self._compute_propabilities(X_float, y)


    def predict(self, str_features: np.array, float_features: np.array):
        X_str = self._transform_X(str_features)
        X_float =float_features
        predictions = []
        for str_row, float_row in zip(X_str, X_float):
            target_values = {}
            for target in self._y_decode:
                likes = [self._likelihoods[target][feature] for feature in str_row if feature in self._likelihoods[target]]
                probs = [ndist.pdf(value) for ndist, value in zip(self._propabilities[target], float_row)]
                posterrior = np.log(likes).sum() + np.log(probs).sum() + np.log(self._priors[target])
                #print(f'Post {posterrior:.1f}, Prior {np.log(self._priors[target]):.1f}, Likely {np.log(likes).sum():.1f}, Probs {np.log(probs).sum():.1f}')
                target_values.update({target: posterrior})   
            labels = {self._y_decode[k]: v for k, v in sorted(target_values.items(), key=lambda item: item[1], reverse=True)}
            predictions.append(labels)
        return predictions


    def get_priors(self):
        return {self._y_decode[k]: v for k, v in sorted(self._priors.items(), key=lambda item: item[1], reverse=True)}
    

    def _transform_X(self, str_features: np.array) -> np.array:
        X_str = self._process_str_features(str_features)
        n_cols = len(max(X_str, key=len))
        for i, row in enumerate(X_str):
            coded = [self._X_encode[word] if word in self._X_encode else -1 for word in row]
            X_str[i] = np.pad(coded, (0, n_cols - len(coded)), 'constant', constant_values=(-1))
        return np.array(X_str)
    
    def _transform_y(self, y: list) -> np.array:
        y = [self._y_encode[label] for label in y]
        return np.array(y)


    def _process_str_features(self, str_features: np.array):
        merged = np.array(list(map(lambda x : ' '.join(x), str_features))) # Merges all string columns on the same row
        nested_word_list = [re.split('\.|;|,|-|_|\*|\s+', str(row).lower()) for row in merged]
        return nested_word_list
    

    def _compute_priors(self, y: np.array):
        labels, counts = np.unique(y, return_counts=True)
        events = y.shape[0]
        probs = counts / events
        priors = {target: prior for target, prior in zip(labels, probs)} 
        self._priors = priors
    

    def _compute_likelihoods(self, X_str: np.array, y: np.array):
        targets = np.unique(y)
        for target in targets:
            sub_set = X_str[y[:] == target]
            sub_set = sub_set[(sub_set != -1)]
            features, counts = np.unique(sub_set, return_counts=True)
            known_unkowns = [k for k in self._X_decode if k not in features]
            features = np.concatenate((features, known_unkowns), axis=0)
            counts = np.concatenate((counts, np.ones(len(known_unkowns))), axis=0)
            events = (sub_set != -1).sum() + len(known_unkowns)
            probs = counts / events
            likelihood = {features: prob for features, prob in zip(features, probs)} 
            self._likelihoods.update({target: likelihood})

    def _compute_propabilities(self, X_float: np.array, y: np.array):
        targets = np.unique(y)
        for target in targets:
            sub_set = X_float[y[:] == target]
            means = np.mean(sub_set, axis=0)
            stds = np.std(sub_set, axis=0)
            ndists = [scipy.stats.norm(mean, std) for mean, std in zip(means, stds)]
            self._propabilities.update({target: ndists})

    def _validate_data(self, str_features: np.array, float_features: np.array, y: np.array):
        assert (str_features.shape[0] == float_features.shape[0] and  
                str_features.shape[0] == y.shape[0]), 'All Features X and Target y shapes must be the same'
        
        assert y.shape[0] > 0, 'Target colum must have at least one row'
        assert y.ndim == 1, 'Target column shape must be a 1 dimensional array'
        assert str_features.ndim == 2, 'String column shape must be a 2 dimensional matrix'
        assert float_features.ndim == 2, 'Numeric column shape must be a 2 dimensional matrix'
        
        if str_features.shape[1] > 0:
            for row in str_features[:, 0]:
                assert isinstance(row, str), 'All values in the String column must have a dtype of str'
        if float_features.shape[1] > 0:
            for row in float_features[:, 0]:
                assert isinstance(row, float), 'All values in the Numeric column must have a dtype of float'
        for row in y[:]:
            assert isinstance(row, str), 'All values in the Target column must have a dtype of str'