# Identifying Fraud From Enron Emails and Financial Data

**Isabel María Villalba Jiménez**

June 16, 2017

##Project Overview

The goal of this project is to be able to detect people committing fraude using a vast dataset of emails between employees of ENRON.  

Enron Corporation was an American company based in Houston, Texas and founded in 1985. Before its bankruptcy on December, 2001, Enron had 20,000 employees and was one of the world's major electricity, natural gas, communications and pulp and paper companies, with claimed revenues of nearly $101 billion during 2000.

At the end of 2001, the  **Enron scandal** emerged, being revealed that the reported financial condition was false and it was sustained by institutionalized, systematic, and creatively planned accounting fraud. 

Enron has since become a well-known example of willful corporate fraud and corruption. The scandal brought into question the accounting practices and activities of many corporations in the United States and was a factor in the enactment of the Sarbanes–Oxley Act of 2002 [[Source]](https://en.wikipedia.org/wiki/Enron).



##1. Dataset and Outliers
The dataset has a total of **146 people** entries with **21 features** each. From the people there are **18 POIs** and **128 Non POIs**.

After making exploratory analysis I found the following information abouth these variables:

* ``TOTAL``:  has many outliers with extreme values.
* ```THE TRAVEL AGENCY IN THE PARK```: Not representative of an individual
* ```LOCKHART EUGENE E```: all NaN values.


##2. Features Selection and Scaling
## What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? 

In orderto complement the 21 features, I created 4 additional features to complement them and have better predictions.

* `fraction_from_poi`: fraction of emails received from POIs.
* `fraction_to_poi`: fraction of emails sent to POIs.
* `fraction_poi_total`: fraction of emails related to POIs. Proportion of messages are between POIs compared to overall messages.
* `wealth`: salary, total stock value, exercised stock options and bonuses.


This is the rank returned by ```SelectKBest``` showing the importance of each variable of the dataset:

| Features                      | Scores   | 
| ----------------------------- |:--------:| 
| Exercised Stock Options       |  25.1| 
| Total Stock Value             | 24.47   |  
| Bonus                         | 21.06  |
| Salary			|  18.58  |
| Fraction to POI		| 16.64 |
| Wealth 					  | 15.55  |
| Deferred Income				  | 11.6   |
| Long Term Incentive           | 10.07    |
| Restricted Stock				  | 9.35    |
| Total Payments				  	  | 8.87    |
| Shared Receipt with POI       | 8.75    |
| Loan Advances 		|7.24|
| Expenses			|6.23|
| Fraction POI from total comm.	|5.52|
| Other				|4.2|
| Fraction from POI		|3.21|
| Deferral Payments		|0.21|
| Restricted Stock Deferred 	|0.06|

> I decided to use the 3 first features since after selecting a higher number, I could check there was not  clear improvement in the predictions of the algorithms that I will describe below. 

The features selected are, hence: 

| Features                      | Scores   | 
| ----------------------------- |:--------:| 
| Exercised Stock Options       |  25.1| 
| Total Stock Value             | 24.47   |  
| Bonus                         | 21.06  |

It seems that knowing how deep you involved into Stocks and how much money you receive from Bonuses may suffice to tell whether you can be a POI or not.

**Features Scaling :**  Before passing the data to the classifiers to train, we must normalized them. It is used to standardize the range of features in the data. In this case, I have used a common scaller from Scikit-learn named ```MinMaxScaler()``` which sets the data to the range 0-1 [[Reference]](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html).

##3. Parameters Tuning
I tested three different algorithms, performing a `scikit-learn` `GridSearchCV` parameter optimization on each of them:

###GaussianNB
........
Precision: 0.436988095238
Recall: 0.294571428571

##DecisionTree:
..........
Precision: 0.21119047619
Recall: 0.140321428571
criterion='entropy', 
max_depth=None, 
max_leaf_nodes=5, 
min_samples_leaf=1, 
min_samples_split=2, 

##AdaBoost:
..........
Precision: 0.321896825397
Recall: 0.156273809524
algorithm='SAMME', 
learning_rate=1, 
n_estimators=10, 


The best behavior is shown by the GaussianNB classifier, with better recall and precision than the others.

Gaussian Naïve Bayes, shows a better recall (i.e. the proportion of individuals identified as POIs, who actually are POIs) compared to other algorithms, at a slight expense of precision (i.e. proportion of POIs who have successfully been identified).

##4. Validation
Finally, the classifier performance is tested against a subset of data separated from the training data.  This way, we can predict how the algorithm will perform against new data in the future, and tune other parameters in consequence. The final step will be to test the algorithm with real data after performing the validation.

For the validation it will be used the `StratifiedShuffleSplit` method from Scikit-Learn. This method splits the data in K different folds, alowing to perform the training and validation data K times and have an estimate of the perfomance [[source]](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html#sklearn.model_selection.StratifiedShuffleSplit). This method is quite used when the amount of data available is restricted and we need to make use of all the data. 

The validation of the algorith was made using 50 randomized trials and returned the mean value of the performance metrics selected.Since the dataset is quite imbalanced in terms of POIs vs non-POIs, **accuracy** is not a good metric. In this case it is better to use  **precision** and **recall** instead:

```
Average precision: 0.54 
Average recall: 0.45 

```

#5 Test

The performance of the algorithm agter running the test has been:                                         

```
Precision: 0.44
Recall: 0.3
```                                              
It is a good result since it follows the validation values and show no overfitting.
  
#Sources

- [ENRON @ Wikipedia](https://en.wikipedia.org/wiki/Enron)
- [MinMaxScaler @ scikit-learn.org](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
- [Precision and recall @ scikit-learn.org](http://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)
- [StratifiedShuffleSplit @ scikit-learn.org](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html#sklearn.model_selection.StratifiedShuffleSplit)
- [Identifying Fraud from Enron Emails and Financial Data by Philip Seifi](https://github.com/seifip/udacity-data-analyst-nanodegree/tree/master/P5%20-%20Identifying%20Fraud%20from%20Enron%20Emails%20and%20Financial%20Data)
- [Identifying Fraud from Enron Emails and Financial Data by Pratyush Kumar](https://github.com/pratyush19/Udacity-Data-Analyst-Nanodegree/tree/master/P5-Identifying-Fraud-From-Enron-Emails-and-Financial-Data)

