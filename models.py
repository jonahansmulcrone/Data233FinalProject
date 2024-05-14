from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import json
from Sentence_quality import sentenceQuality
from collections import Counter, defaultdict
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class KNNModel:
    def __init__(self):
        self.knn_model = KNeighborsClassifier(n_neighbors=3)

    def train(self, X_train, y_train):
        self.knn_model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.knn_model.predict(X_test)

with open("reviews_with_season.json", "r", encoding="utf-8") as input_file:
    reviews_data = json.load(input_file)


stars = [data['stars'] for data in reviews_data]
labels = [data["Quality"] for data in reviews_data]
seas = [data["season"] for data in reviews_data]
sentences = [data['text'] for data in reviews_data]
label_encoder = LabelEncoder()
encoded_categories = label_encoder.fit_transform(seas)
combined_labels = np.column_stack((labels, encoded_categories))

# Reshape the combined labels to a 2D array
labels_resh = np.array(combined_labels).reshape(-1, 2)
#labels_resh = np.array(labels).reshape(-1, 1)

#print(encoded_categories)
#print(seas)


X_train, X_test, y_train, y_test = train_test_split(labels_resh, stars, test_size=0.1, random_state=100)

# Initialize kNNsentenceQuality object
obj = KNNModel()
obj.train(X_train, y_train)

new_sentences = "Love this store!  Who doesn't!  The salad bar is fresh and they have all types of ethnic food to try.  N-JOY"
qualt = sentenceQuality()
predictions = obj.predict(X_test)

# Calculate accuracy by comparing predictions with actual labels
accuracy = np.mean(predictions == y_test)
print("Accuracy:", accuracy)
answer = qualt.calculateQuality(qualt.calculateScores(new_sentences))
prd = np.array([answer, 3]).reshape(1, 2)
quality = obj.predict(prd)
print("Predicted Quality KNN:", quality)





X_train, X_test, y_train, y_test = train_test_split(labels_resh, stars, test_size=0.3, random_state=100)
vectorizer = CountVectorizer()
#X_train_transformed = vectorizer.fit_transform(X_train)

# Initialize the decision tree classifier
decision_tree_model = DecisionTreeClassifier()

# Train the decision tree model
decision_tree_model.fit(X_train, y_train)

# Evaluate the model
#X_test_transformed = vectorizer.transform(X_test)
accuracy = decision_tree_model.score(X_test, y_test)
print("Accuracy:", accuracy)
prediction = decision_tree_model.predict(prd)
print("Predicted Quality using decision tree:", prediction)



X_train, X_test, y_train, y_test = train_test_split(combined_labels, stars, test_size=0.2, random_state=42)

# Initialize the linear regression model
linear_reg_model = LinearRegression()

# Train the model
linear_reg_model.fit(X_train, y_train)

# Make predictions
y_pred = linear_reg_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)

print("Mean Squared Error:", mse)
print("Linear regssion", np.round(linear_reg_model.predict(prd)))


class mod:
    def __init__(self):
        self.reviews_data = reviews_data
    def getSEn(self):
        return reviews_data


