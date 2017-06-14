#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
import enron_tools
import tester


from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

# These are the features appearing on the enron dataset.
# New features will be created later and
# the best will be selecting using SelectKBest().
features_list = features_list = ['poi',
                 'bonus',
                 'deferral_payments',
                 'deferred_income',
                 'director_fees',
                 'exercised_stock_options',
                 'expenses',
                 'loan_advances',
                 'long_term_incentive',
                 'other',
                 'restricted_stock',
                 'restricted_stock_deferred',
                 'salary',
                 'total_payments',
                 'total_stock_value',
                 'from_messages',
                 'from_poi_to_this_person',
                 'from_this_person_to_poi',
                 'shared_receipt_with_poi',
                 'to_messages']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers

outliers = ['TOTAL', 'LOCKHART EUGENE E', 'THE TRAVEL AGENCY IN THE PARK']
enron_tools.remove_outliers(data_dict, outliers)

### Task 3: Create new feature(s)
enron_tools.compute_fraction_poi_communication(data_dict)
enron_tools.total_wealth_by_person(data_dict)

features_list += ['fraction_poi_communication', 'total_wealth']

### Store to my_dataset for easy export below.
my_dataset = data_dict

# Top 10 best features using SelectKBest().
best_features_list = ['poi',
                      'exercised_stock_options',
                      'total_stock_value',
                      'bonus',
                      'salary',
                      'total_wealth',
                      'deferred_income',
                      'long_term_incentive',
                      'restricted_stock',
                      'total_payments',
                      ]



### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

def tune_logistic_regression():

    skb = SelectKBest()
    pca = PCA()
    lr_clf = LogisticRegression()

    pipe_lr = Pipeline(steps=[("SKB", skb), ("PCA", pca), ("LogisticRegression", lr_clf)])

    lr_k = {"SKB__k": range(9, 10)}
    lr_params = {'LogisticRegression__C': [1e-08, 1e-07, 1e-06],
                 'LogisticRegression__tol': [1e-2, 1e-3, 1e-4],
                 'LogisticRegression__penalty': ['l1', 'l2'],
                 'LogisticRegression__random_state': [42, 46, 60]}
    lr_pca = {"PCA__n_components": range(3, 8), "PCA__whiten": [True, False]}

    lr_k.update(lr_params)
    lr_k.update(lr_pca)

    enron_tools.get_best_parameters_reports(pipe_lr, lr_k, features, labels)


def tune_svc():

    skb = SelectKBest()
    pca = PCA()
    svc_clf = SVC()

    pipe_svc = Pipeline(steps=[("SKB", skb), ("PCA", pca), ("SVC", svc_clf)])

    svc_k = {"SKB__k": range(8, 10)}
    svc_params = {'SVC__C': [1000], 'SVC__gamma': [0.001], 'SVC__kernel': ['rbf']}
    svc_pca = {"PCA__n_components": range(3, 8), "PCA__whiten": [True, False]}

    svc_k.update(svc_params)
    svc_k.update(svc_pca)

    enron_tools.get_best_parameters_reports(pipe_svc, svc_k, features, labels)


def tune_decision_tree():

    skb = SelectKBest()
    pca = PCA()
    dt_clf = DecisionTreeClassifier()

    pipe = Pipeline(steps=[("SKB", skb), ("PCA", pca), ("DecisionTreeClassifier", dt_clf)])

    dt_k = {"SKB__k": range(8, 10)}
    dt_params = {"DecisionTreeClassifier__min_samples_leaf": [2, 6, 10, 12],
                 "DecisionTreeClassifier__min_samples_split": [2, 6, 10, 12],
                 "DecisionTreeClassifier__criterion": ["entropy", "gini"],
                 "DecisionTreeClassifier__max_depth": [None, 5],
                 "DecisionTreeClassifier__random_state": [42, 46, 60]}
    dt_pca = {"PCA__n_components": range(4, 7), "PCA__whiten": [True, False]}

    dt_k.update(dt_params)
    dt_k.update(dt_pca)

    enron_tools.get_best_parameters_reports(pipe, dt_k, features, labels)


def tune_random_forest():

    skb = SelectKBest()
    rf_clf = RandomForestClassifier()

    pipe_rf = Pipeline(steps=[("SKB", skb), ("RandomForestClassifier", rf_clf)])

    rf_k = {"SKB__k": range(8, 11)}
    rf_params = {'RandomForestClassifier__max_depth': [None, 5, 10],
                  'RandomForestClassifier__n_estimators': [10, 15, 20, 25],
                  'RandomForestClassifier__random_state': [42, 46, 60]}

    rf_k.update(rf_params)

    enron_tools.get_best_parameters_reports(pipe_rf, rf_k, features, labels)


def tune_ada_boost():

    skb = SelectKBest()
    ab_clf = AdaBoostClassifier()

    pipe_ab = Pipeline(steps=[("SKB", skb), ("AdaBoostClassifier", ab_clf)])

    ab_k = {"SKB__k": range(8, 11)}
    ab_params = {'AdaBoostClassifier__n_estimators': [10, 20, 30, 40],
                 'AdaBoostClassifier__algorithm': ['SAMME', 'SAMME.R'],
                 'AdaBoostClassifier__learning_rate': [.8, 1, 1.2, 1.5]}

    ab_k.update(ab_params)

    enron_tools.get_best_parameters_reports(pipe_ab, ab_k, features, labels)


if __name__ == '__main__':

    '''         GAUSSIAN NAIVE BAYES            '''

    clf = GaussianNB()
    print "Gaussian Naive Bayes : \n", tester.test_classifier(clf, my_dataset, best_features_list)


    '''         LOGISTIC REGRESSION             '''

    #tune_logistic_regression()

    best_features_list_lr = enron_tools.get_k_best(my_dataset, features_list, 9)

    clf_lr = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=4, whiten=False)),
        ('classifier', LogisticRegression(tol=0.01, C=1e-08, penalty='l2', random_state=42))])

    print "Logistic Regression : \n", tester.test_classifier(clf_lr, my_dataset, best_features_list_lr)


    '''         SUPPORT VECTOR CLASSIFIER           '''

    #tune_svc()

    best_features_list_svc = enron_tools.get_k_best(my_dataset, features_list, 8)

    clf_svc = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=6, whiten=True)),
        ('classifier', SVC(C=1000, gamma=.001, kernel='rbf'))])

    print "Support Vector Classifier : \n", tester.test_classifier(clf_svc, my_dataset, best_features_list_svc)


    '''         DECISION TREE CLASSIFIER            '''

    #tune_decision_tree()

    best_features_list_dt = enron_tools.get_k_best(my_dataset, features_list, 8)

    clf_dt = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=5, whiten=True)),
        ('classifier', DecisionTreeClassifier(criterion='entropy',
                                              min_samples_leaf=2,
                                              min_samples_split=2,
                                              random_state=46,
                                              max_depth=None))
    ])

    print "Decision Tree Classifier : \n",tester.test_classifier(clf_dt, my_dataset, best_features_list_dt)


    '''         RANDOM FOREST CLASSIFIER              '''

    #tune_random_forest()

    best_features_list_rf = enron_tools.get_k_best(my_dataset, features_list, 9)

    clf_rf = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(max_depth=5,
                                              n_estimators=25,
                                              random_state=42))
    ])

    print "Random Forest Classifier : \n", tester.test_classifier(clf_rf, my_dataset, best_features_list_rf)


    '''         ADA BOOST CLASSIFIER            '''

    #tune_ada_boost()

    best_features_list_ab = enron_tools.get_k_best(my_dataset, features_list, 9)

    clf_ab = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('classifier', AdaBoostClassifier(learning_rate=1.5,
                                          n_estimators=30,
                                          algorithm='SAMME.R'))
    ])

    print "Ada Boost Classifier : \n", tester.test_classifier(clf_ab, my_dataset, best_features_list_ab)



    '''         dump final algorithm classifier, dataset and features in the data directory         '''
    #dump_classifier_and_data(clf_lr, my_dataset, best_features_list_lr)


# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)