import random
import pandas as pd
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import requests


load_dotenv()


def return_image(bases=None, random_retrieve=False):
    """This function returns the url of the image
    using a random selection or using the closest image


    Args:
        bases (list): List of base liquour among 20 different types
        random (bool, optional): Is the return random or not. Defaults to True.
    """
    bases = [base.replace(' ', '_').lower() for base in bases]
    base_url = "https://cocktail-recommendations.s3.us-east-2.amazonaws.com/spirits-pictures/"
    random_image = "https://cocktail-recommendations.s3.us-east-2.amazonaws.com/spirits-pictures/random.jpg"
    all_images = []

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
        for base in bases:
            image_url = base_url + base + ".jpg"
            if is_url_valid(image_url):
                print("URL is valid.")
                all_images.append(image_url)
            else:
                print("URL is not valid. Switching to default backup.")
                all_images.append(random_image)
                
        return  all_images


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

def is_url_valid(url):
    response = requests.head(url)
    return response.status_code == 200