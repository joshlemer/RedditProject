import sys
import praw
import operator
import time

class Frequencies:
    def __init__(self, frequencies={}):
        self.frequencies = frequencies

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


class User:
    def __init__(self,subreddit, user):
        self.thing_limit = 10
        self.userName = str(user.name)
        self.subredditFrequencies = Frequencies()
        self.userFrequencies = Frequencies()
        self.userObject = user
        self.subreddit = subreddit
        self.comments = []
        self.subreddits = []
        self.totalComments = 0.0


    def get_frequencies(self):
        print "Processing User " + self.userName
        for comment in self.userObject.get_comments(limit=self.thing_limit):
            self.subredditFrequencies.add_frequency(str(comment.subreddit.display_name.strip(' ').lower()), 1.0)

            if(self.subreddit):
                if str(comment.subreddit.display_name.strip(' ').lower()) is str(self.projection.subreddit.display_name.strip(' ').lower()):
                    self.subreddit.totalComments += 1

            self.totalComments += 1

    def get_comments(self):
        self.comments = list(self.userObject.get_comments(limit=self.thing_limit))
        for comment in self.comments:
            self.subredditFrequencies.add_frequency(str(comment.subreddit.display_name.strip(' ').lower()), 1.0)

    def register_user_frequencies(self):
        for subreddit in self.subreddits:
            for freq in subreddit.userFrequencies.frequencies:
                self.userFrequencies.add_frequency(freq, self.calculate_frequency(subreddit, freq))

    def calculate_frequency(self, commentor, subreddit):
        #(subredditComments from originalUser / total originalUser comments) * (frequencyOfSubredditInUser / totalSubredditComments)

        origSubComments = 0
        for comment in self.comments:
            if str(commentor.userName) == str(comment.author.name):
                origSubComments += 1

        if origSubComments is None:
            origSubComments = 0.0
        absFreq = commentor.subredditFrequencies.frequencies.get(subreddit)
        if absFreq is None:
            absFreq = 0.0

        result = ((origSubComments + 0.0)/len(self.comments)) * ((0.0 + absFreq) / commentor.totalComments)
        #print "%s %s %s %s %s" % (origSubComments, len(self.comments), absFreq, commentor.totalComments, result)
        return result

    def get_subreddit_frequencies(self):
        i = 0
        for subreddit in self.subreddits:
            i += 1
            print "On subreddit %d / %d" % (i, self.thing_limit)
            if str(subreddit.display_name) not in self.subredditFrequencies.frequencies:
                self.subredditFrequencies.add_frequency(str(subreddit.display_name.strip(' ').lower()))
                newSubreddit = Subreddit(self, str(subreddit.display_name.strip(' ').lower()))
                newSubreddit.get__frequencies()
                self.subreddits.append(newSubreddit)




class Projection:
    def __init__(self, center, outers):
        self.center_frequencies = Frequencies()
        self.center_name = ""
        self.outer_objects = {}
        self.outer_object_names = []
        self.object_weights = {}



class Subreddit:
    def __init__(self, subredditName, thing_limit):
        user_agent = ("Testing Reddit Functionality by /u/Nomopomo https://github.com/joshlemer/RedditProject")
        self.reddit = praw.Reddit(user_agent)
        self.thing_limit = thing_limit
        self.subreddit = self.reddit.get_subreddit(subredditName)
        self.comments = {}
        self.subredditFrequencies = Frequencies()
        self.commentors = []
        self.commentorNames = []

    def get_comments(self):
        self.comments = list(self.subreddit.get_comments(limit=self.thing_limit))

    def register_subreddit_frequencies(self):
        for commentor in self.commentors:
            for freq in commentor.subredditFrequencies.frequencies:
                self.subredditFrequencies.add_frequency(freq, self.calculate_frequency(commentor, freq))

    def calculate_frequency(self, commentor, subreddit):
        #(commentorComments in origSub / totalInOriginalSub) * (frequencyOfCommentorInSubreddit / totalCommenterComments)

        origSubComments = 0
        for comment in self.comments:
            if str(commentor.userName) == str(comment.author.name):
                origSubComments += 1

        if origSubComments is None:
            origSubComments = 0.0
        absFreq = commentor.subredditFrequencies.frequencies.get(subreddit)
        if absFreq is None:
            absFreq = 0.0

        result = ((origSubComments + 0.0)/len(self.comments)) * ((0.0 + absFreq) / commentor.totalComments)
        #print "%s %s %s %s %s" % (origSubComments, len(self.comments), absFreq, commentor.totalComments, result)
        return result

    def get_commentor_frequencies(self):
        i = 0
        for comment in self.comments:
            i += 1
            print "On comment %d / %d" % (i, self.thing_limit)
            if str(comment.author) not in self.commentorNames:
                self.commentorNames.append(str(comment.author))
                newUser = User(self,comment.author)
                newUser.get_frequencies()
                self.commentors.append(newUser)

def run_analysis(subreddit, depth):
    myProj = Subreddit(subreddit, depth)
    myProj.get_comments()
    myProj.get_commentor_frequencies()
    myProj.register_subreddit_frequencies()

    myList = []
    mySum = 0.0
    for key, value in myProj.subredditFrequencies.frequencies.iteritems():
        temp = [key, value]
        mySum += value
        myList.append(temp)

    myList = sorted(myList, key=operator.itemgetter(1),reverse=True)

    file = open(subreddit + "_" + time.strftime("%Y-%m-%d") + "_" + time.strftime("%X") + ".txt", "w")
    for item in myList:
        file.write("%s   %s\n" % (item[0], item[1]))

    file.close()


if len(sys.argv) >= 2:
    if len(sys.argv) >= 3:
        run_analysis(sys.argv[1], int(sys.argv[2]))
    else:
        run_analysis(sys.argv[1], 10)











