import requests

business_url = "https://api.yelp.com/v3/businesses/search?location=Seattle&limit=20"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer wxUp4LTf7UM8ofjG2H1lZ7kSmi3n_PkASO6-8ON1lpsmT9yqKjbmFXApXcfXpjn_K5Zj_rpYKjGWGihGz70xkIRWerJoaIeGqrxLnE6tbpKZpQfl_fb0KtVVs2wwZnYx"
}

response = requests.get(business_url, headers=headers)

if response.status_code == 200:

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

    
    print(reviews)


