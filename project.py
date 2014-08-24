import praw
import operator

class User:
    def __init__(self,projection, user):
        self.userName = str(user.name)
        self.subredditFrequencies = {}
        self.userObject = user
        self.projection = projection
        self.totalComments = 0.0

    def get_frequencies(self):
        print "Processing User " + self.userName
        for comment in self.userObject.get_comments(limit=self.projection.thing_limit):
            self.register_comment(str(comment.subreddit.display_name.strip(' ').lower()))

    def register_comment(self, subredditName):
        if str(subredditName.strip(' ').lower()) in self.subredditFrequencies:
            self.subredditFrequencies[str(subredditName.strip(' ').lower())] += 1
        else:
            self.subredditFrequencies[str(subredditName.strip(' ').lower())] = 1

        if str(subredditName.strip(' ').lower()) is str(self.projection.subreddit.display_name.strip(' ').lower()):
            self.projection.totalComments += 1

        self.totalComments += 1
        """
        print "THIS IS REGISTERING"
        print subredditName.strip(' ').lower() + " " + self.projection.subreddit.display_name.strip(' ').lower()
        print subredditName
        print self.subredditFrequencies
        else:
        print subredditName.strip(' ').lower() + " " + self.projection.subreddit.display_name.strip(' ').lower()
        """


class Projection:
    def __init__(self, subredditName):
        user_agent = ("Testing Reddit Functionality by /u/Nomopomo https://github.com/joshlemer/RedditProject")
        self.reddit = praw.Reddit(user_agent)
        self.thing_limit = 100
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

        #origSubComments = commentor.subredditFrequencies.get(str(self.subreddit.display_name).strip(' ').lower())
        origSubComments = 0
        for comment in self.comments:
            if str(commentor.userName) == str(comment.author.name):
                origSubComments += 1

        if origSubComments is None:
            origSubComments = 0.0
        absFreq = commentor.subredditFrequencies.get(subreddit)
        if absFreq is None:
            absFreq = 0.0

        result = ((origSubComments + 0.0)/len(self.comments)) * ((0.0 + absFreq) / commentor.totalComments)
        print "%s %s %s %s %s" % (origSubComments, len(self.comments), absFreq, commentor.totalComments, result)
        return result

    def get_commentor_frequencies(self):
        for comment in self.comments:
            if str(comment.author) not in self.commentorNames:
                self.commentorNames.append(str(comment.author))
                newUser = User(self,comment.author)
                newUser.get_frequencies()
                self.commentors.append(newUser)

def run_Analysis():
    #theSubreddit = 'Anarcho_CapiTALism'

    myProj = Projection('Bonsai')

    myProj.get_comments()

    myProj.get_commentor_frequencies()

    myProj.register_subreddit_frequencies()

    myList = []
    mySum = 0.0
    for key, value in myProj.subredditFrequencies.iteritems():
        temp = [key, value]
        mySum += value
        myList.append(temp)

    myList = sorted(myList, key=operator.itemgetter(1),reverse=True)

    for item in myList:
        print "%s   %s" % (item[0], item[1])

    print mySum


run_Analysis()
#print myProj.subredditFrequencies
#print sorted(myProj.subredditFrequencies.iteritems(), key=operator.itemgetter(1))











