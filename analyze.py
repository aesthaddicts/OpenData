import requests, json

def get_district(article_headline):
    """
    Returns a geo-coded version of a district an article is about, based on its
    headline.
    """
    pass

def get_categories(article_body):
    """
    Gives a list of categories an article falls into, which is empty if none of
    the following are matched:
    - sexism
    - antisemitism
    - homophobia
    - racism
    """
    bad_words = {
        'antisemit': 'antisemitism',
        'homophob': 'homophobia',
        'sexis': 'sexism',
        'rassis': 'racism'
    }
    found_categories = [bad_words[key] for key in bad_words
                                        if key in article_body.lower()]
    return found_categories or ['other']

def get_geoloc(query):
    query.replace(" ", "%20")
    url = "http://nominatim.openstreetmap.org/search?q=" + query + "%20Berlin" + "&countrycodes=de&format=json&limit=1"
    r = requests.get(url)

    return(r.json()[0]["lat"], r.json()[0]["lon"])
