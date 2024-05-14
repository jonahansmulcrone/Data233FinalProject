from models import mod
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

n = mod()

reviews_data = n.getSEn()
stars = [data['stars'] for data in reviews_data]
labels = [data["Quality"] for data in reviews_data]
seas = [data["season"] for data in reviews_data]
#print(labels)



# Sentiment Analysis Results
# Assuming you have sentiment_scores for each review

# Histogram of sentiment scores
plt.hist(labels, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.title('Distribution of Sentiment Scores')
plt.show()

# Rating Distributions of Yelp Reviews
# Assuming you have star ratings for each review

# Histogram of star ratings
sns.histplot(stars, bins=5, kde=False, color='orange')
plt.xlabel('Star Rating')
plt.ylabel('Frequency')
plt.title('Distribution of Star Ratings')
plt.show()

# Relationship Between Weather Conditions and Restaurant Recommendations
# Assuming you have weather data and number of restaurant recommendations

# Scatter plot of temperature vs. recommendations
from sklearn.preprocessing import LabelEncoder

# Encode the "seas" variable
label_encoder = LabelEncoder()
encoded_seas = label_encoder.fit_transform(seas)

correlation = np.corrcoef(labels, stars)[0, 1]

# Plot a scatter plot with correlation coefficient
sns.regplot(x=stars, y=labels, scatter_kws={'alpha':0.5})
plt.ylabel('Sentence Quality')
plt.xlabel('Star Rating')
plt.title('Relationship Between Season and Star Ratings (Correlation: {:.2f})'.format(correlation))
plt.show()

sns.regplot(x=encoded_seas, y=labels, scatter_kws={'alpha':0.5})
plt.xlabel('Seasons')
plt.ylabel('Sentence Quality')
plt.title('Relationship Between Season and Star Ratings')
plt.xticks(ticks=range(len(label_encoder.classes_)), labels=label_encoder.classes_, rotation=45)
plt.show()

