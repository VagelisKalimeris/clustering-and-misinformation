###############################################################################
# AUTHOR        : Evangelos Kalimeris                                         #
#                                                                             #
# PROJECT NAME  : Clustering and Misinformation                               #
#                                                                             #
# FILE NAME     : util_funcs.py                                               #
#                                                                             #
# OBJECTIVE     : Provides utility functions used by the main script          #
#                                                                             #
###############################################################################
import csv


###############################################################################
#                        CALCULATION FUNCTIONS SECTION                        #
###############################################################################
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


###############################################################################
#                          FILE I/O FUNCTIONS SECTION                         #
###############################################################################
def get_data_from_files(files_list):
    result_lists = []
    for file in files_list:
        with open(file, 'r') as file:
            result_lists.append([str.rstrip().split('\t') for str in file.readlines()])
    return result_lists


def export_data_to_csv_files(users_lists, filenames_list):
    for users_list, file in zip(users_lists, filenames_list):
        with open(file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Source', 'Target'])
            for line in users_list:
                writer.writerow(line)


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


###############################################################################
#                          PRINT FUNCTIONS SECTION                         #
###############################################################################
def print_task_1_results(bf_sum_list, pf_sum_list):
    for feed, sum in zip(('BuzzFeed', 'PolitiFact'), (bf_sum_list, pf_sum_list)):
        for news, i in zip(('real', 'fake', 'both real and fake'), range(3)):
            print('\t', str(sum[i]), 'total users posted', news, 'news on', feed)


def print_task_2_results(bf_avg_list, pf_avg_list):
    for feed, avgs in zip(('BuzzFeed', 'PolitiFact'), (bf_avg_list, pf_avg_list)):
        for rate, i in zip(('tweet', 're-tweet'), range(2)):
            for news, j in zip(('real', 'fake'), range(2)):
                print('\tAverage', rate, 'rate for', feed, news, 'news:',
                      str(round(avgs[i][j], 2)))


def print_task_3_results(bf_avg_max_list, pf_avg_max_list):
    for feed, avgs in zip(('BuzzFeed', 'PolitiFact'), (bf_avg_max_list, pf_avg_max_list)):
        for news, i in zip(('real', 'fake'), range(2)):
            for linktype, j in zip(('following', 'followers'), range(2)):
                print('\tAverage', feed, 'users', linktype, 'of users that posted', news,
                      'news:', str(round(avgs[i][j][0], 2)), '[group max:',
                      str(round(avgs[i][j][1], 2)), ']')


def print_task_4_results(bf_avg_conn_list, pf_avg_conn_list):
    for feed, avgs in zip(('BuzzFeed', 'PolitiFact'), (bf_avg_conn_list, pf_avg_conn_list)):
        for news_from, i in zip(('real', 'fake'), range(2)):
            for news_to, j in zip(('real', 'fake'), range(2)):
                print('\tAverage of connections from', news_from, 'news posters to',
                      news_to, 'news posters on', feed, ':', str(round(avgs[i][j], 2)))