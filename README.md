# Flipkart Review Sentiment Analyzer and Visualizer
Ever wish you could quickly tell what people really think about a product before you buy it? Scrolling through tons of reviews is a pain, right? Well, I whipped up this little tool that uses sentiment analysis to figure out how folks feel! It's super handy for getting the general vibe.
This tool's pretty neat! It automatically grabs reviews from Flipkart, then dives into them to see if they're positive, negative, or just neutral. After that, it shows you a cool visual breakdown of all those sentiments. So, instead of reading every single review, you get a quick, clear picture of what the crowd thinks. Easy peasy!

# How to Get Started - *Ready to give it a whirl? Just follow these simple steps:*

## Grab What You Need:
First off, make sure you've got all the necessary Python libraries installed. Just pop open your terminal (or command prompt), head to your project folder, and type this:

`pip install -r requirements.txt`

## Update the Product Link:
Next, open up the python script `main.py` and find where it says `PRODUCT_URL_TEMPLATE`. You totally need to swap that out with the actual review page URL for the Flipkart product you want to check out.

## *Here's a quick example:*
Let's say your product's main URL looks like `https://www.flipkart.com/your-product-name/p/some-id?pid=SOMEID&lid=SOMLID`. You'll want the reviews page URL, which usually looks something like `https://www.flipkart.com/your-product-name/product-reviews/some-id?pid=SOMEID&lid=SOMLID&marketplace=FLIPKART&page={}`. Just make sure to change that `page=X` bit to `page={}`.

## Run It!
Once everything's set up with your dependencies and that product link, just run the script from your terminal like this:

`python main.py`

(Remember to use `main.py` if that's what you called your file).

## Then, watch it go! The script will:

- Grab all those reviews from the Flipkart product page you picked.

- Figure out the sentiment (positive, negative, or neutral) for each one.

- Save all the reviews and their sentiments into a handy CSV file called Product_Review_with_Sentiment.csv.

- Pop up two cool charts (and save them as .png files too!): a bar chart and a pie chart, both showing you the sentiment breakdown. Pretty neat, huh?

## Just a Heads-Up!
Right now, this project works best and is really designed for mobile phone review pages on Flipkart. The way it finds things on the page is specifically set up for those.

## What's Next?
Good news! I'm planning to make a more general version soon. That one will be able to handle all sorts of product categories and page layouts on Flipkart (and maybe even other shopping sites!). So, it'll be even more flexible!
