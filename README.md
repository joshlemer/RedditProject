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

    python project.py

I haven’t added command line arguments yet but will soon. For now you’ll have to hardcode the subreddit you want to inspect.
