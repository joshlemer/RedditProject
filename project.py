import praw

class User:
    def __init__(self,projection, user):
        self.userName = str(user)
        self.subredditFrequency = {}
        self.userObject = user
        self.projection = projection
    def get_frequencies(self):
        for comment in self.userObject.get_comments():
            self.register_comment(comment.subreddit.display_name)

    def register_comment(self, subredditName):
        if subredditName in self.subredditFrequency:
            self.subredditFrequency[subredditName] += 1
        else:
            self.subredditFrequency[subredditName] = 1

        if subredditName is self.projection.subredditName:
            self.projection.totalComments += 1


class Projection:
    def __init__(self, subredditName):
        user_agent = ("Testing Reddit Functionality by /u/Nomopomo")
        self.reddit = praw.Reddit(user_agent)
        self.thing_limit = 10
        self.subreddit = self.reddit.get_subreddit(subredditName)
        self.comments = {}
        self.commentors = []
        self.commentorNames = []
        self.totalComments = 0

    def get_comments(self):
        self.comments = list(self.subreddit.get_comments(limit=self.thing_limit))

    def get_commentor_frequency(self):
        for comment in self.comments:
            if str(comment.author) not in self.commentorNames:
                self.commentorNames.append(str(comment.author))
                newUser = User(self,comment.author)
                newUser.get_frequencies()
                self.commentors.append(newUser)
                print newUser.subredditFrequency




def getSubredditCommentDistribution(subreddit):
    comments =  subreddit.get_comments()

    return comments_by_user


#subreddit = r.get_subreddit('LibertarianWallpapers')
#reddit_distribution = getSubredditCommentDistribution(subreddit)
#print(getSubredditCommentDistribution(subreddit))

myProj = Projection('Technology')

myProj.get_comments()

myProj.get_commentor_frequency()









