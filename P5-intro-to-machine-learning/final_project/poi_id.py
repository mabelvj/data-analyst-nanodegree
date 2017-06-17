#!/usr/bin/python

import sys
import pickle
import random
import matplotlib
from matplotlib import pyplot
sys.path.append("../tools/")

from numpy import mean
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
from sklearn.grid_search import GridSearchCV

import pandas as pd
import numpy as np



### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi'] # You will need to use more features

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )

### Task 2: Remove outliers

### EXPLORATION

num_data_points = len(data_dict)
num_data_features = len(data_dict[data_dict.keys()[0]])

num_poi = 0
for dic in data_dict.values():
	if dic['poi'] == 1: num_poi += 1

print "Data points: ", num_data_points
print "Features: ", num_data_features
print "POIs: ", num_poi

#
#
#
# Clean data
#
#
#

count = 0
for k, v in data_dict.items():
	if v['salary'] != 'NaN' and v['salary'] > 10000000:
		count = count + 1;
print count," extreme value in 'salary'";
#There is an extreme outlier in salary

#TOTAL  turn out to be the sum of the salaries & bonuses list, let's remove it

del data_dict["TOTAL"]

del data_dict["THE TRAVEL AGENCY IN THE PARK"] # not representative

del data_dict["LOCKHART EUGENE E"] #All NaN



print('\n==================================================================\n')
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = pd.DataFrame(data_dict)

##
# Count NaNs
print("Counting NaNs")
print ((my_dataset == 'NaN').sum(axis = 1).sort_values(ascending = False))
print('\n -----------------------------------------------------------------\n')
## Custom aggregate features
## Communication
def communication_poi(my_dataset):
# We iterate over the entire dataset to extract poi communcation
	data = my_dataset.copy(deep = True)
	new_data = pd.DataFrame()
	for item in data:
		#iterate over the columns of the dataframe. Columns contains people.
		person = data[item]
		person_data = dict() #new data to be calculated and appended
		if (all([	person['from_poi_to_this_person'] != 'NaN',
					person['from_this_person_to_poi'] != 'NaN',
					person['to_messages'] != 'NaN',
					person['from_messages'] != 'NaN'
				])):
			fraction_from_poi = float(person["from_poi_to_this_person"]) / float(person["to_messages"])
			person_data["fraction_from_poi"] = fraction_from_poi
			fraction_to_poi = float(person["from_this_person_to_poi"]) / float(person["from_messages"])
			person_data["fraction_to_poi"] = fraction_to_poi
			fraction_total_poi = float(person['from_this_person_to_poi'] + person['from_poi_to_this_person']) / \
													float(person['to_messages'] + person['from_messages'])
			person_data["fraction_total_poi"] = fraction_total_poi
		else:
			person_data["fraction_from_poi"] = person_data["fraction_to_poi"] =  person_data["fraction_total_poi"] =0

		new_data[item] = pd.Series(person_data) #add column

	return pd.concat([data, new_data], axis=0) #save the value and update my_dataset


my_dataset= communication_poi(my_dataset).copy(deep = True)
## Financial:
def wealth(my_dataset):
	## Calculates the wealth as the sum of salary, total stock value
	# exercised stock options and bonuses.
	data = my_dataset.copy(deep = True)
	new_data = pd.DataFrame()

	for item in data:
		person = data[item]
		person_data = dict() #new data to be calculated and appended
		if (all([	person['salary'] != 'NaN',
					person['total_stock_value'] != 'NaN',
					person['exercised_stock_options'] != 'NaN',
					person['bonus'] != 'NaN'
				])):
			person_data['wealth'] = sum([person[field] for field in ['salary',
															   'total_stock_value',
															   'exercised_stock_options',
															   'bonus']])
		else:
		    person_data['wealth'] = 'NaN'
		new_data[item] = pd.Series(person_data) #add column

	return pd.concat([data, new_data], axis=0) #save the value and update my_dataset


my_dataset = wealth(my_dataset).copy(deep = True);

## Features to be used in the prediction
my_features = features_list + ['fraction_from_poi',
							   'fraction_to_poi',
							   'fraction_total_poi',
							   'shared_receipt_with_poi', #this is interesting. Maybe POI share receipts trying to commit fraud
							   'expenses',
							   'loan_advances',
							   'long_term_incentive',
							   'other',
							   'restricted_stock',
							   'restricted_stock_deferred',
							   'deferral_payments',
							   'deferred_income',
							   'salary',
							   'total_stock_value',
							   'exercised_stock_options',
							   'total_payments',
							   'bonus',
							   'wealth']

### Extract features and labels from dataset for local testing

data = featureFormat(my_dataset, my_features, sort_keys = True)

labels, features = targetFeatureSplit(data)

print "Intuitive features:\n", pd.DataFrame(my_features)
print ('\n----------------------------------------------------------------- \n')

# Scale features to make better predictions
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

# K-best features


def kbest_performance(features, labels):
	from sklearn.naive_bayes import GaussianNB
	from sklearn.metrics import precision_recall_curve
	from sklearn.model_selection import StratifiedShuffleSplit
	# Check the performance of the classifier when adding more features
	
	features = np.array(features)
	labels = np.array(labels)
	precision = []
	recall = []
	sss = StratifiedShuffleSplit(n_splits=20, test_size=0.3, random_state=19)

	for train_index, test_index in sss.split(features, labels):
	   #print("TRAIN:", train_index, "TEST:", test_index)
		X_train, X_test = features[train_index], features[test_index]
		y_train, y_test = labels[train_index], labels[test_index]
		clf = GaussianNB() # Final selected model
		clf.fit(X_train, y_train)
		y_pred = clf.predict(X_test)		
		p = precision_score(y_test,y_pred)
		r = recall_score(y_test,y_pred)   
		precision.append(p)
   		recall.append(r)

	#print "Average precision: %.2f \n" %np.mean(np.array(precision))
	#print "Average recall: %.2f \n" %np.mean(np.array(recall))

   	return([np.mean(np.array(precision)),np.mean(np.array(recall))])


## Try different values for k
k_array = range(2, np.array(my_features).size, 1)
precision = [];
recall = [];

for v in k_array:

 	k_best = SelectKBest(k = v)
 	k_best.fit(features, labels)

 	results_list = zip(k_best.get_support(), my_features[1:], k_best.scores_)
	results_list = sorted(results_list, key=lambda x: x[2], reverse=True)

 	## Create pandas to prettify the results

 	results_df = pd.DataFrame(results_list)

 	## 3 best features chosen by SelectKBest
 	# feature_list = 'poi'
 	my_features_ = features_list + results_df[1][results_df[0]==True].values.tolist()

 	data_ = featureFormat(my_dataset, my_features_, sort_keys = True)
 	labels_, features_ = targetFeatureSplit(data_)
 	p, r = kbest_performance(features_, labels_)
 	precision.append(p)
 	recall.append(r)


import matplotlib.pyplot as plt


p1 = plt.figure()
plt.plot(k_array, precision, 'o-', label = 'precision')
plt.plot(k_array, recall, 'o-', label = 'recall')
plt.title('Precision and Recall')

plt.xlabel('k')
plt.ylim([0.0,1.0])
plt.legend()
#plt.show()
p1.savefig('pr.png')

## Value selected of k = 7

k_best = SelectKBest(k = 7)
k_best.fit(features, labels)

results_list = zip(k_best.get_support(), my_features[1:], k_best.scores_)
results_list = sorted(results_list, key=lambda x: x[2], reverse=True)

## Create pandas to prettify the results

results_df = pd.DataFrame(results_list)
print "K-best features:\n", results_df
print ('\n----------------------------------------------------------------- \n')

## 3 best features chosen by SelectKBest
# feature_list = 'poi'
my_features = features_list + results_df[1][results_df[0]==True].values.tolist()

data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

def test_clf(grid_search, features, labels, parameters, iterations=100):
	precision, recall = [], []
	for iteration in range(iterations):
		features_train, features_test, labels_train, labels_test = train_test_split(features, labels, random_state=iteration)
		grid_search.fit(features_train, labels_train)
		predictions = grid_search.predict(features_test)
		precision = precision + [precision_score(labels_test, predictions)]
		recall = recall + [recall_score(labels_test, predictions)]
		if iteration % 10 == 0:
			sys.stdout.write('.')
	print '\nPrecision:', mean(precision)
	print 'Recall:', mean(recall)
	best_params = grid_search.best_estimator_.get_params()
	for param_name in sorted(parameters.keys()):
		print '%s=%r, ' % (param_name, best_params[param_name])

# Gaussian #http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
parameters = {}
grid_search = GridSearchCV(clf, parameters)
print '\nGaussianNB:'
test_clf(grid_search, features, labels, parameters)

## Decission tree 
from sklearn import tree
clf = tree.DecisionTreeClassifier()

parameters = {'criterion': ['gini', 'entropy'],
              'min_samples_split': [2, 5, 10],
              'max_depth': [None, 1,2, 5],
              'min_samples_leaf': [1, 5, 10],
              'max_leaf_nodes': [None, 5, 10]}
grid_search = GridSearchCV(clf, parameters)
print '\nDecisionTree:'
test_clf(grid_search, features, labels, parameters)

## AdaBoost
from sklearn.ensemble import AdaBoostClassifier
clf = AdaBoostClassifier()
parameters = {'n_estimators': [2, 5, 10],
              'algorithm': ['SAMME', 'SAMME.R'],
              'learning_rate': [.5,.8, 1, 1.2]}
grid_search = GridSearchCV(clf, parameters)
print '\nAdaBoost:'
test_clf(grid_search, features, labels, parameters)

# GaussianNB:
# Precision: 0.436988095238
# Recall: 0.294571428571

# DecisionTree:
# ..........
# Precision: 0.21119047619
# Recall: 0.140321428571
# criterion='entropy', 
# max_depth=None, 
# max_leaf_nodes=5, 
# min_samples_leaf=1, 
# min_samples_split=2, 

# AdaBoost:
# ..........
# Precision: 0.321896825397
# Recall: 0.156273809524
# algorithm='SAMME', 
# learning_rate=1, 
# n_estimators=10,  


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

# Cross validation
from sklearn.model_selection import StratifiedShuffleSplit
#from sklearn.metrics import precision_recall_curve

sss = StratifiedShuffleSplit(n_splits=20, test_size=0.3, random_state=19)
sss.get_n_splits(features, labels)

print(sss)       

precision = []
recall = []

features = np.array(features)
labels = np.array(labels)
for train_index, test_index in sss.split(features, labels):
   #print("TRAIN:", train_index, "TEST:", test_index)
   X_train, X_test = features[train_index], features[test_index]
   y_train, y_test = labels[train_index], labels[test_index]
   clf.fit(X_train, y_train)
   y_pred = clf.predict(X_test)
   p = precision_score(y_test,y_pred)
   r = recall_score(y_test,y_pred)
   precision.append(p)
   recall.append(r)

print "Average precision: %.2f \n" %np.mean(np.array(precision))
print "Average recall: %.2f \n" %np.mean(np.array(recall))


test_clf(grid_search, features, labels, parameters)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, my_features)


