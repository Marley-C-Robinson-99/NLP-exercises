import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import os

def get_blog_articles(rerun = False):
    '''
    This function uses a list of urls for Codeup blog articles. Iterates through and wraps all pulled 
    info in a dictionary caching the reuslts. If rerun flag is True, grabs articles again instead of relying on cache.
    '''
    
    filename = 'blog_posts.csv'

    # Check for filename presence
    if os.path.isfile(filename) and rerun == False:
        return pd.read_csv(filename)
    else:
        # If not present grabs URLs
        urls = ['https://codeup.com/data-science/codeups-data-science-career-accelerator-is-here/',
                'https://codeup.com/data-science/data-science-myths/',
                'https://codeup.com/data-science/data-science-vs-data-analytics-whats-the-difference/',
                'https://codeup.com/data-science/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
                'https://codeup.com/data-science/competitor-bootcamps-are-closing-is-the-model-in-danger/'
            ]

        # Init the empty list to append the article dicts to
        arts = []
        
        for url in urls:
            response = get(url, headers = {'user-agent':'Codeup DS Germain'})
            soup = BeautifulSoup(response.content, 'html.parser')
            art = {'title': soup.find('h1', class_ = 'entry-title').text, 
                'pub_date': soup.find('span', class_ = 'published').text,
                'cat': soup.find('a', rel = 'category tag').text, 
                'content': soup.find('div', class_ = 'et_pb_post_content').text.strip().replace('\n', ' ').replace('\xa0', ' ')}
            arts.append(art)
        articles = pd.DataFrame(arts)
        # Pass to local CSV
        articles.to_csv(filename, index = False)
    
        return articles

def get_page_data(category):
    '''
    This function takes in the category, creates the amalgamated URL, passes data to dict.
    Returns list of dicts.
    '''
    # Create the url
    url = 'https://inshorts.com/en/read/' + category
    
    # Grab HTML from created url
    response = get(url, headers = {'user-agent':'Codeup DS Germain'})
    soup = BeautifulSoup(response.content, 'html.parser') # Soup it up
    
    # Get card-stack for news
    news = soup.find('div', class_ = 'card-stack')
    
    # Find all news_cards in news for articles
    articles = news.find_all('div', class_ = 'news-card')
    
    # Init empty list for dicts
    article_dicts = []
    
    #Loop through each article and gather the info
    for article in articles:
        article_dict = {
            'title': article.find('span', itemprop = 'headline').text,
            'author': article.find('span', class_ = 'author').text,
            'date': article.find('span', clas = 'date').text.split(',')[0],
            'cat': category,
            'content': article.find('div', itemprop = 'articleBody').text
        }
        article_dicts.append(article_dict) # Send it to list of dicts
        
    return article_dicts

def get_news_articles(categories = ['business', 'sports', 'technology', 'entertainment'], refresh = False):
    '''
    This function takes in the category, creates list of dicts iteratively.
    Caches data and pulls cached data in future uses unless refresh flag is True 
    in which case it treats the cache as nonexistent
    '''

    filename = 'news_articles.csv'

    # Checks for cached files and refresh flag
    if os.path.isfile(filename) and refresh == False:
        return pd.read_csv(filename)
    else:
        # Init empty list of dicts
        article_info = []
        
        # iterate through categories
        for cat in categories:
            article_list = get_page_data(cat)
            
            # appends article to article list
            for article in article_list:
                article_info.append(article)

        # Wrap in df and pass to csv locally
        article_info = pd.DataFrame(article_info)
        article_info.to_csv(filename, index = False)
        
        return article_info