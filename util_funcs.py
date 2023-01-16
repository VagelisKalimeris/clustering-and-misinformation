###############################################################################
# AUTHOR        : Evangelos Kalimeris                                         #
#                                                                             #
# PROJECT NAME  : Clustering and Misinformation                               #
#                                                                             #
# FILE NAME     : util_funcs.py                                               #
#                                                                             #
###############################################################################
import csv

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


def get_avg_and_max_links(arr, dir_arr, total):
    temp_sum, max_link = 0, 0
    for user in arr:
        curr_friends = dir_arr.count(user)
        temp_sum += curr_friends
        if curr_friends > max_link:
            max_link = curr_friends
    return temp_sum / total, max_link


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