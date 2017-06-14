#!/usr/bin/python

import sys
import csv
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit

# Import models from sklearn 
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit



def remove_outliers(data_dict, indices):
    # Remove from data_dictk the elements in indices;
    for index in indices:
        data_dict.pop(index, 0)

def compute_fraction_poi_communication(data_dict):

    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """

    features = ['to_messages', 'from_messages', 'from_this_person_to_poi', 'from_poi_to_this_person']

    for key in data_dict:
        d = data_dict[key]

        is_null = False
        for feature in features:
            #See if eny feature is NaN
            if d[feature] == 'NaN':
                is_null = True

        if not is_null:
            d['fraction_poi_communication'] = float(d['from_this_person_to_poi'] + d['from_poi_to_this_person']) / \
                                                        float(d['to_messages'] + d['from_messages'])
        else:
            d['fraction_poi_communication'] = 'NaN'


def total_wealth_by_person(data_dict):
    # This functions retunrs the total wealth that each person in the company has.
    features = ['salary', 'bonus', 'total_stock_value', 'exercised_stock_options']

    for key in data_dict:
        d = data_dict[key]

        is_null = False
        for feature in features:
            if d[feature] == 'NaN':
                is_null = True

        if not is_null:
            d['total_wealth'] = d['salary'] + d['total_stock_value'] +\
                                    d['bonus'] + d['exercised_stock_options']
        else:
            d['total_wealth'] = 'NaN'

def get_k_best(data_dict, features_list, k):

    data = featureFormat(data_dict, features_list)
    labels_train, features_train = targetFeatureSplit(data)

    k_best = SelectKBest(f_classif, k=k)
    k_best.fit(features_train, labels_train)

    unsorted_list = zip(features_list[1:], k_best.scores_)
    sorted_list = sorted(unsorted_list, key=lambda x: x[1], reverse=True)
    k_best_features = dict(sorted_list[:k])

    return ['poi'] + k_best_features.keys()


def get_best_parameters_reports(clf, parameters, features, labels):


    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=60)


    cv_strata = StratifiedShuffleSplit(labels_train, 100, test_size=0.2, random_state=60)

    grid_search = GridSearchCV(clf, parameters, n_jobs=-1, cv=cv_strata, scoring='f1')
    grid_search.fit(features_train, labels_train)

    '''
    prediction = grid_search.predict(features_test)
    print 'Precision:', precision_score(labels_test, prediction)
    print 'Recall:', recall_score(labels_test, prediction)
    print 'F1 Score:', f1_score(labels_test, prediction)
    '''

    print 'Best score: %0.3f' % grid_search.best_score_
    print 'Best parameters set:'
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print '\t%s: %r' % (param_name, best_parameters[param_name])


