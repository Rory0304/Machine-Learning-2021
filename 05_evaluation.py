# -*- coding: utf-8 -*-
"""05.Evaluation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tmBP61OrK0ooIdlMd3B0py__EytCW-SB
"""

!wget http://www.aueb.gr/users/ion/data/enron-spam/preprocessed/enron1.tar.gz

!tar -zxvf enron1.tar.gz

file_path = 'enron1/ham/0007.1999-12-14.farmer.ham.txt'

with open(file_path, 'r') as infile:
  ham_sample = infile.read()

print(ham_sample)

import glob

mails = [] #메일 전체를 저장 (x좌표)
labels = [] #ham은 0, spam은 1로 저장 (y좌표)

# spam file을 읽음
for filename in glob.glob('enron1/spam/*.txt'):
  with open(filename, 'r', encoding='iso-8859-1') as infile:
    mails += [infile.read()]
    labels += [1] #[1,1,1,1...]

# ham file을 읽음
for filename in glob.glob('enron1/ham/*.txt'):
  with open(filename, 'r', encoding='iso-8859-1') as infile:
    mails += [infile.read()]
    labels += [0] #[0,0,0,0...]

#텍스트 전처리

import nltk
nltk.download('names') #사람 이름 제거
nltk.download('wordnet') #표제어 원형 복원

from nltk.corpus import names
from nltk.stem import WordNetLemmatizer

all_names = set(names.words())
lemmatizer = WordNetLemmatizer()

def clean_text(docs):
  cleaned_docs = []
  for doc in docs:
    lemmatized_list = [ 
                       lemmatizer.lemmatize(word.lower())
                       for word in doc.split()
                       if word.isalpha() and word not in all_names
                       ]
    cleaned_docs += [''.join(lemmatized_list)]
  return cleaned_docs

cleaned_mails = clean_text(mails) #mails 리스트를 텍스트 전처리

cleaned_mails[0]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(cleaned_mails,
                                                    labels,
                                                    test_size=0.2,
                                                    random_state=0)

#test_size(0.2)는 train(80)과 test(20) 데이터의 비중을 나눔
#random_state : random하게 선택해서 데이터를 나눔, 다시 실행했을 때 random 선택을 조절할 수 있도록 함.

#문서 모델 생성
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words='english', max_features=500) #무시할 수 있는 단어 제거
term_docs_train = cv.fit_transform(X_train) #train에 대해서는 fit transform
term_docs_test = cv.transform(X_test) #test 대해서는 transform

#Naive Bayes 모델 학습, 스팸이냐 아니냐 구분
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB(alpha=1.0, fit_prior=True)
clf.fit(term_docs_train, y_train) #학습 모델 생성

prediction_prob = clf.predict_proba(term_docs_test)
prediction_prob

prediction = clf.predict(term_docs_test)
prediction

from sklearn.metrics import confusion_matrix

prediction = clf.predict(term_docs_test)
confusion_matrix(y_test, prediction, labels = [0,1])

from sklearn.metrics import precision_score, recall_score, f1_score

accuracy = clf.score(term_docs_test, y_test)
print('Accuracy: {:.1f}%'.format(accuracy*100))
precision = precision_score(y_test, prediction, pos_label=1)
print('Precision: {:.1f}%'.format(precision*100))
recall = recall_score(y_test, prediction, pos_label=1)
print('Recall: {:.1f}%'.format(recall*100))
f1 = f1_score(y_test, prediction, pos_label=1)
print('F1-score: {:.1f}%'.format(f1*100))

from sklearn.metrics import classification_report
print(classification_report(y_test, prediction))

from sklearn import metrics
import matplotlib.pyplot as plt
fpr, tpr, thresholds = metrics.roc_curve(y_test,
prediction_prob[:, 1],
pos_label=1)
fig, ax = plt.subplots(figsize=(7, 7))
ax.plot([0, 1], [0, 1], 'k--')
ax.plot(fpr, tpr)
plt.xlabel('1-Specificity')
plt.ylabel('Sensitivity')
plt.title('ROC curve')
auc = metrics.roc_auc_score( y_test, prediction_prob[:, 1] )
textstr = 'AUC = {:.3f}'.format(auc)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.5, 0.1, textstr, fontsize=14, bbox=props)
plt.show()

