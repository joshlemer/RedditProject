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

This will result in 100 of the previous comments being analyzed, and 100 of each commenter’s other comments being analyzed for a total of 100 x 100 = 10000 comments (assuming no repeat commenters).
Careful though, time / requests increases proportional to the square of this number. 100 will take a minute or two, 500 - 45 minutes or so. 1000 - go put a pot of coffee on.

project.py will output a textfile in the folder with the most frequent subreddits commented in at the top, with percentages on the right.

You can also compare two communities, or one community against reddit as a whole, by using 3 arguments:

    python project.py AskReddit all 300

This will give a contrast between AskReddit commenters and general reddit commenters (/r/all is the combination of all subreddits).
Or you can contrast two specific communities:

    python project.py javascript python 400

This will output a text file with a list of communities and a number beside it, such as
    JavaScript  10001.4394
    Java    1.24
    Ruby    0.54

The way to interpret these results is that Javascript commenters are 10001.4394 times as likely to post in /r/JavaScript as Python commenters are.
JavaScript commenters are 24% more likely to post in Java than Python commenters are, but that Javascript commenters are only 54% as likely to post in /r/Ruby as python commenters are.



#Future features

I’ll soon have an “extended user profile” feature, where you input a reddit user, and it gathers the profiles of each of their frequented communities and amalgamates them according to how much the user goes in that community. This will be really great for predicting, say, what subreddits a user would like to comment in in the future.

In the not-too-distant future, I’d like to start saving the data to a database, possibly offering the software as a web service.


