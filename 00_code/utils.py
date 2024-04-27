import random
import pandas as pd

url_drinks = {
    "tequila": "https://www.lanaval.com.mx/115615-product_default/tequila-don-julio-70-700-ml.jpg",
    "whiskey": "https://bouquetdebarrica.com/cdn/shop/products/WoodfordReserveMain.jpg?v=1659570654",
    "beer": "https://cocktail-recommendations.s3.amazonaws.com/cocktail-pictures/Hi-WireBrewery/MountainWater.jpg",
    "vodka": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSg9YSJgWS8UFXkJlmnWkBx5c9Ynx4MjhRP4k7WqFun7A&s",
}


def return_image(ingredients=None, random_retrieve=True):
    """This function returns the url of the image
    using a random selection or using the closest image


    Args:
        base_liquor (str): base liquour among 20 different
        random (bool, optional): Is the return random or not. Defaults to True.
    """

    if random_retrieve:
        return random.choice(url_drinks.values)
    else:
        # Using lambda to retrieve the info.
        return None


def retrieve_random_coktails():
    data = pd.read_csv("10_data/filtered_data.csv")
