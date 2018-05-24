# used to pick a random entry and to chose between 3 or 4 hours between tweets
import random
# manipulates de database where firefox url history is stored
import sqlite3
import operator
# to manipulate unix time stored in the database
import time
# to parse the url and replace escaped characteres with regular ones
import urllib
# twitter API
import tweepy

# import private keys and tokens for twitter API
from secrets import consumer_key, consumer_secret, access_token, access_secret

# gives us a list of tuples with all relevant wikipedia.org URL and the
# time (unix time) of last access, read from the browser (firefox in this case)
# database file that contains access history.
def get_all_wiki_accesses():
    history_db = r"C:\Users\Caio Marcos\AppData\Roaming\Mozilla\Firefox\Profiles\juo9u3z2.default\places.sqlite"
    c = sqlite3.connect(history_db)
    cursor = c.cursor()
    select_statement = "SELECT moz_places.url, moz_places.last_visit_date FROM moz_places WHERE url LIKE '%wikipedia.org/wiki%' AND url NOT LIKE '%File:%' AND url NOT LIKE '%#%' AND url NOT LIKE '%disambiguation%' AND url NOT LIKE '%Special:%' AND url NOT LIKE '%Template:%';"
    cursor.execute(select_statement)
    return cursor.fetchall()

# picks one tuple from the list
def pick_random_wiki_access(list_of_url_date, random_number):
    return list_of_url_date[random_number]

# returns the 'name of article' part of the url, replacing underscore with
# spaces, so if the full url is "https://en.wikipedia.org/wiki/Chua%27s_circuit"
# we get "Chua%27s circuit"
def get_picked_wiki_article(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/')
		article = sublevel_split[2].replace("_", " ")
		return article
	except IndexError:
		print("URL format error!")

# returns the date associated to the url above in day/month/year format
def get_picked_wiki_date(unix_time):
    return time.strftime("%d/%m/%Y", time.gmtime(unix_time/1000000))

# brings everything together, while replacing escaped chars with
# regular ones. So if the article is "Chua%27s_circuit" we get "Chua's circuit"
# "Eu li sobre [ARTICLE] no dia [DATE] - [FULL WIKIPEDIA URL LINKING TO ARTICLE]"
def build_tweet(article, date, url):
    unquote_article = urllib.parse.unquote(article)
    return "Eu li sobre %s no dia %s - %s" % (unquote_article, date, url)

##################### Infinite loop, tweeting every 3-4h #######################
while True:
    # reads the db every time so it can get new entries that were added since
    # the script started to run
    wiki_accesses = get_all_wiki_accesses()
    size = len(wiki_accesses)
    print("total wikipedia entries is %s" % size)

    # generates a random number from 0 to the number of wikipedia entries. If
    # there was already a tweet related to that entry, it gets another number.
    # unless the SELECT statement changes, this ensures non-repeted tweets.
    valid = 0
    while valid == 0:
        picked_number = random.randint(0, size)
        print("picked entry is %s" % picked_number)
        if str(picked_number) in open('tweets.txt').read():
            valid = 0
            print("entry already tweeted about, picking another one.")
        else:
            print("entry never tweeted about, proceeding...")
            valid = 1

    picked_access = pick_random_wiki_access(wiki_accesses, picked_number)
    article = get_picked_wiki_article(picked_access[0])
    date = get_picked_wiki_date(picked_access[1])

    tweet = build_tweet(article, date, picked_access[0])

    # create an OAuthHandler instance
    # Twitter requires all requests to use OAuth for authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_secret)

    # Construct the API instance
    api = tweepy.API(auth) # create an API object

    # tries to tweet. if successful, saves the entry tweeted about so it does
    # not tweet about it again.
    try:
        if api.update_status(tweet):
            print("Posted")
            print(tweet)
            f = open('tweets.txt', 'a')
            f.write(str(picked_number) + '\n')
    except tweepy.error.TweepError as e:
        print(e)

    # wait for 3 or 4 hours until next tweet, so we have 6 to 8 tweets a day
    time_to_wait = random.choice([3, 4])
    print("waiting for %s hours until next tweet" % time_to_wait)
    time.sleep(60*60*time_to_wait)
