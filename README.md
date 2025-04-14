# Customized User-interactive Movie Query and Recommendation System

## Overview
In today’s era of abundant entertainment options, choosing the right movie can be overwhelming. This project aims to simplify that process by providing a user-interactive system that combines powerful search and recommendation functionalities. Leveraging techniques from machine learning and information retrieval, our system offers personalized movie recommendations and tailored search results—all in one intuitive application.

## Key Features
- **User-Interactive Login:**  
  Quickly identify registered users using their unique userID. Upon login, users receive a personalized greeting and access to customized functionalities.

- **Movie Query/Search Functionality:**  
  Search for movies by entering keywords related to movie genres, comment tags, and ratings. The system utilizes Apache Solr to perform efficient, semantic searches and retrieve a maximum of 20 relevant results per query.

- **Personalized Recommendation System:**  
  Built on Singular Value Decomposition (SVD) from Python’s Surprise library, the recommendation engine analyzes a user’s viewing history to predict ratings for unseen movies. This enables the generation of a personalized recommendation list tailored to each user’s preferences.

- **Customized Want List:**  
  Users can curate their own “want list” by selecting movies from either the search results or recommendation list. This list can be saved and later exported to a CSV file for easy access and planning.

## Underlying Technologies
- **Machine Learning with SVD:**  
  We apply SVD-based collaborative filtering to factorize the user-item matrix, extracting latent features that enhance prediction accuracy and reduce noise.

- **Data Crawling and Web Scraping:**  
  The application collects movie reviews by scraping the IMDB website using the Requests and BeautifulSoup libraries. To significantly speed up the process, multiprocessing techniques are employed.

- **Apache Solr Integration:**  
  Utilizing the pysolr package, our system interfaces with Apache Solr to index and search movie data. Solr’s faceting, grouping, and semantic similarity features allow for fine-tuned, efficient searches.

- **MovieLens 25M Dataset:**  
  Our project is built upon the extensive MovieLens 25M dataset, which includes over 25 million ratings and more than 1 million tag applications across 62,423 movies. This robust dataset serves as the foundation for accurate movie recommendations and search results.

- **Graphical User Interface:**  
  A user-friendly interface is built with tkinter, offering an intuitive way for users to interact with the movie list, search functionalities, and recommendation outputs.

## Project Architecture & Workflow
1. **User Login:**  
   Verify registered users via userID and initiate the session with a personalized greeting.

2. **Movie Query Module:**  
   - Users can input search criteria (e.g., movie genres, tags, ratings).  
   - The system interacts with Solr to retrieve matching movie records, applying an "AND" operation when multiple fields are used.

3. **Recommendation Module:**  
   - The SVD model processes the user's historical ratings data.  
   - The engine predicts ratings for unseen movies and presents a top-ranked personalized recommendation list.

4. **Want List Feature:**  
   - Users can easily select and save movies from both search and recommendation outputs.  
   - The curated movie list can be exported as a CSV file for future reference.

## Getting Started
### Prerequisites
- **Python 3.x**  
- **Required Libraries:**  
  - `requests`
  - `BeautifulSoup`
  - `pysolr`
  - `scikit-surprise` (for SVD implementation)
  - `tkinter` (for the GUI)
- **Apache Solr:** Installed and configured to host a core for movie data.
- **MovieLens 25M Dataset:** Download and prepare the dataset as described in the documentation.
