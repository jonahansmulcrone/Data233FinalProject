import requests
import pandas as pd
import json
from datetime import datetime
from Sentence_quality import sentenceQuality

business_url = "https://api.yelp.com/v3/businesses/search?location=Seattle&limit=20"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer wxUp4LTf7UM8ofjG2H1lZ7kSmi3n_PkASO6-8ON1lpsmT9yqKjbmFXApXcfXpjn_K5Zj_rpYKjGWGihGz70xkIRWerJoaIeGqrxLnE6tbpKZpQfl_fb0KtVVs2wwZnYx"
}

#gloss over, not using yelp fusion api:
response = {
    "status_code": 400
}

if response.get("status_code", 200) == 200: 

    data = response.json()
    businesses = data.get('businesses')

    reviews = []

    for business in businesses:

        business_id = business['id']

        review_url = f"https://api.yelp.com/v3/businesses/" + business_id + "/reviews?limit=1&sort_by=yelp_sort"
        response = requests.get(review_url, headers=headers)

        print(response.json())

        current_review = {
            "business_name": business['name'],
            "city": business['location']['city'],
            "category": business['categories'][0]['title']
        }

        reviews.append(current_review)


"""

input_file_path = "yelp_dataset/yelp_academic_dataset_review.json"
output_file_path = "reduced_reviews.json"


with open(input_file_path, "r") as input_file:

    with open(output_file_path, "w") as output_file:

        for i in range(550):
            line = input_file.readline().strip()
            if line: 
                output_file.write(line + '\n')

with open(output_file_path, "r") as output_file:
    first_100_reviews = [json.loads(line) for line in output_file]

with open(output_file_path, "w") as output_file:
    json.dump(first_100_reviews, output_file, indent=2)

"""


"""
business_data = {}
with open("yelp_dataset/yelp_academic_dataset_business.json", "r", encoding="utf-8") as business_file:
    for line in business_file:
        business = json.loads(line)
        business_data[business["business_id"]] = business

first_business_id = next(iter(business_data.keys()))
print(first_business_id)

first_business = next(iter(business_data.values()))
print(first_business)
"""

"""

with open("yelp_dataset/reduced_reviews.json", "r", encoding="utf-8") as reviews_file:
    reduced_reviews = json.load(reviews_file)


reviews_with_state_and_category = []
for review in reduced_reviews:
    business_id = review.get("business_id")
    if business_id:
        
        business = business_data.get(business_id)
        if business:
            
            review["state"] = business.get("state")
            review["category"] = business.get("categories", "").split(", ")[0]
            review["city"] = business.get("city")
        else:
            print(f"No business found for ID: {business_id}")
    reviews_with_state_and_category.append(review)


with open("reviews_join_business", "w", encoding="utf-8") as output_file:
    json.dump(reviews_with_state_and_category, output_file, indent=2)

"""

#Encode Dates as Seasons

def get_season(date_str):
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    
    # Determine the season based on the month
    month = date_obj.month
    if 3 <= month <= 5:
        return "Spring"
    elif 6 <= month <= 8:
        return "Summer"
    elif 9 <= month <= 11:
        return "Autumn"
    else:
        return "Winter"

# Read the JSON file
with open("yelp_dataset/reviews_join_business.json", "r", encoding="utf-8") as input_file:
    reviews_data = json.load(input_file)

# Filter objects with seasons
reviews_with_season = []
for review in reviews_data:
    if "date" in review:
        qualt = sentenceQuality()
        review["season"] = get_season(review["date"])
        review["Quality"] = qualt.calculateQuality(qualt.calculateScores(review["text"]))
        reviews_with_season.append(review)

# Save objects with seasons into a new file
with open("reviews_with_season.json", "w", encoding="utf-8") as output_file:
    json.dump(reviews_with_season, output_file, indent=2)