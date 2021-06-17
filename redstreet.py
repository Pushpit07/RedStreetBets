from keys import CLIENT_ID, SECRET_TOKEN, USERNAME, PASSWORD
from collections import Counter
import praw
import csv
import sys

# Default number of comments to lookup
no_of_comments = 50
# Number of comments to lookup as specified as the command line argument
try:
    no_of_comments = int(sys.argv[1])
except:
    pass

# Connect to Reddit API
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET_TOKEN, user_agent='RedStreetBets', username=USERNAME, password=PASSWORD)

#################################################
#  START: Get the number of specified comments  #
#################################################

subreddit = reddit.subreddit('wallstreetbets')

print('Fetching comments...')
top_subreddit = subreddit.new(limit=no_of_comments)

words_collection = []

print('Fragmenting comments into separate words...')
for submission in top_subreddit:
    title = submission.title
    title_words = title.split()
    words_collection.append(title_words)

###############################################
#  END: Get the number of specified comments  #
###############################################


###########################################
#  START: Funnel out possible stock names #
###########################################

potential_stock_symbols = []

known_not_stocks = ['UPVOTE', 'SUPPORT', 'YOLO', 'YOLO.', 'CLASS', 'ACTION', 'AGAINST', 'ROBINHOOD', 'GAIN', 'LOSS', 'PORN', 'WSB', 'I', 'STILL', "DIDN'T", 'HEAR', 'NO', 'BELL']

for title in words_collection:
    for word in title:
        if word.isupper() and word not in known_not_stocks:
            potential_stock_symbols.append(word)

#########################################
#  END: Funnel out possible stock names #
#########################################


#######################################
#  START: Get stock tickers from csv  #
#######################################

stocks_list = []
with open('./files/unique_usa_tickers.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        stocks_list.append(row[0])

#####################################
#  END: Get stock tickers from csv  #
#####################################


########################################
#  START: Find most discussed tickers  #
########################################

stock_dict = Counter()

def get_stock_list(comments, stocks_list):
    for potential_stock_symbol in comments:
        for ticker in stocks_list:
            if ticker == potential_stock_symbol or potential_stock_symbol == (ticker+'.') or potential_stock_symbol == ('$'+ticker) or potential_stock_symbol == (ticker+'!'):
                stock_dict[ticker] += 1

def Reverse(lst):
    new_lst = lst[::-1]
    return new_lst

get_stock_list(potential_stock_symbols, stocks_list)

ordered_stock_dict = sorted(stock_dict.items(), key=lambda stock_dict: stock_dict[1])
largest_discussed_tickers = Reverse(ordered_stock_dict)

######################################
#  END: Find most discussed tickers  #
######################################

print('\nTotal comments read :', no_of_comments)
print("\nTop 20 most discussed tickers-\n")
for tick in largest_discussed_tickers[:20]:
    print(tick)