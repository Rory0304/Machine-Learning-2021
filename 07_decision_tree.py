# -*- coding: utf-8 -*-
"""07_Decision Tree

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iVr09jYPlAPEVBCGx4cDPAxuL24XkIvS
"""

import pandas as pd

data = pd.read_csv('ctr_data_20000.csv')

data.head()

print(data.columns)

data = data.drop(['id', 'hour', 'device_id', 'device_ip'], axis=1)
print(data.columns)

## 클릭률에 따른 데이터 분류
X = data.loc[:, data.columns != 'click'].astype('str')
Y = data.loc[:, data.columns == 'click'].astype('int').values.ravel()

X_dic = X.to_dict('records')

print(X_dic[0])

from sklearn.feature_extraction import DictVectorizer

one_hot_encoder = DictVectorizer()

onehot_X = one_hot_encoder.fit_transform(X_dic)

print(X.shape)
print(onehot_X.shape)

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

train_X, test_X = onehot_X[0:15000], onehot_X[15000:]
train_y, text_y = Y[0:15000], Y[15000:]

# 평가 척도가 gini 계수임
decision_tree = DecisionTreeClassifier(criterion='gini', min_samples_split=30)
parameters = {'max_depth': [3,10,None]}

grid_search = GridSearchCV(decision_tree, parameters, cv=3, scoring='accuracy'
) # grid search 모델을 생성

grid_search.fit(train_X, train_y)

print(grid_search.best_params_)

from sklearn.metrics import classification_report

model_best = grid_search.best_estimator_

prediction = model_best.predict(test_X)

print(classification_report(text_y, prediction))
