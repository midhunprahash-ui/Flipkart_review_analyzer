import matplotlib.pyplot as plt
import pandas as pd 
df = pd.read_csv("Product_Review.csv")
# Plot sentiment distribution
df["Sentiment"].value_counts().plot(kind="bar", color=["green", "red", "blue"])
plt.title("Sentiment Distribution of Flipkart Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.show()