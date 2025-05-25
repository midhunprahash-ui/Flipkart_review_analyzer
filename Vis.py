import matplotlib.pyplot as plt
import pandas as pd 
df = pd.read_csv("Product_Review.csv")
# Plot sentiment distribution
df["Sentiment"].value_counts().plot(kind="bar", color=["green", "red", "blue"])
plt.title("Sentiment Distribution of Flipkart Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.show()
plt.savefig("sentiment_distribution.png")
# Plot sentiment distribution
# Plot sentiment distribution
df["Sentiment"].value_counts().plot(kind="pie", autopct='%1.1f%%', startangle=90, colors=["green", "red", "blue"])
plt.title("Sentiment Distribution of Flipkart Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.show()
plt.savefig("sentiment_distribution_pie.png")

