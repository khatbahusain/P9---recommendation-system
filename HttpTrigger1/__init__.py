import logging
import azure.functions as func
import pickle
import pandas as pd
import random

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


clicks_df = pd.read_csv('clicks_df.csv')

def get_top_n_articles_for_user(user_id, n=5):
    
    user_id = int(user_id)
    
    articles = clicks_df['click_article_id'].unique()
    # Get list of articles that the user has already clicked on
    articles_read = clicks_df.loc[clicks_df['user_id'] == user_id, 'click_article_id'].tolist()

    # Remove articles that the user has already read from the articles index
    articles_to_recommend = [article for article in articles if article not in articles_read]
        
    # Use collaborative filtering to predict user ratings for remaining articles
    user_ratings = model.test([(user_id, article_id, 0) for article_id in articles_to_recommend], verbose=False)
    
    results = {rating.iid: rating.est for rating in user_ratings}

    # Sort the results dictionary by value in descending order
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    #random_items = random.sample(articles_to_recommend, 5)
    # Return the top n articles with the highest predicted ratings
    return user_id,[sorted_results[i][0] for i in range(min(n, len(sorted_results)))]




def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('user_id')

    if user_id:
        
        result = get_top_n_articles_for_user(user_id, n=5)
        return func.HttpResponse(str(result))
    
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass an id in the query string or in the request body for a personalized response.",
             status_code=200
        )
