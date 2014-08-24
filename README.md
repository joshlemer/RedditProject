This is a python program that measures how connected subreddit communities are to each other.

The metric used is to take the proportion of comments made in each subreddit, by each commenter in the target subreddit, and then weigh the results proportionally to how active they are in the target subreddit.

#An overview of the metric and algorithm

    dictionary findConnectedSubreddits (subreddit sub)
        for all commenters usr of sub
            let usr.prop be the proportion of comments in sub made by usr

            let usr.totalComments = 0
            for all subreddits usrSub that usr commented in
                let usr.dist[commSub] be the number of comments made by usr in usrSub
                usr.totalComments += usr.dist[commSub]

            for all subreddits usrSub that usr commented in
                sub.connection[usrSub] += usr.dist[usrSub] * usr.prop

        return sub.connection

#Installation and usage

You will need to have python 2.7.8 installed, as well as pip. In Ubuntu/Debian:

    sudo apt-get install python
    sudo apt-get install python-pip python-dev build-essential 

This program also requires you install PRAW, a library used to access the Reddit API in Python

    sudo pip install praw

And to use the program, just 

    python project.py YourSubredditHere 

If you want to analyze more than 10 commenters and 10 of their comments each, then add an integer argument
    
    python project.py YourSubredditHere 100

Careful though, time / requests increases proportional to the square of this number. 100 will take a minute or two, 500 - 45 minutes or so. 1000 - Go put a pot of coffee on.

project.py will output a textfile in the folder with the most frequent subreddits commented in at the top, with percentages on the right.

#Future features

I’ll soon have an “extended user profile” feature, where you input a reddit user, and it gathers the profiles of each of their frequented communities and amalgamates them according to how much the user goes in that community. This will be really great for predicting, say, what subreddits a user would like to comment in in the future.

In the not-too-distant future, I’d like to start saving the data to a database, possibly offering the software as a web service.


