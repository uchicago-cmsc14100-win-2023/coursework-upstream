"""
CMSC 14100
Winter 2023
Homework #6

A note about types for docstrings:

  You can use tweet_dict as the type of a tweet in the original format
  in your docstrings.

  You can use simple_tweet_dict as the type of tweet in the format
  returned by process_tweets.

  For tweets-by-user dictionaries, use dict(str, list[simple_tweet_dict]).

  For the results of the last 4 tasks: use dict(str, list(tuple(str)))

We will be using anonymous grading, so please do NOT include your name
in this file

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.

[RESUBMISSIONS ONLY: Explain how you addressed the grader's comments
 for your original submission.  If you did not submit a solution for the
 initial deadline, please state that this submission is new.]
"""

# import the provided function that sorts (key, value) pairs
from util import sort_count_pairs

# Exercise 1
def count_tweets_by_user(orig_tweets):
    """
    Count the number of tweets for each user in the list
    of original tweets.

    Inputs:
        orig_tweets [list[tweet_dict]]: a list of tweets in
          the original format

    Returns [dict(str, int)]: a dictonary that maps user screen
      names to integer counts.
    """
    pass


# Exercise 2
def extract_entities(orig_tweet, key, subkey):
    """
    Your doc string
    """
    pass


# Exercise 3
def process_tweets(orig_tweets, entity_descriptions):
    """
    Your doc string
    """
    pass

# Exercise 4
def organize_tweets_by_user(simple_tweets):
    """
    Your doc string
    """
    pass

# Exercise 5 and 6: helper
def get_entity_counts(tweets, entity_key):
    """
    Your doc string
    """
    pass


# Exercise 5
def find_top_k_entities(tweets_by_user, entity_key, k):
    """
    Your doc string
    """
    pass


# Exercise 6
def find_min_count_entities(tweets_by_user, entity_key, min_count):
    """
    Your doc string
    """
    pass


# Helper function for Exercises 7 and 8
def count_all_ngrams_for_user(tweets, n):
    """
    Your doc string
    """
    pass


def find_top_k_ngrams(tweets_by_user, n, k):
    """
    Your doc string
    """
    pass


def find_min_count_ngrams(tweets_by_user, n, min_count):
    """
    Your doc string
    """
    pass

