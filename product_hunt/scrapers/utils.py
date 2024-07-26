from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

def sentiment_score(review):
    """_summary_ sentences_polarity( sentences, sentence_polarity):

    Args:       
        text (_type_): The text to be analyzed. 

    Returns:
        _type_: The polarity of the text in form of percentage.
    """
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(review)
    return score

def sentiment_label(score, **kwargs):
    if score['compound'] < -0.7:
        return "Critical"
    elif score['compound'] < -0.5 and score['compound'] >= -0.7:
        return "Serious"
    elif score['compound'] < -0.3 and score['compound'] >= -0.5:
        return "Negative"
    elif score['compound'] == 0 and score['compound'] < 0.1:
        return "Balance"
    elif score['compound'] > 0.5:
        return "Positive"
    elif score['compound'] > 0.3 and score['compound'] <= 0.5:
        return "Slightly Positive"
    