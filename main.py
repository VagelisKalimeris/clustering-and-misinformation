###############################################################################
# AUTHOR        : Evangelos Kalimeris                                         #
#                                                                             #
# PROJECT NAME  : Clustering and Misinformation                               #
#                                                                             #
# FILE NAME     : main.py                                                     #
#                                                                             #
###############################################################################
import csv
from statistics import mean
from util_funcs import get_posts_and_retweets, get_avg_and_max_links, \
    get_avg_cross_group_links, export_connectivity


# News ranges
BF_REAL_RANGE, BF_FAKE_RANGE, PF_REAL_RANGE, PF_FAKE_RANGE = \
    range(1, 92), range(92, 183), range(1, 121), range(121, 241)


################################################################################
#                             DEAL WITH FILE I/O                               #
################################################################################
# Open files relating users with news
with open('Data/BuzzFeed/BuzzFeedNewsUser.txt', 'r') as file:
    buzzfeed_news_user = [str.rstrip().split('\t') for str in file.readlines()]
with open('Data/PolitiFact/PolitiFactNewsUser.txt', 'r') as file:
    politifact_news_user = [str.rstrip().split('\t') for str in file.readlines()]
# Open files relating users to users
with open('Data/BuzzFeed/BuzzFeedUserUser.txt', 'r') as file:
    buzzfeed_user_user = [str.rstrip().split('\t') for str in file.readlines()]
with open('Data/PolitiFact/PolitiFactUserUser.txt', 'r') as file:
    politifact_user_user = [str.rstrip().split('\t') for str in file.readlines()]

# Export user-user data to csv for Gephi analysis
with open('Data/BuzzFeed/BuzzFeedUserUser.csv', 'w') as bf_user_user_csv:
    writer = csv.writer(bf_user_user_csv)
    writer.writerow(['Source', 'Target'])
    for line in buzzfeed_user_user:
        writer.writerow(line)
with open('Data/PolitiFact/PolitiFactUserUser.csv', 'w') as pf_user_user_csv:
    writer = csv.writer(pf_user_user_csv)
    writer.writerow(['Source', 'Target'])
    for line in politifact_user_user:
        writer.writerow(line)


################################################################################
# TASK        : 1                                                              #
#                                                                              #
# OBJECTIVE   : Find the total amounts of users posting real/fake/both news.   #
#               Also sum up each group's re-tweets.                            #
#                                                                              #
################################################################################
# BUZZFEED
bf_real_posts_arr, bf_fake_posts_arr, bf_real_retweets_sum, \
bf_fake_retweets_sum = get_posts_and_retweets(buzzfeed_news_user,
                                              BF_REAL_RANGE, BF_FAKE_RANGE)
bf_both_posters_arr = set(bf_real_posts_arr) & set(bf_fake_posts_arr)
bf_real_posters_arr = set(bf_real_posts_arr) - bf_both_posters_arr
bf_fake_posters_arr = set(bf_fake_posts_arr) - bf_both_posters_arr
bf_real_posters_sum, bf_fake_posters_sum = len(bf_real_posters_arr), \
                                           len(bf_fake_posters_arr)
bf_both_posters_sum = len(bf_both_posters_arr)

# POLITIFACT
pf_real_posts_arr, pf_fake_posts_arr,pf_real_retweets_sum, \
pf_fake_retweets_sum = get_posts_and_retweets(politifact_news_user,
                                              PF_REAL_RANGE, PF_FAKE_RANGE)
pf_both_posters_arr = set(pf_real_posts_arr) & set(pf_fake_posts_arr)
pf_real_posters_arr = set(pf_real_posts_arr) - pf_both_posters_arr
pf_fake_posters_arr = set(pf_fake_posts_arr) - pf_both_posters_arr
pf_real_posters_sum, pf_fake_posters_sum = len(pf_real_posters_arr), \
                                           len(pf_fake_posters_arr)
pf_both_posters_sum = len(pf_both_posters_arr)

# Prints
print("\n" + str(bf_real_posters_sum), "total users posted real news on "
                                        "BuzzFeed.")
print(str(bf_fake_posters_sum), "total users posted fake news on BuzzFeed.")
print(str(bf_both_posters_sum), "total users posted both real and fake news "
                              "on BuzzFeed.")
print("\n" + str(pf_real_posters_sum), "total users posted real news on "
                                        "PolitiFact.")
print(str(pf_fake_posters_sum), "total users posted fake news on PolitiFact.")
print(str(pf_both_posters_sum), "total users posted both real and fake news "
                              "on PolitiFact.")


################################################################################
# TASK        : 2                                                              #
#                                                                              #
# OBJECTIVE   : Find the average of tweet/re-tweet rate for each list.         #
#                                                                              #
################################################################################
# BUZZFEED
bf_real_tweets_avg = mean(bf_real_posts_arr.count(id) for id in
                            bf_real_posters_arr)
bf_fake_tweets_avg = mean(bf_fake_posts_arr.count(id) for id in
                            bf_fake_posters_arr)

# POLITIFACT
pf_real_tweets_avg = mean(pf_real_posts_arr.count(id) for id in
                            pf_real_posters_arr)
pf_fake_tweets_avg = mean(pf_fake_posts_arr.count(id) for id in
                            pf_fake_posters_arr)

# BUZZFEED
bf_real_retweets_avg = bf_real_retweets_sum / len(bf_real_posts_arr)
bf_fake_retweets_avg = bf_fake_retweets_sum / len(bf_fake_posts_arr)

# POLITIFACT
pf_real_retweets_avg = pf_real_retweets_sum / len(pf_real_posts_arr)
pf_fake_retweets_avg = pf_fake_retweets_sum / len(pf_fake_posts_arr)

# Prints
print("\nAverage tweet rate for buzzfeed real news:",
      str(round(bf_real_tweets_avg, 2)))
print("Average tweet rate for buzzfeed fake news:",
      str(round(bf_fake_tweets_avg, 2)))
print("Average tweet rate for politifact real news:",
      str(round(pf_real_tweets_avg, 2)))
print("Average tweet rate for politifact fake news:",
      str(round(pf_fake_tweets_avg, 2)))
print("\nAverage re-tweet rate for buzzfeed real news:",
      str(round(bf_real_retweets_avg, 2)))
print("Average re-tweet rate for buzzfeed fake news:",
      str(round(bf_fake_retweets_avg, 2)))
print("Average re-tweet rate for politifact real news:",
      str(round(pf_real_retweets_avg, 2)))
print("Average re-tweet rate for politifact fake news:",
      str(round(pf_fake_retweets_avg, 2)))


################################################################################
# TASK        : 3                                                              #
#                                                                              #
# OBJECTIVE   : Find the average of friends for each list.                     #
#                                                                              #
################################################################################
# BUZZFEED
# Create Inlink and Outlink arrays
bf_from_arr, bf_to_arr = [int(x[0]) for x in buzzfeed_user_user], \
                   [int(x[1]) for x in buzzfeed_user_user]
# Real Outlinks
bf_real_avg_outlinks, bf_max_real_outlinks = \
    get_avg_and_max_links(bf_real_posters_arr, bf_from_arr, bf_real_posters_sum)
# Real Inlinks
bf_real_avg_inlinks, bf_max_real_inlinks = \
    get_avg_and_max_links(bf_real_posters_arr, bf_to_arr, bf_real_posters_sum)
# Fake Outlinks
bf_fake_avg_outlinks, bf_max_fake_outlinks = \
    get_avg_and_max_links(bf_fake_posters_arr, bf_from_arr, bf_fake_posters_sum)
# Fake Inlinks
bf_fake_avg_inlinks, bf_max_fake_inlinks = \
    get_avg_and_max_links(bf_fake_posters_arr, bf_to_arr, bf_fake_posters_sum)

# POLITIFACT
# Create Inlink and Outlink arrays
pf_from_arr, pf_to_arr = [int(x[0]) for x in politifact_user_user], \
                   [int(x[1]) for x in politifact_user_user]
# Real Outlinks
pf_real_avg_outlinks, pf_max_real_outlinks = \
    get_avg_and_max_links(pf_real_posters_arr, pf_from_arr, pf_real_posters_sum)
# Real Inlinks
pf_real_avg_inlinks, pf_max_real_inlinks = \
    get_avg_and_max_links(pf_real_posters_arr, pf_to_arr, pf_real_posters_sum)
# Fake Outlinks
pf_fake_avg_outlinks, pf_max_fake_outlinks = \
    get_avg_and_max_links(pf_fake_posters_arr, pf_from_arr, pf_fake_posters_sum)
# Fake Inlinks
pf_fake_avg_inlinks, pf_max_fake_inlinks = \
    get_avg_and_max_links(pf_fake_posters_arr, pf_to_arr, pf_fake_posters_sum)

# Prints
print("\nAverage buzzfeed users following of users that posted real news:",
      str(round(bf_real_avg_outlinks, 2)), ", max :", str(bf_max_real_outlinks))
print("Average buzzfeed followers of users that posted real news:",
      str(round(bf_real_avg_inlinks, 2)), ", max :", str(bf_max_real_inlinks))
print("Average buzzfeed users following of users that posted fake news: ",
      str(round(bf_fake_avg_outlinks, 2)), ", max :", str(bf_max_fake_outlinks))
print("Average buzzfeed followers of users that posted fake news: ",
      str(round(bf_fake_avg_inlinks, 2)), ", max :", str(bf_max_fake_inlinks))
print("\nAverage politifact users following of users that posted real news:",
      str(round(pf_real_avg_outlinks, 2)), ", max :", str(pf_max_real_outlinks))
print("Average politifact followers of users that posted real news:",
      str(round(pf_real_avg_inlinks, 2)), ", max :", str(pf_max_real_inlinks))
print("Average politifact users following of users that posted fake news: ",
      str(round(pf_fake_avg_outlinks, 2)), ", max :", str(pf_max_fake_outlinks))
print("Average politifact followers of users that posted fake news: ",
      str(round(pf_fake_avg_inlinks, 2)), ", max :", str(pf_max_fake_inlinks))


################################################################################
# TASK        : 4                                                              #
#                                                                              #
# OBJECTIVE   : Find connectivity between real and fake news spreaders.        #
#                                                                              #
################################################################################
# Calculate total users for both datasets
bf_total_users = bf_real_posters_sum + bf_fake_posters_sum - bf_both_posters_sum
pf_total_users = pf_real_posters_sum + pf_fake_posters_sum - pf_both_posters_sum


# BUZZFEED
bf_avg_real2real, bf_avg_real2fake, bf_avg_fake2fake, bf_avg_fake2real = \
    get_avg_cross_group_links(buzzfeed_user_user, bf_real_posters_arr,
                  bf_fake_posters_arr, bf_real_posters_sum, bf_fake_posters_sum)

# POLITIFACT
pf_avg_real2real, pf_avg_real2fake, pf_avg_fake2fake, pf_avg_fake2real = \
    get_avg_cross_group_links(politifact_user_user, pf_real_posters_arr,
                  pf_fake_posters_arr, pf_real_posters_sum, pf_fake_posters_sum)
# Prints
print("\nThe avg of connections from real news posters to real news posters"
      " on buzzfeed: " + str(round(bf_avg_real2real, 2)))
print("The avg of connections from real news posters to fake news posters"
      " on buzzfeed: " + str(round(bf_avg_fake2real, 2)))
print("The avg of connections from fake news posters to real news posters"
      " on buzzfeed: " + str(round(bf_avg_fake2real, 2)))
print("The avg of connections from fake news posters to fake news posters"
      " on buzzfeed: " + str(round(bf_avg_fake2fake, 2)))
print("The avg of connections from real news posters to real news posters"
      " on politifact: " + str(round(pf_avg_real2real, 2)))
print("The avg of connections from real news posters to fake news posters"
      " on politifact: " + str(round(pf_avg_fake2real, 2)))
print("The avg of connections from fake news posters to real news posters"
      " on politifact: " + str(round(pf_avg_fake2real, 2)))
print("The avg of connections from fake news posters to fake news posters"
      " on politifact: " + str(round(pf_avg_fake2fake, 2)))


################################################################################
# TASK        : 5                                                              #
#                                                                              #
# OBJECTIVE   : Export user-user user connectivity data to csv for Gephi       #
#               analysis.                                                      #
#                                                                              #
################################################################################
# BUZZFEED
export_connectivity('Data/BuzzFeed/', buzzfeed_user_user, bf_real_posters_arr,
                    bf_fake_posters_arr)
# POLITIFACT
export_connectivity('Data/PolitiFact/', politifact_user_user,
                    pf_real_posters_arr, pf_fake_posters_arr)

