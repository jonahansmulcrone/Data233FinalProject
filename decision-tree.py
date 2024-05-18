import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import json
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

df = pd.read_json('yelp_dataset/reviews_with_season.json')

# Data Preparation
df = pd.get_dummies(df, columns=['season', 'city'])
X = df.drop(columns=['category', 'text', 'review_id', 'user_id', 'business_id', 'date', 'state', 'funny', 'cool', 'useful'])  # Drop non-numeric columns
y = df['category']

# Training the Model
clf = DecisionTreeClassifier()
clf.fit(X, y)

# Create user input DataFrame
user_input = pd.DataFrame({
    'city_' + 'Tampa': [1],
    'season_Winter': [1]
})

user_input2 = pd.DataFrame({
    'city_' + 'Reno': [1],
    'season_Winter': [1]
})

user_input = user_input.reindex(columns=X.columns, fill_value=0)

# Make predictiona
predicted_category = clf.predict(user_input)
print("Predicted category:", predicted_category[0])

feature_importance = clf.feature_importances_
feature_names = X.columns

# Sort feature importances in descending order
indices = feature_importance.argsort()[::-1][:20]  # Selecting top 20 most important features

# Plot the feature importances of the decision tree
plt.figure(figsize=(10, 6))
plt.title("Top 20 Feature Importance")
plt.bar(range(len(indices)), feature_importance[indices], align="center")
plt.xticks(range(len(indices)), feature_names[indices], rotation=90)
plt.xlabel("Features")
plt.ylabel("Importance")
plt.show()

# Visualizing the Decision Tree
plt.figure(figsize=(20, 10))
plot_tree(clf, filled=True, feature_names=X.columns, class_names=clf.classes_, max_depth=3)
plt.show()