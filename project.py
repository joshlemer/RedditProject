import praw

user_agent = ("Testing Reddit Functionality by /u/Nomopomo ")

r = praw.Reddit(user_agent)

user = r.get_redditor("Nomopomo")
thing_limit = 10
gen = user.get_submitted(limit=thing_limit)

karma_by_subreddit = {}

for thing in gen:
    subreddit = thing.subreddit.display_name
    karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)

print(karma_by_subreddit)




