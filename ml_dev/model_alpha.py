

import pandas as pd
import numpy as np
import re


class NB():
    def __init__(self):
        self._y_encode = {}
        self._y_decode = {}
        self._X_encode = {}
        self._X_decode = {}
        self._priors = {}
        self._likelihoods = {}

    def fit(self, X: list, y: list):
        def word_coder(values: list) -> dict:
            decode = {i: label for i, label in enumerate(set(values))}
            encode = {label: i for i, label in enumerate(set(values))}
            return encode, decode
        nested_word_list = self._process_X(X)
        corpus = set(value for nested in nested_word_list for value in nested)
        self._X_encode, self._X_decode = word_coder(corpus)
        self._y_encode, self._y_decode = word_coder(y)
        X, y = self._transform_to_X_y(X, y)
        self._compute_priors(y)
        self._compute_likelihoods(X, y)

    def predict(self, X: list):
        X = self._transform_X(X)
        predictions = []
        for row in X:
            target_values = {}
            for target in self._y_decode:
                probs = [self._likelihoods[target][feature] for feature in row if feature in self._likelihoods[target]]
                posterrior = np.log(probs).sum() + np.log(self._priors[target])
                target_values.update({target: posterrior})   
            labels = {self._y_decode[k]: v for k, v in sorted(target_values.items(), key=lambda item: item[1], reverse=True)}
            predictions.append(labels)
        return predictions

    def get_priors(self):
        return {self._y_decode[k]: v for k, v in sorted(self._priors.items(), key=lambda item: item[1], reverse=True)}
    
    def get_classes_in_desc_prior_order(self):
        priors = self.get_priors()
        return list(priors.keys())

    def _transform_to_X_y(self, X: list, y: list) -> np.array:
        X = self._transform_X(X)
        y = [self._y_encode[label] for label in y]
        return np.array(X), np.array(y)
    
    def _transform_X(self, X: list) -> np.array:
        X = self._process_X(X)
        n_cols = len(max(X, key=len))
        for i, row in enumerate(X):
            coded = [self._X_encode[word] if word in self._X_encode else -1 for word in row]
            X[i] = np.pad(coded, (0, n_cols - len(coded)), 'constant', constant_values=(-1))
        return X

    def _process_X(self, X: list):
        nested_word_list = [re.split('\.|;|,|-|_|\*|\s+', str(row).lower()) for row in X]
        return nested_word_list
    
    def _compute_priors(self, y: np.array):
        targets, counts = np.unique(y, return_counts=True)
        events = y.shape[0]
        probs = counts / events
        priors = {target: prior for target, prior in zip(targets, probs)} 
        self._priors = priors
    
    def _compute_likelihoods(self, X: np.array, y: np.array):
        targets = np.unique(y)
        for target in targets:
            sub_set = X[y[:] == target]
            sub_set = sub_set[(sub_set != -1)]
            features, counts = np.unique(sub_set, return_counts=True)
            known_unkowns = [k for k in self._X_decode if k not in features]
            features = np.concatenate((features, known_unkowns), axis=0)
            counts = np.concatenate((counts, np.ones(len(known_unkowns))), axis=0)
            events = (sub_set != -1).sum() + len(known_unkowns)
            probs = counts / events
            likelihood = {features: prob for features, prob in zip(features, probs)} 
            self._likelihoods.update({target: likelihood})