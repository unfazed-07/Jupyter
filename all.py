# E-Commerce Product analysis
#Store Product Prices 
#Apply 10% discount on each product price using numpy
#create a dataframe 
#plot a price comparison graph(Product  and discounted price bar graph)
#plot a line graph of original price vs discounted price
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

products = ["Laptop", "Smartphone", "Headphones", "Smartwatch"]
prices = np.array([1000, 500, 150, 200])
discounted_prices = prices * 0.9 
df = pd.DataFrame({
    "Product": products,
    "Original Price": prices,
    "Discounted Price": discounted_prices
})
print(df)
plt.plot(df["Product"], df["Original Price"],marker = "o")
plt.plot(df["Product"], df["Discounted Price"],marker = "o")
plt.title("Price comparisons")
plt.xlabel("Product")
plt.ylabel("Price")
plt.show()
