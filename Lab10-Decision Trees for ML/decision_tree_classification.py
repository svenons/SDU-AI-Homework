# Decision Tree Classification

# Importing the libraries
import numpy as np
import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from matplotlib import pyplot as plt

#import os  
#path = os.getcwd() 
#os.chdir(path)
 

# Importing the dataset 
dataset = pd.read_csv('./Desktop/Social_Network_Ads.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# TODO: Visualize each feature and observe the plots to better understand 
# Write code scripts to plot the figures


# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0) # 80% train, 20% test
 

# Training the Decision Tree Classification model on the Training set
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0) # Use 'gini' for Gini impurity
classifier.fit(X_train, y_train)


# Predicting the Test set results
y_pred = classifier.predict(X_test)


#  Evaluate the model by making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred) 
print(f"Confusion Matrix: \n {cm}")
 
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
 

# Visualize the decision tree  
plt.figure(figsize=(25,20))
tree.plot_tree(classifier, class_names=['no', 'yes'],  filled=True, rounded=True)
plt.show()


# Predicting a new result
new_data=[[30,87000]]
prediction = classifier.predict(new_data)
print(f"Prediction for new data: {prediction}")
 
# TODO: Observe the plotted tree to see if it is too complex or not
# write a code check whether or not there is an overfitting
# if the model is overfitting, fix the overfitting and show the plot results for before and after

