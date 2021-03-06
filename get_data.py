import praw
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

class data:
    def __init__(self, comments, x_subs):
        self.comments = comments
        self.x_subs = x_subs


def remove_sub_data(subredditName):
    the_data = pickle.load(open('data.pkl', 'rb'))
    comments = the_data.comments
    x_subs = the_data.x_subs

    comments = [x for x in comments if x.subreddit.lower() != subredditName]
    x_subs = [x for x in x_subs if x != subredditName]

    the_data = data(comments, x_subs )
    print x_subs
    output = open('data.pkl', 'wb')
    pickle.dump(the_data,output)
    output.close()




def add_sub_data(subredditName, num_redditors):
    user_agent = ("Testing Reddit Functionality by /u/Reddit_Projector https://github.com/joshlemer/RedditProject")
    reddit = praw.Reddit(user_agent)
    subreddit_object = reddit.get_subreddit(subredditName)

    the_data = pickle.load(open('data.pkl', 'rb'))
    comments = the_data.comments
    x_subs = the_data.x_subs
    y_comments = [comment(a) for a in subreddit_object.get_comments(limit=num_redditors)]

    z_comments = []
    redditors = []
    i = 0
    for y_com in y_comments:
        print y_com.subreddit, " z = ", i
        redditor = y_com.author_name
        if redditor not in redditors:
            try:
                z_comments += [comment(a) for a in reddit.get_redditor(y_com.author_name).get_comments(limit=100)]
                redditors.append(redditor)
            except:
                print "oops, that user is weird"
        i += 1

    comments += list(z_comments)
    print "COMMENTS LENGTH: ", len(comments)
    the_data = data(comments, x_subs + [subredditName] )
    output = open('data.pkl', 'wb')
    pickle.dump(the_data,output)
    output.close()



if __name__ == "__main__":
    user_agent = ("Testing Reddit Functionality by /u/Reddit_Projector https://github.com/joshlemer/RedditProject")
    reddit = praw.Reddit(user_agent)
    subredditName = 'all'
    subreddit_object = reddit.get_subreddit(subredditName)
    y = 5 #Comments per subreddit inspected
    z = 100 #Comments per user inspected



    #List of subreddits to be analyzed
    # x_subs = [
    #     'hiphopheads',
    #     'metal',
    #     'postrock',
    #     'letstalkmusic' ]

    #Commented code below is for pulling our x_subs from the most recent comments in /r/all

    # x_comments = [comment(a) for a in subreddit_object.get_comments(limit=x)]
    # i = 0
    # for c in x_comments:
    #     print "x = ", i
    #     if c.subreddit not in x_subs:
    #         x_subs.append(c.subreddit)
    #     i += 1

    #List of subreddits to be analyzed
    x_subs = [
        'hiphopheads',
        'metal',
        'postrock',
        'letstalkmusic' ]

    y_comments = []
    i = 0
    print "Getting ", y, " comments from each of the ", len(x_subs), " subreddits"
    for x_sub in x_subs:
        print "\tRetrieving ", 5, " comments from /r/", x_sub
        subreddit_object = reddit.get_subreddit(x_sub)
        y_comments += [comment(a) for a in subreddit_object.get_comments(limit=y)]
        i += 1

    z_comments = []
    redditors = []
    i = 0
    print "Following commenters from original subs to gather their other reddit activity"
    for y_com in y_comments:
        redditor = y_com.author_name
        print "\tAnalyzing user ", redditor, " (user ", i, "/", len(y_comments), ")"
        if redditor not in redditors:
            try:
                z_comments += [comment(a) for a in reddit.get_redditor(y_com.author_name).get_comments(limit=z)]
                redditors.append(redditor)
            except:
                print "\t\toops, that user is weird\n\t\tprobably deleted their comment or profile or something"
        else:
            print "\t\tAlready looked at this user, no need to make an other call."
        i += 1

    comments = list(z_comments)
    print "COMMENTS LENGTH: ", len(comments)
    the_data = data(comments, x_subs)
    output = open('data.pkl', 'wb')
    pickle.dump(the_data,output)
    output.close()
