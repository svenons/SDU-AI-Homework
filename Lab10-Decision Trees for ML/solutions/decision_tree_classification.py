# Decision Tree Classification

# Importing the libraries
import numpy as np
import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn import tree
#pip install scikit-learn
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from matplotlib import pyplot as plt
import seaborn as sns

import os  
path = os.getcwd() 
os.chdir(path)
 

# Importing the dataset 
dataset = pd.read_csv('Lab10-Decision Trees for ML\social_network_ads.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# TODO: Visualize each feature and observe the plots to better understand 
# Write code scripts to plot the figures
# Combine features and target for better visualization
df = pd.DataFrame(X, columns=['Age', 'EstimatedSalary'])
df['Purchased'] = y

# Plot feature distributions
sns.pairplot(df, hue='Purchased')
plt.suptitle('Feature Distributions by Class', y=1.02)
plt.show()

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
 
# Accuracy on Training Data
y_train_pred = classifier.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Training Accuracy: {train_accuracy}")
print(f"Testing Accuracy: {accuracy}")  # already computed above

# Check for Overfitting
if train_accuracy - accuracy > 0.1:
    print("Potential overfitting detected (high training accuracy vs. lower test accuracy).")
else:
    print("No significant overfitting detected.")

# Fix Overfitting by Pruning (limit tree depth)
pruned_classifier = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
pruned_classifier.fit(X_train, y_train)
y_test_pruned = pruned_classifier.predict(X_test)
pruned_accuracy = accuracy_score(y_test, y_test_pruned)
print(f"Pruned Tree Accuracy: {pruned_accuracy}")

# Visualize the Pruned Tree
plt.figure(figsize=(20,15))
tree.plot_tree(pruned_classifier, class_names=['no', 'yes'], filled=True, rounded=True)
plt.title("Pruned Decision Tree (max_depth=3)")
plt.show()