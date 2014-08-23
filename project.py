import praw
import operator

class User:
    def __init__(self,projection, user):
        self.userName = str(user)
        self.subredditFrequencies = {}
        self.userObject = user
        self.projection = projection
        self.totalComments = 0.0

    def get_frequencies(self):
        for comment in self.userObject.get_comments():
            self.register_comment(comment.subreddit.display_name)

    def register_comment(self, subredditName):
        if subredditName in self.subredditFrequencies:
            self.subredditFrequencies[subredditName] += 1
        else:
            self.subredditFrequencies[subredditName] = 1

        if subredditName is self.projection.subreddit.display_name:
            self.projection.totalComments += 1
            """
            print subredditName
            print self.subredditFrequencies
            """

        self.totalComments += 1


class Projection:
    def __init__(self, subredditName):
        user_agent = ("Testing Reddit Functionality by /u/Nomopomo https://github.com/joshlemer/RedditProject")
        self.reddit = praw.Reddit(user_agent)
        self.thing_limit = 400
        self.subreddit = self.reddit.get_subreddit(subredditName)
        self.comments = {}
        self.subredditFrequencies = {}
        self.commentors = []
        self.commentorNames = []

    def get_comments(self):
        self.comments = list(self.subreddit.get_comments(limit=self.thing_limit))

        #print self.comments

    def register_subreddit_frequency (self, subredditName, frequency):
        if subredditName in self.subredditFrequencies:
            self.subredditFrequencies[subredditName] += frequency
        else:
            self.subredditFrequencies[subredditName] = frequency

    def register_subreddit_frequencies(self):
        for commentor in self.commentors:
            for freq in commentor.subredditFrequencies:
                self.register_subreddit_frequency(freq, self.calculate_frequency(commentor, freq))

    def calculate_frequency(self, commentor, subreddit):
        #(commentorComments in origSub / totalInOriginalSub) * (frequencyOfCommentorInSubreddit / totalCommenterComments)

        origSubComments = commentor.subredditFrequencies.get(self.subreddit.display_name)

        if origSubComments is None:
            origSubComments = 0.0
        absFreq = commentor.subredditFrequencies.get(subreddit)
        if absFreq is None:
            absFreq = 0.0

        return ((origSubComments + 0.0)/len(self.comments)) * ((0.0 + absFreq) / commentor.totalComments)

    def get_commentor_frequencies(self):
        for comment in self.comments:
            if str(comment.author) not in self.commentorNames:
                self.commentorNames.append(str(comment.author))
                newUser = User(self,comment.author)
                newUser.get_frequencies()
                self.commentors.append(newUser)

myProj = Projection('Technology')

myProj.get_comments()

myProj.get_commentor_frequencies()

myProj.register_subreddit_frequencies()

print myProj.subredditFrequencies

print sorted(myProj.subredditFrequencies.iteritems(), key=operator.itemgetter(1))









