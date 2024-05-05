import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
import pickle
data = pd.read_csv("dataset.csv")
print("Top 10 rows of the data")
print(data.head())
print("shape of the dataframe")
print(data.shape)
print("columns of the dataset")
print(data.columns)
print("Info of the dataset")
print(data.info())
print("check for unique values in each feature")
print(data.nunique())
print("rwmoving index column")
data = data.drop(['index'],axis = 1)
print(data.describe().T)
print("pie chart")
data['Result'].value_counts().plot(kind='pie',autopct='%1.2f%%')
plt.title("Phishing Count")
plt.show()
X = data.drop(["Result"],axis =1)
y = data["Result"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

gb_clf = GradientBoostingClassifier(max_depth=4,learning_rate=0.7)

gb_clf.fit(X_train,y_train)
y_train_gbc = gb_clf.predict(X_train)
y_test_gbc = gb_clf.predict(X_test)
print("confusion matrix")
print(confusion_matrix(y_test, y_test_gbc))
print("classification report")
print(metrics.classification_report(y_test, y_test_gbc))

# pickle.dump(gb_clf, open('gbcmodel.pkl', 'wb'))
