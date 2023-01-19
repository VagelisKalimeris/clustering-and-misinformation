###############################################################################
# AUTHOR        : Evangelos Kalimeris                                         #
#                                                                             #
# PROJECT NAME  : Clustering and Misinformation                               #
#                                                                             #
# FILE NAME     : main.py                                                     #
#                                                                             #
###############################################################################
from statistics import mean
from util_funcs import get_posts_and_retweets, get_avg_and_max_links, \
    get_avg_cross_group_links, export_connectivity, print_task_1_results, \
    print_task_2_results, print_task_3_results, print_task_4_results, \
    export_data_to_csv_files, get_data_from_files


################################################################################
#                                 NEWS RANGES                                  #
################################################################################
BF_REAL_RANGE, BF_FAKE_RANGE, PF_REAL_RANGE, PF_FAKE_RANGE = \
    range(1, 92), range(92, 183), range(1, 121), range(121, 241)


################################################################################
#                             DEAL WITH FILE I/O                               #
################################################################################
# Open files relating users to news and users to users
buzzfeed_news_user, politifact_news_user, buzzfeed_user_user, \
    politifact_user_user = get_data_from_files((
    'Data/BuzzFeed/BuzzFeedNewsUser.txt',
    'Data/PolitiFact/PolitiFactNewsUser.txt',
    'Data/BuzzFeed/BuzzFeedUserUser.txt',
    'Data/PolitiFact/PolitiFactUserUser.txt'))

# Export user-user data from created lists, to csv files, for Gephi analysis
export_data_to_csv_files((buzzfeed_user_user, politifact_user_user),
    ('Data/BuzzFeed/BuzzFeedUserUser.csv',
    'Data/PolitiFact/PolitiFactUserUser.csv'))


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

# Print task results to console
print('Task 1:')
print_task_1_results((bf_real_posters_sum, bf_fake_posters_sum,
    bf_both_posters_sum), (pf_real_posters_sum, pf_fake_posters_sum,
    pf_both_posters_sum))


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

# Print task results to console
print('\nTask 2:')
print_task_2_results(((bf_real_tweets_avg, bf_fake_tweets_avg), (
    bf_real_retweets_avg, bf_fake_retweets_avg)), ((pf_real_tweets_avg,
    pf_fake_tweets_avg), (pf_real_retweets_avg, pf_fake_retweets_avg)))


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

# Print task results to console
print('\nTask 3:')
print_task_3_results((((bf_real_avg_outlinks, bf_max_real_outlinks),
    (bf_real_avg_inlinks, bf_max_real_inlinks)), ((bf_fake_avg_outlinks,
    bf_max_fake_outlinks), (bf_fake_avg_inlinks, bf_max_fake_inlinks))), (((
    pf_real_avg_outlinks, pf_max_real_outlinks), (pf_real_avg_inlinks,
    pf_max_real_inlinks)), ((pf_fake_avg_outlinks, pf_max_fake_outlinks), (
    pf_fake_avg_inlinks, pf_max_fake_inlinks))))


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

# Print task results to console
print('\nTask 4:')
print_task_4_results(((bf_avg_real2real, bf_avg_real2fake), (bf_avg_fake2real,
    bf_avg_fake2fake)), ((pf_avg_real2real, pf_avg_real2fake),
    (pf_avg_fake2real, pf_avg_fake2fake)))


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

# Print task results to console
print('\nTask 5:\n\tExport DONE')
