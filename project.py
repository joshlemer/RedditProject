import sys
import praw
import operator
import time

class Frequencies:
    def __init__(self):
        self.frequencies = {}

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


class User:
    def __init__(self,projection, user, userName=None):
        if user:
            self.userName = str(user.name)
        elif userName:
            self.userName = userName
        self.subredditFrequencies = Frequencies()
        self.extendedFrequencies = Frequencies()
        self.userObject = user
        self.projection = projection
        self.totalComments = 0.0


    def get_frequencies(self):
        print "Processing User " + self.userName
        while True:
            try:
                #for comment in self.userObject.get_comments(limit=100):
                for comment in self.userObject.get_comments(limit=self.projection.thing_limit):
                    self.subredditFrequencies.add_frequency(str(comment.subreddit.display_name.strip(' ').lower()), 1.0)
                    if str(comment.subreddit.display_name.strip(' ').lower()) is str(self.projection.subreddit.display_name.strip(' ').lower()):
                        self.projection.totalComments += 1
                    self.totalComments += 1
                break
            except:
                print "error..."

    def get_extended_profile(self):
        for subreddit in self.subredditFrequencies.frequencies:
            if self.subredditFrequencies.frequencies[subreddit] > 0.1:
                subProj = Projection(subreddit, 100)
                subProj.get_comments()
                subProj.get_commentor_frequencies()
                subProj.register_subreddit_frequencies()

                self.extendedFrequencies.add_by_frequencies(subProj.frequencies)





class Projection:
    def __init__(self, subredditName, thing_limit):
        user_agent = ("Testing Reddit Functionality by /u/Reddit_Projector https://github.com/joshlemer/RedditProject")
        self.reddit = praw.Reddit(user_agent)
        self.thing_limit = thing_limit
        self.subreddit = self.reddit.get_subreddit(subredditName)
        self.comments = {}
        self.subredditFrequencies = Frequencies()
        self.commentors = []
        self.commentorNames = []

    def get_comments(self):
        while True:
            try:
                self.comments = list(self.subreddit.get_comments(limit=self.thing_limit))
                break
            except:
                print "error..."

    def register_subreddit_frequency (self, subredditName, frequency):
        if subredditName in self.subredditFrequencies.frequencies:
            self.subredditFrequencies[subredditName] += frequency
        else:
            self.subredditFrequencies[subredditName] = frequency

    def register_subreddit_frequencies(self):
        for commentor in self.commentors:
            for freq in commentor.subredditFrequencies.frequencies:
                self.subredditFrequencies.add_frequency(freq, self.calculate_frequency(commentor, freq))

    def calculate_frequency(self, commentor, subreddit):
        #(commentorComments in origSub / totalInOriginalSub) * (frequencyOfCommentorInSubreddit / totalCommenterComments)

        origSubComments = 0
        for comment in self.comments:
            if comment is not None and hasattr(comment,'author') and comment.author is not None and hasattr(comment.author, 'name') and comment.author.name is not None and str(commentor.userName) == str(comment.author.name):
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
            if comment is not None and hasattr(comment, 'author') and hasattr(comment.author, 'name') and str(comment.author) not in self.commentorNames:
                self.commentorNames.append(str(comment.author))
                newUser = User(self,comment.author)
                newUser.get_frequencies()
                self.commentors.append(newUser)

def run_analysis(subreddit, depth):
    myProj = Projection(subreddit, depth)
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

    filename = subreddit + "_" + time.strftime("%Y-%m-%d") + "_" + time.strftime("%X") + ".txt"
    file = open(filename, "w")
    for item in myList:
        file.write("%s   %s\n" % (item[0], item[1]))

    file.close()
    print "Information printed to " + filename

def run_diff_analysis(subredditA, subredditB, depth):
    projA = Projection(subredditA, depth)
    projA.get_comments()
    projA.get_commentor_frequencies()
    projA.register_subreddit_frequencies()

    projB = Projection(subredditB, depth)
    projB.get_comments()
    projB.get_commentor_frequencies()
    projB.register_subreddit_frequencies()

    diff_freqs = Frequencies()
    negative_B_freqs = Frequencies()

    negative_B_freqs.add_by_frequencies(projB.subredditFrequencies)
    negative_B_freqs.multiply_by_scalar(-1)

    diff_freqs.add_by_frequencies(projA.subredditFrequencies)
    diff_freqs.add_by_frequencies(negative_B_freqs)


    myList = []
    mySum = 0.0
    for key, value in diff_freqs.frequencies.iteritems():
        temp = [key, value]
        mySum += value
        myList.append(temp)

    myList = sorted(myList, key=operator.itemgetter(1),reverse=True)

    filename = subredditA + "-" + subredditB + "_" + time.strftime("%Y-%m-%d") + "_" + time.strftime("%X") + ".txt",
    file = open(filename , "w")
    for item in myList:
        file.write("%s   %s\n" % (item[0], item[1]))

    file.close()
    print "Information recorded to file " + filename

def run_percent_analysis(subredditA, subredditB, depth):
    projA = Projection(subredditA, depth)
    projA.get_comments()
    projA.get_commentor_frequencies()
    projA.register_subreddit_frequencies()

    projB = Projection(subredditB, depth)
    projB.get_comments()
    projB.get_commentor_frequencies()
    projB.register_subreddit_frequencies()

    percent_freqs = Frequencies()


    percent_freqs.add_by_frequencies(projA.subredditFrequencies)
    percent_freqs.divide_by_frequencies(projB.subredditFrequencies)


    myList = []
    mySum = 0.0
    for key, value in percent_freqs.frequencies.iteritems():
        temp = [key, value]
        mySum += value
        myList.append(temp)

    myList = sorted(myList, key=operator.itemgetter(1),reverse=True)

    filename = subredditA + "-percent-of" + subredditB + "_" + time.strftime("%Y-%m-%d") + "_" + time.strftime("%X") + ".txt"
    file = open(filename, "w")
    for item in myList:
        file.write("%s   %s\n" % (item[0], item[1]))

    file.close()
    print "Information printed to " + filename

if len(sys.argv) >= 2:
    if len(sys.argv) >= 3:
        if len(sys.argv) >= 4:
            run_percent_analysis(sys.argv[1], sys.argv[2],int(sys.argv[3]))
        else:
            run_analysis(sys.argv[1], int(sys.argv[2]))
    else:
        run_analysis(sys.argv[1], 10)
