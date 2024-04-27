![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Rust](https://img.shields.io/badge/rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white)
![FLASK](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)


### Demo video
<div align="left">
 
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://youtu.be/31c-DYnYhQ4)

</div>


 

# Mix and Cocktail recommendation Engine 🍷🍸🍹

# Motivation

Our moto is the impact we can make in alleviating choice overload. This phenomenon, characterized by the overwhelming stress and indecision caused by an abundance of options, is a challenge many face daily. By developing a recommendation engine, we aim to empower individuals with personalized suggestions, reducing the cognitive load associated with decision-making and increasing satisfaction with chosen options. Let's drink and think in the conversation not on what to drink!

# Project Structure

This is the broad structure of the project and how we visualize is going to be merging all projects:

![structure](static/images/structure.png)

## Personal Cocktail Recommendation Engine
The first half of this project was to create a home-brewed cocktail recommendation engine. The engine was built using a dataset of cocktail recipes and ingredients. Using Pinecone, we were able to create a vector representation of each cocktail recipe and use cosine similarity to recommend similar cocktails based on user input. 

## Hugging Face Cocktail Recommendation Engine
The second half of this project was to create a cocktail recommendation engine using Hugging Face's model hub. For the same, we used a pre-trained model from Hugging Face's model hub to generate cocktail recommendations based on user input, namely, google-flan-large. 

# Deployment

For this individual one the project was deployed on Azure because doing it on AWS has not being explored yet, the website was https://midsmix.azurewebsites.net/ but it will be up just for the demo.

![webapp](static/images/webapp.png)

