This is a python program that measures how connected subreddit communities are to each other.

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
