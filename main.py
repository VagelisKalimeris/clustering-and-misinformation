###############################################################################
# AUTHOR        : Evangelos Kalimeris                                         #
#                                                                             #
# COURSE NAME   : Complex Network Dynamics                                    #
#                                                                             #
# PROJECT NAME  : Clustering and Misinformation                               #
#                                                                             #
# FILE NAME     : main.py                                                     #
#                                                                             #
###############################################################################
from statistics import mean
import csv

# News ranges
BUZZFEED_REAL_RNG = range(1, 92)
BUZZFEED_FAKE_RNG = range(92, 183)
POLITIFACT_REAL_RNG = range(1, 121)
POLITIFACT_FAKE_RNG = range(121, 241)

# Files relating users with news
# Fields: news_id, user_id, times_posted
with open('Data/BuzzFeed/BuzzFeedNewsUser.txt', 'r') as file:
    buzzfeed_news_user = [str.rstrip().split('\t') for str in file.readlines()]
with open('Data/PolitiFact/PolitiFactNewsUser.txt', 'r') as file:
    politifact_news_user = [str.rstrip().split('\t') for str in file.readlines()]
# Open user-user files
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

"""First task - find the total amounts of users posting real/fake/both news -
also sum up each group's re-tweets"""
def get_posts_and_retweets(news_user, real_range, fake_range):
    real_posts_arr, fake_posts_arr, = [], []
    real_retweets_sum, fake_retweets_sum = 0, 0
    for line in news_user:
        if int(line[0]) in real_range:
            real_posts_arr.append(int(line[1]))
            real_retweets_sum += int(line[2])
        elif int(line[0]) in fake_range:
            fake_posts_arr.append(int(line[1]))
            fake_retweets_sum += int(line[2])
    return real_posts_arr, fake_posts_arr, real_retweets_sum, fake_retweets_sum


# BUZZFEED
bf_real_posts_arr, bf_fake_posts_arr, bf_real_retweets_sum, \
bf_fake_retweets_sum = get_posts_and_retweets(buzzfeed_news_user,
                                          BUZZFEED_REAL_RNG, BUZZFEED_FAKE_RNG)
bf_both_posters_arr = set(bf_real_posts_arr) & set(bf_fake_posts_arr)
bf_real_posters_arr = set(bf_real_posts_arr) - bf_both_posters_arr
bf_fake_posters_arr = set(bf_fake_posts_arr) - bf_both_posters_arr
bf_real_posters_sum, bf_fake_posters_sum = len(bf_real_posters_arr), \
                                           len(bf_fake_posters_arr)
bf_both_posters_sum = len(bf_both_posters_arr)

# POLITIFACT
pf_real_posts_arr, pf_fake_posts_arr,pf_real_retweets_sum, \
pf_fake_retweets_sum = get_posts_and_retweets(politifact_news_user,
                                      POLITIFACT_REAL_RNG, POLITIFACT_FAKE_RNG)
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


""""Second task - find the average of tweet/retweet rate for each list"""
# Tweet rates
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
# Re-tweet rates
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


""""Third task - find the average of friends for each list."""
# Helper function
def get_avg_and_max_links(arr, dir_arr, total):
    temp_sum, max_link = 0, 0
    for user in arr:
        curr_friends = dir_arr.count(user)
        temp_sum += curr_friends
        if curr_friends > max_link:
            max_link = curr_friends
    return temp_sum / total, max_link


# BUZZFEED
# Create Inlink and Outlink arrays
from_arr, to_arr = [int(x[0]) for x in buzzfeed_user_user], \
                   [int(x[1]) for x in buzzfeed_user_user]
# Real Outlinks
bf_real_avg_outlinks, bf_max_real_outlinks = \
    get_avg_and_max_links(bf_real_posters_arr, from_arr, bf_real_posters_sum)
# Real Inlinks
bf_real_avg_inlinks, bf_max_real_inlinks = \
    get_avg_and_max_links(bf_real_posters_arr, to_arr, bf_real_posters_sum)
# Fake Outlinks
bf_fake_avg_outlinks, bf_max_fake_outlinks = \
    get_avg_and_max_links(bf_fake_posters_arr, from_arr, bf_fake_posters_sum)
# Fake Inlinks
bf_fake_avg_inlinks, bf_max_fake_inlinks = \
    get_avg_and_max_links(bf_fake_posters_arr, to_arr, bf_fake_posters_sum)

# POLITIFACT
# Create Inlink and Outlink arrays
from_arr, to_arr = [int(x[0]) for x in politifact_user_user], \
                   [int(x[1]) for x in politifact_user_user]
# Real Outlinks
pf_real_avg_outlinks, pf_max_real_outlinks = \
    get_avg_and_max_links(pf_real_posters_arr, from_arr, pf_real_posters_sum)
# Real Inlinks
pf_real_avg_inlinks, pf_max_real_inlinks = \
    get_avg_and_max_links(pf_real_posters_arr, to_arr, pf_real_posters_sum)
# Fake Outlinks
pf_fake_avg_outlinks, pf_max_fake_outlinks = \
    get_avg_and_max_links(pf_fake_posters_arr, from_arr, pf_fake_posters_sum)
# Fake Inlinks
pf_fake_avg_inlinks, pf_max_fake_inlinks = \
    get_avg_and_max_links(pf_fake_posters_arr, to_arr, pf_fake_posters_sum)
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


"""Fourth task - Find connectivity between real and fake news spreaders"""
# Total users for both datasets
bf_total_users = bf_real_posters_sum + bf_fake_posters_sum - bf_both_posters_sum
pf_total_users = pf_real_posters_sum + pf_fake_posters_sum - pf_both_posters_sum


# Helper function
def get_avg_cross_group_links(user_user, real_posters_arr, fake_posters_arr,
                              real_users, fake_users=0):
    real2real, real2fake, fake2fake, fake2real = 0, 0, 0, 0
    for row in user_user:
        # Get real to real connections
        if int(row[0]) in real_posters_arr and int(row[1]) in real_posters_arr:
            real2real += 1
        # Get real to fake connections
        elif int(row[0]) in real_posters_arr and int(row[1]) in fake_posters_arr:
            real2fake += 1
        # Get fake to fake connections
        elif int(row[0]) in fake_posters_arr and int(row[1]) in fake_posters_arr:
            fake2fake += 1
        # Get fake to real connections
        elif int(row[0]) in fake_posters_arr and int(row[1]) in real_posters_arr:
            fake2real += 1
    return real2real / real_users, real2fake / real_users, \
           fake2fake / fake_users, fake2real / fake_users


# BUZZFEED
bf_avg_real2real, bf_avg_real2fake, bf_avg_fake2fake, bf_avg_fake2real = \
    get_avg_cross_group_links(buzzfeed_user_user, bf_real_posters_arr,
                  bf_fake_posters_arr, bf_real_posters_sum, bf_fake_posters_sum)
# POLITIFACT
pf_avg_real2real, pf_avg_real2fake, pf_avg_fake2fake, pf_avg_fake2real = \
    get_avg_cross_group_links(politifact_user_user, pf_real_posters_arr,
                  pf_fake_posters_arr, pf_real_posters_sum, pf_fake_posters_sum)
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


"""Fifth task - Export data for Gephi analysis"""
# Export user-user user connectivity data to csv for Gephi analysis
# Helper function
def export_connectivity(dir, user_user, real_posters_arr, fake_posters_arr):
    # Create output files
    rr_writer, rf_writer, ff_writer, fr_writer = \
        csv.writer(open(dir + 'realreal.csv', 'w')), \
        csv.writer(open(dir + 'realfake.csv', 'w')),\
        csv.writer(open(dir + 'fakefake.csv', 'w')), \
        csv.writer(open(dir + 'fakereal.csv', 'w'))
    # Write file headers
    rr_writer.writerow(['Source', 'Target'])
    rf_writer.writerow(['Source', 'Target'])
    ff_writer.writerow(['Source', 'Target'])
    fr_writer.writerow(['Source', 'Target'])
    # Add edges
    for row in user_user:
        # Write real to real connections
        if int(row[0]) in real_posters_arr and int(row[1]) in \
                                                real_posters_arr:
            rr_writer.writerow(row)
        # Get real to fake connections
        elif int(row[0]) in real_posters_arr and int(row[1]) in \
                                                fake_posters_arr:
            rf_writer.writerow(row)
        # Get fake to fake connections
        elif int(row[0]) in fake_posters_arr and int(row[1]) in \
                                                fake_posters_arr:
            ff_writer.writerow(row)
        # Get fake to real connections
        elif int(row[0]) in fake_posters_arr and int(row[1]) in \
                                                real_posters_arr:
            fr_writer.writerow(row)


# BUZZFEED
export_connectivity('Data/BuzzFeed/', buzzfeed_user_user, bf_real_posters_arr,
                    bf_fake_posters_arr)
# POLITIFACT
export_connectivity('Data/PolitiFact/', politifact_user_user,
                    pf_real_posters_arr, pf_fake_posters_arr)

