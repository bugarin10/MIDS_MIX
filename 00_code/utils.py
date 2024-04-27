import random
import pandas as pd
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import requests


load_dotenv()


def return_image(base=None, random_retrieve=True):
    """This function returns the url of the image
    using a random selection or using the closest image


    Args:
        base_liquor (str): base liquour among 20 different
        random (bool, optional): Is the return random or not. Defaults to True.
    """
    url_drinks = {
        "tequila": "https://www.lanaval.com.mx/115615-product_default/tequila-don-julio-70-700-ml.jpg",
        "whiskey": "https://bouquetdebarrica.com/cdn/shop/products/WoodfordReserveMain.jpg?v=1659570654",
        "beer": "https://cocktail-recommendations.s3.amazonaws.com/cocktail-pictures/Hi-WireBrewery/MountainWater.jpg",
        "vodka": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSg9YSJgWS8UFXkJlmnWkBx5c9Ynx4MjhRP4k7WqFun7A&s",
    }

    if random_retrieve:
        random_keys = random.sample(list(url_drinks.keys()), 3)
        random_values = [url_drinks[key] for key in random_keys]
        return random_values

    else:
        # Using lambda to retrieve the info.
        return None


def retrieve_random_coktails():
    """retrieve the first three random vectors

    Returns:
        dictionary: returns three IDs with their relevant information
    """
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index = pc.Index("midsmix")

    three_ids = random.sample(range(1, 604), 3)

    three_ids = ["ID" + str(i) for i in three_ids]

    result = index.fetch(ids=three_ids)

    return result["vectors"]


def closest_vector(id):

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index = pc.Index("midsmix")

    id_to_compare = index.fetch(ids=[id])

    result = id_to_compare["vectors"]

    values = id_to_compare["vectors"][id]["values"]

    closest_vectors = index.query(
        vector=values,
        top_k=3,
        include_metadata=True,
    )

    IDs = [i["id"] for i in closest_vectors["matches"]]

    result = {IDs[i]: closest_vectors["matches"][i] for i in range(3)}

    return result
