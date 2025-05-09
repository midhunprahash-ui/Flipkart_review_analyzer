import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

df = pd.read_csv("Product_Review.csv")

nltk.download("vader_lexicon")
nltk.download("stopwords")

sia = SentimentIntensityAnalyzer()

stop_words = set(stopwords.words("english"))


def clean_review(text):
   
    text = text.lower()

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    text = " ".join(word for word in text.split() if word not in stop_words)
    return text


df["Cleaned_Review"] = df["Review"].apply(clean_review)

def get_sentiment(text):
    score = sia.polarity_scores(text)
    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Cleaned_Review"].apply(get_sentiment)


df["Sentiment"].value_counts().plot(kind="pie", color=["green", "red", "blue"])
plt.title("Customer Reviews for Realme XT")
plt.xlabel("")
plt.ylabel("Number of Reviews")
plt.show()


df.to_csv("Product_Review_Sentiment.csv", index=False)
print("Sentiment analysis results saved to 'Product_Review_Sentiment.csv'")