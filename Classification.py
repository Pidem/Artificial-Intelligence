# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 21:46:20 2017

@author: p_mal
"""

#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

dataframe=pd.read_csv(str(sys.argv[1]),header=None)
output=[]

#%matplotlib inline
#plt.scatter(dataframe["A"],dataframe["B"],c=dataframe["label"].apply(lambda x: "red" if x==1 else "blue"),marker="o",s=50)
#plt.show()

#Split in train data set and test data set
xtrain, xtest, ytrain, ytest = train_test_split(dataframe[["A","B"]], dataframe["label"], test_size=0.4)
#print(xtrain.shape,ytrain.shape)
#print(xtest.shape,ytest.shape)

#SVM
parameter1=[{'kernel': ['linear'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}]
clf=GridSearchCV(SVC(C=1),parameter1,cv=5)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["SVM",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])


parameter2=[{'kernel':['poly'],'C':[0.1, 1, 3],'degree':[4,5,6],'gamma':[0.1, 0.5]}]
clf=GridSearchCV(SVC(C=1),parameter2,cv=5)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["SVM",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])


parameter3=[{'kernel': ['rbf'], 'gamma': [0.1, 0.5, 1, 3, 6, 10],'C': [0.1, 0.5, 1, 5, 10, 50, 100]}]
clf=GridSearchCV(SVC(C=1),parameter3,cv=5)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["SVM",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])


#Logistic Regression 
parameter4 = {'C': [0.1, 0.5, 1, 5, 10, 50, 100] }
clf = GridSearchCV(LogisticRegression(), parameter4)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["Logistic Regression",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])


#KNN 
parameter5 = {'n_neighbors':[i for i in range(1,51)],'leaf_size':[i for i in range(5,65,5)]}
clf = GridSearchCV(KNeighborsClassifier(), parameter5)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["k-nearest Neighbors",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])



#Tree Classifier
parameter6 = {'max_depth':[i for i in range(1,51)],'min_samples_split':[i for i in range(2,11)]}
clf = GridSearchCV(DecisionTreeClassifier(), parameter6)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["Decision Trees",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])


#Random Forest
parameter7 = {'max_depth':[i for i in range(1,51)],'min_samples_split':[i for i in range(2,11)]}
clf = GridSearchCV(RandomForestClassifier(), parameter7)
clf.fit(xtrain,ytrain)
#print(clf.best_params_)
#print(clf.best_score_)
#print(clf.cv_results_["mean_test_score"])
#print(clf.score(xtest,ytest))
output.append(["Random Forest",clf.best_params_,clf.best_score_,clf.score(xtest,ytest)])



#Output Datafile
OutputDataframe=pd.DataFrame(output)
OutputDataframe.to_csv(sys.argv[2])

