<<<<<<< HEAD
import requests, json
=======
import re
import string
from nltk.tag.stanford import POSTagger

tagger = POSTagger('./stanford-postagger-full-2014-10-26/models/german-fast.tagger',
                   './stanford-postagger-full-2014-10-26/stanford-postagger-3.5.0.jar',
                    'UTF-8')

punctuation_regex = re.compile("[%s]" % re.escape(string.punctuation))

def get_potential_places(article_place, article_body):
    """
    Returns a list of potential places as tuples with their part-of-speech tags
    for later filtering
    """
    place_pos = tagger.tag(punctuation_regex.sub(" ", article_place).split())
    text_pos = tagger.tag(punctuation_regex.sub(" ", article_body).split())

    # extract the places out of the full text
    places = [place_pos]
    is_matching = False
    current_match = []
    for tuple in text_pos:
        if is_matching:
            # when we're matching, the phrases we're looking for look like
            # "Im S-Bahnhof Wedding"... the tags below mean
            if tuple[1] in ("ART", "ADJA", "NN", "NE", "CARD"):
                current_match.append(tuple)
            else:
                # we stop the match, so append the current match
                places.append(current_match)
                current_match = []

                # whe we're looking at a preposition again, just start new match
                if tuple[1] not in ("APPR", "APPRART"):
                    is_matching = False
        else:
            # start matching when we have a preposition
            if tuple[1] in ("APPR", "APPRART"):
                is_matching = True

    return places

def improve_potential_places(pos_tuples):
    """
    Improves the matches' quality so we don't have to look up the lat-lng of so
    many mismatches
    """
    better_tuples = []
    for tuple_list in pos_tuples:
        # first, exluce empty lists
        if tuple_list:
            cleaner_list = []

            index = -1
            for tuple in tuple_list:
                index += 1

                # exclude articles ("the", "a"), they only introduce noise, but
                # keep the list as a whole
                if tuple[1] == "ART":
                    continue

                # if we have numbers in the middle of our phrase, probably the
                # whole list is not useful (as opposed to e.g. Krügerstr. 22)
                if tuple[1] == "CARD" and index < len(tuple_list):
                    cleaner_list = []
                    break

                cleaner_list.append(tuple)

            if cleaner_list:
                better_tuples.append(cleaner_list)

    return better_tuples
>>>>>>> place_extraction

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
