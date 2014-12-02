import scipy as sp
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hi
import pickle
import copy
import get_data as gd


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


class data:
    def __init__(self, comments, x_subs):
        self.comments = comments
        self.x_subs = x_subs

the_data = pickle.load(open('data.pkl', 'rb'))
comments = the_data.comments
x_subs = the_data.x_subs

users = {}
for comment in comments:
    if comment.author_name not in users:
        users[comment.author_name] = gd.user.get_histogram(comments, comment.author_name)

#Will be of form {'sub_A': {'user_A':0.5, 'user_B': 0.5}, 'sub_B':{...}}
subreddits = {}
for comment in comments:
    if comment.subreddit not in subreddits:
        subreddits[comment.subreddit] = gd.community.get_histogram(comments, comment.subreddit)

#print subreddits

sub_relatedness = {}
for sub in x_subs:
    sub_histogram = histogram()
    for u in subreddits[sub]:
        user_histogram = histogram(users[u])
        print u, ' ', user_histogram.get_sum()
        user_histogram.multiply_by_scalar(subreddits[sub][u])

        sub_histogram.add_by_frequencies(user_histogram)
    sub_relatedness[sub] = sub_histogram.frequencies


subreddit_names = [w for w in subreddits]
subreddit_rows = []
for sub in x_subs:
    sub_row = []
    for sub_name in subreddit_names:
	if sub_name in sub_relatedness[sub]:
            sub_row.append(sub_relatedness[sub][sub_name])
        else:
            sub_row.append(float(0))
    subreddit_rows.append(sub_row)
#print subreddit_rows

import sklearn.preprocessing
subreddit_rows = sklearn.preprocessing.normalize(subreddit_rows)

b = sp.spatial.distance.pdist(subreddit_rows, 'euclidean')
c = hi.linkage(b,method='complete', metric='euclidean')
print "linkages calculated"
hi.dendrogram(c,labels=x_subs,orientation='right')
plt.title("Euclidean")
plt.show()
