def get_tweet_id(d):
    return d["id_str"]


def get_user_id(d):
    return d["user"]["id_str"]


def get_user_name(d):
    return d["user"]["name"]


def get_followers_count(d):
    return d["user"]["followers_count"]


def get_friends_count(d):
    return d["user"]["friends_count"]


def get_user_location(d):
    return d["user"]["location"]


def get_tweet_text(d):
    return d["text"]


def get_retweet_count(d):
    return d["retweet_count"]

accessors = {
    "tweet_id": get_tweet_id,
    "user_id": get_user_id,
    "user_name": get_user_name,
    "followers_count": get_followers_count,
    "friends_count": get_friends_count,
    "user_location": get_user_location,
    "text": get_tweet_text,
    "retweet_count": get_retweet_count
}
