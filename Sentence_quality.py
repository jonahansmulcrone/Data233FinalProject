from textblob import TextBlob

class sentenceQuality():
    def __init__(self):
        # do some initialization, optional
        pass

    def count_letters_and_numbers(input_string):
        count = 0
        for char in input_string:
            if char.isalnum():
                count += 1
        return count

    def calculateScores(self, tweet):
        # please implement this function
        # input: any tweet text
        # output: a list of scores for the tweet, it must include: score for length, score for Polarity, score for Subjectivity, and at least one score of the following:
        # https://en.wikipedia.org/wiki/Automated_readability_index
        # https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
        # https://en.wikipedia.org/wiki/Gunning_fog_index
        # https://en.wikipedia.org/wiki/SMOG
        # https://en.wikipedia.org/wiki/Fry_readability_formula
        # https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
        # You should implement at least one score

        texts = TextBlob(tweet)

        subj = texts.sentiment.subjectivity
        polar = texts.sentiment.polarity

        charater = float(sentenceQuality.count_letters_and_numbers(tweet))
        words = float(len(texts.words))
        num_sentens = len(texts.sentences)
        automated = float(4.71*(charater/words) + 0.5*(words/num_sentens) - 21.73)


        if automated > 1:
            automated = 1

        x = len(tweet)/100
        if x > 1.0:
            x = 1.0;

        obj = TwitterPositive()
        y = obj.evaluateTweet(tweet)

        if y < 0.5:
            y = 0

        return [x, polar, subj, automated]
        pass

    def calculateQuality(self, scores):
        # please implement this function to calculate a final quality score between 0 and 1
        # Input: a list of scores, which is the output of calculateScores
        # output: 0 means low quality, 1 mean high quality

        if scores[1] == 0.0 or scores[2] == 0.0:
            return 0


        ans = (sum(scores)/len(scores))

        return ans


import re


def countWor(lis):
    word_counts = {}
    sum = 0
    # Iterate over each string in the list
    for string in lis:
        # Split the string into words
        words = string.split()
        # Iterate over each word in the list
        for word in words:
            # Update the count for the word in the dictionary
            word_counts[word] = word_counts.get(word, 0) + 1

    # Print the word counts
    for word, count in word_counts.items():
        if count > 2:
            sum = sum + count
    return sum


class TwitterPositive():
    def __init__(self):
        # do some initialization, optional
        pass

    def evaluateTweet(self, tweet):
        # please implement this function
        # input: any tweet text
        # output: a score [0,1], 0 means it is low quality and negative, 1 means it is high quality and positive

        positive_words = [
            'good', 'excellent', 'great', 'awesome', 'fantastic',
            'amazing', 'wonderful', 'superb', 'brilliant', 'outstanding',
            'terrific', 'fabulous', 'incredible', 'perfect', 'marvelous',
            'delightful', 'splendid', 'phenomenal', 'exceptional', 'stellar',
            'remarkable', 'extraordinary', 'top-notch', 'first-rate', 'superior',
            'impressive', 'magnificent', 'glorious', 'sublime', 'majestic',
            'divine', 'exemplary', 'praiseworthy', 'admirable', 'commendable',
            'heartwarming', 'joyful', 'uplifting', 'inspiring', 'positive',
            'optimistic', 'ecstatic', 'blissful', 'euphoric', 'thrilling',
            'sensational', 'electrifying', 'captivating', 'enchanting', 'charming',
            'enticing', 'alluring', 'engaging', 'invigorating', 'refreshing',
            'energizing', 'stimulating', 'vibrant', 'dynamic', 'alive', 'radiant',
            'cheerful', 'lively', 'vivacious', 'buoyant', 'spirited', 'exhilarating',
            'festive', 'celebratory', 'jubilant', 'festive', 'gleeful', 'playful',
            'delicious', 'scrumptious', 'mouthwatering', 'tasty', 'flavorful',
            'satisfying', 'fulfilling', 'gratifying', 'nourishing', 'wholesome',
            'beneficial', 'heavenly', 'divine', 'sumptuous', 'lavish', 'opulent',
            'luxurious', 'gorgeous', 'beautiful', 'stunning', 'breathtaking',
            'mesmerizing', 'enchanting', 'fascinating', 'captivating', 'hypnotic',
            'bewitching', 'enticing', 'spellbinding', 'charismatic', 'alluring', 'wonderful'
        ]

        negative_words = [
            'bad', 'poor', 'terrible', 'horrible', 'awful',
            'mediocre', 'subpar', 'inferior', 'unsatisfactory', 'disappointing',
            'unpleasant', 'unfavorable', 'negative', 'dreadful', 'lousy',
            'abysmal', 'atrocious', 'ghastly', 'miserable', 'wretched',
            'deplorable', 'appalling', 'disgusting', 'repulsive', 'revolting',
            'offensive', 'vile', 'disgraceful', 'shameful', 'abominable',
            'detestable', 'horrifying', 'repugnant', 'odious', 'noxious',
            'repellent', 'unsavory', 'distasteful', 'unwelcome', 'unwanted',
            'disheartening', 'discouraging', 'demoralizing', 'depressing', 'gloomy',
            'melancholy', 'dreary', 'sorrowful', 'mournful', 'bleak',
            'despondent', 'dismal', 'grievous', 'tragic', 'pitiful',
            'heartbreaking', 'heart-wrenching', 'saddening', 'tearful', 'unfortunate',
            'unlucky', 'troublesome', 'problematic', 'difficult', 'challenging',
            'frustrating', 'annoying', 'irritating', 'exasperating', 'aggravating',
            'bothersome', 'disruptive', 'displeasing', 'discontented', 'disgruntled',
            'grumpy', 'miserable', 'crummy', 'irksome', 'pesty', 'vexing',
            'maddening', 'provoking', 'enraging', 'infuriating', 'outrageous',
            'intolerable', 'unbearable', 'exasperating', 'anger-inducing', 'irksome',
            'troublesome', 'annoying', 'bothersome', 'irritating', 'frustrating',
            'aggravating', 'infuriating', 'vexing', 'maddening', 'galling',
            'exasperating', 'peeving', 'perturbing', 'trying', 'nagging'
        ]

        delimiters = "[,;|\\s]+"

        words = re.split(delimiters, tweet)

        two_gram = TwitterPositive.twoGram(words)

        num_positive_words = sum(4 for word in tweet.split() if word.lower() in positive_words)
        num_negative_words = sum(1 for word in tweet.split() if word.lower() in negative_words)
        # print(num_positive_words)
        # print(num_negative_words)

        total_words = len(tweet.split())
        # print(total_words)
        if total_words == 0:
            return 0.0
        else:
            positive_ratio = num_positive_words / total_words

        occu = countWor(two_gram)

        # print(occu)

        score = positive_ratio - ((occu + num_negative_words) / total_words)

        score = max(0, min(score, 1))

        # print(two_gram)

        return score

    def twoGram(lis):

        result = []

        for i in range(len(lis)):
            if i == len(lis) - 1:
                break
            else:
                result.append(lis[i] + " " + lis[i + 1])

        return result
