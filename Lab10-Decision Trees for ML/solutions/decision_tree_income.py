# Exercise 2 – Classification on Adult Income Data

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ----------------------------------------
# Step 1: Load and explore the dataset
# ----------------------------------------

df = pd.read_csv('Lab10-Decision Trees for ML\\adult_income.csv')

print("First few rows of the dataset:")
print(df.head(), "\n")

print("Summary of dataset:")
print(df.info(), "\n")

print("Class distribution for 'income_high':")
print(df['income_high'].value_counts(), "\n")

# ----------------------------------------
# Step 2: Visualize dataset features
# ----------------------------------------

# Age distribution by income class
sns.histplot(data=df, x='age', hue='income_high', multiple='stack', bins=20)
plt.title("Age Distribution by Income Class")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

# Hours per week distribution by income
sns.boxplot(data=df, x='income_high', y='hours_per_week')
plt.title("Working Hours per Week by Income")
plt.show()

# Education vs income
sns.countplot(data=df, x='education_num', hue='income_high')
plt.title("Education Level by Income")
plt.show()

# ----------------------------------------
# Step 3: Prepare data for modeling
# ----------------------------------------

# Drop ID if present
if 'ID' in df.columns:
    df.drop(columns=['ID'], inplace=True)

# Encode categorical columns
categorical_cols = df.select_dtypes(include='object').columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and label
X = df.drop(columns='income_high')
y = df['income_high']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# ----------------------------------------
# Step 4: Train basic decision tree model
# ----------------------------------------

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("Initial Model Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Visualize full tree (limited depth for readability)
plt.figure(figsize=(20, 12))
plot_tree(clf, feature_names=X.columns,
          class_names=['Low', 'High'], filled=True, max_depth=3)
plt.title("Decision Tree (partial view up to depth=3)")
plt.show()

# ----------------------------------------
# Step 5: Check for overfitting
# ----------------------------------------

train_acc = accuracy_score(y_train, clf.predict(X_train))
test_acc = accuracy_score(y_test, y_pred)

print(f"Training Accuracy: {train_acc}")
print(f"Testing Accuracy: {test_acc}")

if train_acc - test_acc > 0.1:
    print("Potential overfitting detected. Training accuracy is much higher than test accuracy.")
else:
    print("No significant overfitting detected.")

# ----------------------------------------
# Step 6: Apply pruning to reduce overfitting
# ----------------------------------------

pruned_clf = DecisionTreeClassifier(
    random_state=42, max_depth=5, min_samples_split=20)
pruned_clf.fit(X_train, y_train)

y_pruned_pred = pruned_clf.predict(X_test)

print("Pruned Model Performance:")
print("Accuracy:", accuracy_score(y_test, y_pruned_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pruned_pred))
print("Classification Report:")
print(classification_report(y_test, y_pruned_pred))

# Visualize pruned tree
plt.figure(figsize=(20, 12))
plot_tree(pruned_clf, feature_names=X.columns,
          class_names=['Low', 'High'], filled=True, max_depth=3)
plt.title("Pruned Decision Tree (partial view up to depth=3)")
plt.show()