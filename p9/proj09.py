################################################################################
# Computer Project 9
#
# This program answers a few questions about a given file of twitter data.
# 1. What are the most frequently tweeted hashtags?
#
# 2. Which user tweeted some hashtag more frequently than any other user tweeted
#    any hashtag? What three users each have the most tweets for some (possibly
#    three different) hashtag(s)?
#
# 3. How often did two users tweet the same hashtag during the same month of the
#    year?
#
# To answer these questions the program implements following tasks.
# Organize data from the twitter file into an easy to use python data structure.
# [username_str, month_int, hashtags_from_a_tweet_list]
# Question 1:
#     For each tweet in the data,
#         For each hashtag in tweet,
#             If we've seen the hashtag before,
#                 Increment the hashtag's count.
#             Else,
#                 Initialize the hashtag's count to 1.
#     The set of hashtag count pairs answers the question.
# Question 2:
#     Get the set of all usernames from the dataset.
#     For each user,
#         For each hashtag,
#             Count the number of times user tweeted hashtag.
#             Store the count along with the hashtag and username in a list.
#             list.append( (count, hashtag, username) )
#     Sort the list by counts.
#     The top three elements of the list answer the question.
# Question 3:
#     Prompt for two users to compare, user1 and user2.
#     For each month from 1 to 12,
#         Get a set of hashtags tweeted by user1 and by user2 during the month.
#         Append the intersection of the two sets to a list.
#     The list gives the answer to the question.
################################################################################

import string
import calendar
import pylab

MONTH_NAMES = [calendar.month_name[month] for month in range(1, 12+1)]

def open_file():
    '''Prompts for a file name and opens the file for reading if it exists.
    If the file does not exists, print an error and retry.
    Returns: file pointer.'''

    while True:
        try:
            filename = input('Input a filename: ')
            # filename = 'twitterdata.csv'
            # filename = 'smalldata.csv'
            fp = open(filename)
            break
        except FileNotFoundError:
            print('Error in input filename. Please try again.')
    print()
    return fp

def validate_hashtag(hashtag: str) -> bool:
    '''Returns True if the hashtag is a valid Twitter hashtag.'''
    if hashtag == '':
        return False
    if hashtag[0] != '#':
        return False
    if len(hashtag) == 1:
        return False
    if len(hashtag) == 2 and hashtag[1].isdigit():
        return False
    for c in hashtag[1:]:
        # Underscores are allowed
        if c == '_':
            continue
        elif c in string.punctuation:
            return False
    return True

def get_hashtags(tweet: str) -> list:
    '''Returns the valid hashtags in the tweet.
    Returns: a list of strings'''
    hashtags = []
    base = tweet.find('#')
    while base != -1:
        end = tweet.find(' ', base)
        # if there are no spaces after base, then there are no valid hashtags
        # after base. But we should consider hashtags at the end of the tweet.
        # So if there is no space after the hashtag, take everything until the
        # end of the tweet line.
        if end == -1:
            end = None
        hashtag = tweet[base:end]
        if validate_hashtag(hashtag):
            hashtags.append(hashtag)
        # consider the case tweet='##MSU' where the valid hashtag is '#MSU'
        base = tweet.find('#', base+1)
    return hashtags

def read_data(fp) -> list:
    '''Parse the data file into a python list of lists.
    Each line of the datafile is in the format
        'username,month,tweet...'
    and is converted into the list
        [username_str, month_int, valid_hashtags_in_tweet]
    Throws exceptions and prints errors if the file is not in the expected
    format.'''
    data = []
    for line in fp:
        comma1 = line.find(',')
        comma2 = line.find(',', comma1+1)

        try:
            username = line[:comma1]
        except IndexError:
            print("IndexError error parsing username from file")
            username = ''

        try:
            month = int(line[comma1+1:comma2])
        except ValueError:
            print("ValueError error parsing month from file")
            month = 0
        except IndexError:
            print("IndexError error parsing month from file")
            month = 0

        try:
            tweet = line[comma2+1:].strip()
        except IndexError:
            print("IndexError error parsing tweet from file")
            tweet = ''

        hashtags = get_hashtags(tweet)
        data.append([username, month, hashtags])

    return data

def get_histogram_tag_count_for_users(data: list, usernames: list) -> dict:
    '''Returns a hashtag/count map for the hashtags tweeted by any of the users
    in usernames.'''
    histogram = dict()
    for data_point in data:
        username = data_point[0]
        # Filter hashtags to count based on given usernames
        if username in usernames:
            hashtags = data_point[2]
            for hashtag in hashtags:
                if hashtag in histogram:
                    histogram[hashtag] += 1
                else:
                    histogram[hashtag] = 1
    return histogram

def get_tags_by_month_for_users(data: list, usernames: list) -> list:
    '''Returns a list of (month_int,hashtag_set) tuples for the hashtags tweeted
    in each month by the users in usernames.'''
    month_tags_list = [(month, set()) for month in range(1, 12+1)]
    for data_point in data:
        username = data_point[0]
        if username in usernames:
            month = data_point[1]
            hashtags = data_point[2]
            for hashtag in hashtags:
                # Convert month to index
                month_tags_list[month - 1][1].add(hashtag)
    return month_tags_list

def get_user_names(data: list) -> list:
    '''Returns a list of username strings.'''
    username_set = set()
    for data_point in data:
        username = data_point[0]
        username_set.add(username)
    return sorted(username_set)

def three_most_common_hashtags_combined(data: list, usernames: list) -> list:
    '''Returns the list of the three most frequently tweeted hashtags from
    data.'''
    hashtag_histogram_dict = get_histogram_tag_count_for_users(data,usernames)
    # sort based on counts
    count_hashtag_list = []
    for hashtag, count in hashtag_histogram_dict.items():
        count_hashtag_list.append((count, hashtag))
    count_hashtag_list.sort(reverse=True)
    return count_hashtag_list[:3]

def three_most_common_hashtags_individuals(data: list, usernames: list) -> list:
    '''Returns the three (count, hashtag, username) tuples where count is
    largest. count is the number of times that username tweeted hashtag.

    Returning the said value answeres the following question.
    Which user tweeted some hashtag more frequently than any other user tweeted
    any hashtag? What three users each have the most tweets for some (possibly
    three different) hashtag?'''
    count_tag_user_list = []
    for user in usernames:
        tag_counts = get_histogram_tag_count_for_users(data, [user]).items()
        # Add user name to (count, hashtag) datapoint
        for tag,count in tag_counts:
            count_tag_user_list.append((count, tag, user))
    count_tag_user_list.sort(reverse=True)
    return count_tag_user_list[:3]

def similarity(data: list, user1: str, user2: str) -> list:
    '''Compares the tweets made by user1 and user2 in each month of the year.
    Returns a list of (month,hashtag_set) tuples where hashtag_set is the set of
    hashtags that were tweeted by both user1 and user2 during month.'''
    user1_tags = get_tags_by_month_for_users(data, [user1])
    user2_tags = get_tags_by_month_for_users(data, [user2])
    common_tags = []
    # For each month
    for month in range(12):
        # Get the tags for user during the month as a set
        user1_set = user1_tags[month][1]
        user2_set = user2_tags[month][1]

        # Find the tags that both users tweeted in month
        tup = (month+1, user1_set.intersection(user2_set))
        common_tags.append(tup)

    return common_tags

def plot_similarity(x: list, y: list, name1: str, name2: str):
    '''Plot y vs. x with name1 and name2 in the title.'''

    pylab.plot(x, y)
    pylab.xticks(x, MONTH_NAMES, rotation=45, ha='right')
    pylab.ylabel('Hashtag Similarity')
    pylab.title('Twitter Similarity Between ' + name1 + ' and ' + name2)
    pylab.tight_layout()
    pylab.show()
    # the next line is simply to illustrate how to save the plot
    # leave it commented out in the version you submit
    #pylab.savefig("plot.png")

def main():
    fp = open_file()
    data = read_data(fp)
    usernames = get_user_names(data)

    # Calculate the top three hashtags combined for all users
    top_three_hashtags = three_most_common_hashtags_combined(data, usernames)
    print("Top Three Hashtags Combined")
    print("{:>6s} {:20s}".format("Count", "Hashtag"))
    for count, hashtag in top_three_hashtags:
        print("{:6d} {:20s}".format(count, hashtag))
    print()

    # Calculate the top three hashtags individually for all users
    top_three_hashtags = three_most_common_hashtags_individuals(data, usernames)
    print("Top Three Hashtags by Individual")
    print("{:>6s} {:20s} {:20s}".format("Count", "Hashtag", "User"))
    for count, hashtag, user in top_three_hashtags:
        print("{:6d} {:20s} {:20s}".format(count, hashtag, user))
    print()

    # Prompt for two user names from username list
    usernames_str = ', '.join(usernames)
    print("Usernames: ", usernames_str)
    users_to_compare = []
    while True:
        users_str=input("Input two user names from the list, comma separated: ")

        users_to_compare = users_str.strip().split(',')
        for i, _ in enumerate(users_to_compare):
            users_to_compare[i] = users_to_compare[i].strip()

        if len(users_to_compare) != 2:
            print("Error in user names.  Please try again")
        elif (users_to_compare[0] not in usernames)\
          or (users_to_compare[1] not in usernames):
            print("Error in user names.  Please try again")
        else:
            break
    print()

    # Calculate similarity for the two users
    similarities = similarity(data, users_to_compare[0], users_to_compare[1])
    print("Similarities for "+users_to_compare[0]+" and "+users_to_compare[1])
    print("{:12s}{:6s}".format("Month", "Count"))
    for month, tags_in_common in similarities:
        print("{:12s}{:<6d}".format(MONTH_NAMES[month-1], len(tags_in_common)))
    print()

    # Prompt to plot
    choice = input("Do you want to plot (yes/no)?: ")
    if choice.lower() == 'yes':
        x_list = [i for i in range(1, 12+1)]
        y_list = [len(tags_in_common) for _, tags_in_common in similarities]
        plot_similarity(x_list, y_list, users_to_compare[0],users_to_compare[1])

if __name__ == '__main__':
    main()
