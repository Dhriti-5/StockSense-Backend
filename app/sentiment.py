import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from .data import recent_news

# Ensure VADER is available (first run will download)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

SENT_THRESH = 0.15

def news_sentiment(symbol: str):
    items = []
    for itm in recent_news(symbol)[:20]:
        title = itm.get('title') or ''
        link = itm.get('link') or ''
        publisher = itm.get('publisher') or 'Unknown'
        published = itm.get('providerPublishTime')
        score = sia.polarity_scores(title)["compound"]
        sentiment = 'neutral'
        if score >= SENT_THRESH:
            sentiment = 'positive'
        elif score <= -SENT_THRESH:
            sentiment = 'negative'
        items.append({
            'title': title,
            'publisher': publisher,
            'link': link,
            'published': str(published),
            'sentiment': sentiment,
            'score': float(score)
        })
    return items
