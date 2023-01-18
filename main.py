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


################################################################################
#                                 NEWS RANGES                                  #
################################################################################
BF_REAL_RANGE, BF_FAKE_RANGE, PF_REAL_RANGE, PF_FAKE_RANGE = \
    range(1, 92), range(92, 183), range(1, 121), range(121, 241)


################################################################################
#                             DEAL WITH FILE I/O                               #
################################################################################
# Open files relating users with news
# todo: Close files
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
pf_real_posts_arr, pf_fake_posts_arr, pf_real_retweets_sum, \
pf_fake_retweets_sum = get_posts_and_retweets(politifact_news_user,
                                              PF_REAL_RANGE, PF_FAKE_RANGE)
pf_both_posters_arr = set(pf_real_posts_arr) & set(pf_fake_posts_arr)
pf_real_posters_arr = set(pf_real_posts_arr) - pf_both_posters_arr
pf_fake_posters_arr = set(pf_fake_posts_arr) - pf_both_posters_arr
pf_real_posters_sum, pf_fake_posters_sum = len(pf_real_posters_arr), \
                                           len(pf_fake_posters_arr)
pf_both_posters_sum = len(pf_both_posters_arr)

bf_sum_list, pf_sum_list = \
    (bf_real_posters_sum, bf_fake_posters_sum, bf_both_posters_sum), \
    (pf_real_posters_sum, pf_fake_posters_sum, pf_both_posters_sum)

# Print info to console
print('Task 1:')
for feed, sum in zip(('BuzzFeed', 'PolitiFact'), (bf_sum_list, pf_sum_list)):
    for news, i in zip(('real', 'fake', 'both real and fake'), range(3)):
        print('\t', str(sum[i]), 'total users posted', news, 'news on', feed)


################################################################################
# TASK        : 2                                                              #
#                                                                              #
# OBJECTIVE   : Find the average of tweet/re-tweet rate for each list.         #
#                                                                              #
################################################################################
# BUZZFEED
bf_real_tweets_avg = mean(bf_real_posts_arr.count(ID) for ID in
                          bf_real_posters_arr)
bf_fake_tweets_avg = mean(bf_fake_posts_arr.count(ID) for ID in
                            bf_fake_posters_arr)

# POLITIFACT
pf_real_tweets_avg = mean(pf_real_posts_arr.count(ID) for ID in
                            pf_real_posters_arr)
pf_fake_tweets_avg = mean(pf_fake_posts_arr.count(ID) for ID in
                            pf_fake_posters_arr)

# BUZZFEED
bf_real_retweets_avg = bf_real_retweets_sum / len(bf_real_posts_arr)
bf_fake_retweets_avg = bf_fake_retweets_sum / len(bf_fake_posts_arr)

# POLITIFACT
pf_real_retweets_avg = pf_real_retweets_sum / len(pf_real_posts_arr)
pf_fake_retweets_avg = pf_fake_retweets_sum / len(pf_fake_posts_arr)

bf_avg_list, pf_avg_list = ((bf_real_tweets_avg, bf_fake_tweets_avg), (
    bf_real_retweets_avg, bf_fake_retweets_avg)), ((pf_real_tweets_avg,
    pf_fake_tweets_avg), (pf_real_retweets_avg, pf_fake_retweets_avg))

# Print info to console
print('\nTask 2:')
for feed, avgs in zip(('BuzzFeed', 'PolitiFact'), (bf_avg_list, pf_avg_list)):
    for rate, i in zip(('tweet', 're-tweet'), range(2)):
        for news, j in zip(('real', 'fake'), range(2)):
            print('\tAverage', rate, 'rate for', feed, news,'news:',
                  str(round(avgs[i][j], 2)))


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

bf_avg_max_list, pf_avg_max_list = (((bf_real_avg_outlinks, bf_max_real_outlinks),
    (bf_real_avg_inlinks, bf_max_real_inlinks)), ((bf_fake_avg_outlinks,
    bf_max_fake_outlinks), (bf_fake_avg_inlinks, bf_max_fake_inlinks))), (((
    pf_real_avg_outlinks, pf_max_real_outlinks), (pf_real_avg_inlinks,
    pf_max_real_inlinks)), ((pf_fake_avg_outlinks, pf_max_fake_outlinks), (
    pf_fake_avg_inlinks, pf_max_fake_inlinks)))

# Print info to console
print('\nTask 3:')
for feed, avgs in zip(('BuzzFeed', 'PolitiFact'), (bf_avg_max_list, pf_avg_max_list)):
    for news, i in zip(('real', 'fake'), range(2)):
        for linktype, j in zip(('following', 'followers'), range(2)):
            print('\tAverage', feed, 'users', linktype, 'of users that posted', news,
                  'news:', str(round(avgs[i][j][0], 2)), '[group max:',
                  str(round(avgs[i][j][1], 2)), ']')


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

bf_avg_conn_list, pf_avg_conn_list = ((bf_avg_real2real, bf_avg_real2fake),
    (bf_avg_fake2real, bf_avg_fake2fake)), ((pf_avg_real2real, pf_avg_real2fake),
                                            (pf_avg_fake2real, pf_avg_fake2fake))

# Print info to console
print('\nTask 4:')
for feed, avgs in zip(('BuzzFeed', 'PolitiFact'), (bf_avg_conn_list, pf_avg_conn_list)):
    for news_from, i in zip(('real', 'fake'), range(2)):
        for news_to, j in zip(('real', 'fake'), range(2)):
            print('\tAverage of connections from', news_from, 'news posters to',
                  news_to, 'news posters on', feed, ':', str(round(avgs[i][j], 2)))


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

print('\nTask 5:\n\tExport DONE')

