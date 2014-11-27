import praw
import scipy as sp
#import numpy as np
#import sys
#import operator
#import time
#import project as p
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hi
import pickle
import copy

class histogram:
    def __init__(self, dictionary=None):
        self.frequencies = {}
        if dictionary is not None:
            self.frequencies = copy.deepcopy(dictionary)

    def get_sum(self):
        the_sum = 0
        for e in self.frequencies:
            the_sum += self.frequencies[e]
        return the_sum

    def add_frequency(self, key, value):
        if key in self.frequencies:
            self.frequencies[key] += value
        else:
            self.frequencies[key] = value

    def add_by_frequencies(self,frequencies):
        for key in frequencies.frequencies:
            self.add_frequency(key, frequencies.frequencies[key])

    def multiply_frequency(self, key, value):
        if key in self.frequencies:
            self.frequencies[key] *= value
        else:
            self.frequencies[key] = 0.0

    def multiply_by_frequencies(self, frequencies):
        for key in frequencies.frequencies:
            self.multiply_frequency(key, frequencies.frequencies[key])

    def multiply_by_scalar(self, scalar):
        for key in self.frequencies:
            self.multiply_frequency(key,scalar)

    def divide_frequency(self, key, value):
        if key in self.frequencies:
            if value != 0:
                if self.frequencies[key] == 0:
                    self.frequencies[key] = 1.0
                else:
                    self.frequencies[key] /= (0.0 + value)
            else:
                if self.frequencies[key] == 0:
                    self.frequencies[key] = 1.0
                else:
                    self.frequencies[key] = float('inf')
        else:
            if value > 0:
                self.frequencies[key] = 0.0
            else:
                self.frequencies[key] = 1.0

    def divide_by_frequencies(self, frequencies):
        for key in frequencies.frequencies:
            self.divide_frequency(key, frequencies.frequencies[key])


class comment:
    def __init__(self, comment):
        if comment is not None and hasattr(comment,'author') and comment.author is not None and hasattr(comment.author, 'name'):
            self.author_name = comment.author.name
        else:
            self.author_name = ''

        self.subreddit = str(comment.subreddit.display_name.strip(' ').lower())

class user:
    @staticmethod
    def get_histogram(comments, author_name):
        total_comments_by_author = 0
        the_histogram = histogram()
        for comment in comments:
            if comment.author_name == author_name:
                total_comments_by_author += 1
                the_histogram.add_frequency(comment.subreddit, 1)
        the_histogram.multiply_by_scalar(1.0 / total_comments_by_author)
        #print author_name, " ", the_histogram.get_sum()
        return the_histogram.frequencies

class community:
    @staticmethod
    def get_histogram(comments, subreddit_name):
        total_comments_in_subreddit = 0
        the_histogram = histogram()
        for comment in comments:
            if comment.subreddit == subreddit_name:
                total_comments_in_subreddit += 1
                the_histogram.add_frequency(comment.author_name, 1)
        the_histogram.multiply_by_scalar(1.0 / total_comments_in_subreddit)
        return the_histogram.frequencies


user_agent = ("Testing Reddit Functionality by /u/Reddit_Projector https://github.com/joshlemer/RedditProject")
reddit = praw.Reddit(user_agent)
subredditName = 'all'
subreddit_object = reddit.get_subreddit(subredditName)


x = 5
y = 15
z = 100
comments = [comment(a) for a in subreddit_object.get_comments(limit=x)]
x_comments = [comment(a) for a in subreddit_object.get_comments(limit=x)]
x_subs = []
i = 0
for c in x_comments:
    print "x = ", i
    if c.subreddit not in x_subs:
        x_subs.append(c.subreddit)
    i += 1
x_subs = ['guitar', 'bass','socialism','conservative','libertarian','politics','linux','opensource','games','opensourcegames']

y_comments = []
i = 0
for x_sub in x_subs:
    print "y = ", i
    subreddit_object = reddit.get_subreddit(x_sub)
    y_comments += [comment(a) for a in subreddit_object.get_comments(limit=y)]
    i += 1

z_comments = []
redditors = []
i = 0
for y_com in y_comments:
    print "z = ", i
    redditor = y_com.author_name
    if redditor not in redditors:
        z_comments += [comment(a) for a in reddit.get_redditor(y_com.author_name).get_comments(limit=z)]
        redditors.append(redditor)
    i += 1

comments = list(z_comments)
print "COMMENTS LENGTH: ", len(comments)
output = open('data.pkl', 'wb')
pickle.dump(comments,output)
output.close()

users = {}
for comment in comments:
    if comment.author_name not in users:
        users[comment.author_name] = user.get_histogram(comments, comment.author_name)

#for c in comments:
#    print "%s\t%s" % (c.author_name, c.subreddit)

#print users


#Will be of form {'sub_A': {'user_A':0.5, 'user_B': 0.5}, 'sub_B':{...}}
subreddits = {}
for comment in comments:
    if comment.subreddit not in subreddits:
        subreddits[comment.subreddit] = community.get_histogram(comments, comment.subreddit)

#print subreddits

sub_relatedness = {}
for sub in x_subs:
    sub_histogram = histogram()
    for user in subreddits[sub]:
        user_histogram = histogram(users[user])
        print user, ' ', user_histogram.get_sum()
        user_histogram.multiply_by_scalar(subreddits[sub][user])

        sub_histogram.add_by_frequencies(user_histogram)
    sub_relatedness[sub] = sub_histogram.frequencies

print "SubredditsRelatedness:"
print sub_relatedness
for s in sub_relatedness:
    s_sum= 0
    for t in sub_relatedness[s]:
        s_sum += sub_relatedness[s][t]
    print s, ' ', s_sum
    if s_sum != 1.0:
        print subreddits[s]
        for u in subreddits[s]:
            print u, users[u]

#print sub_relatedness

"""
for u in sub_relatedness:
    if len(sub_relatedness[u]) != 1:
        print u, sub_relatedness[u]
"""

subreddit_names = [w for w in subreddits]
#print subreddit_names
subreddit_rows = []
#for sub in subreddit_names:
for sub in x_subs:
    sub_row = []
    for sub_name in subreddit_names:
	if sub_name in sub_relatedness[sub]:
            sub_row.append(sub_relatedness[sub][sub_name])
        else:
            sub_row.append(float(0))
    subreddit_rows.append(sub_row)
#print subreddit_rows

b = sp.spatial.distance.pdist(subreddit_rows, 'euclidean')
print "spatial distances calculated"
c = hi.linkage(b,method='single', metric='euclidean')
print "linkages calculated"
hi.dendrogram(c,labels=x_subs)
plt.title("Using min-distance merging")
plt.show()

c = hi.linkage(b,method='complete', metric='euclidean')
print "linkages calculated"
hi.dendrogram(c,labels=x_subs)
plt.title("Using max-distance merging")
plt.show()

for row in subreddit_rows:
    row_sum = 0
    for elem in row:
        row_sum += elem
    print row_sum









