###########################################################
# Computer Project #6
#
# This program parses a table, loaded from file, containing water usage data for
# counties accross America.
# The program prompts the user for a state abbreviation for the state that the
# user would like water information for.
# If the user enters the string 'all', then the program outputs information for
# counties in all states. If the user enters the string 'quit', then the program
# exits.
# The program then outputs the total water usage and the water used per person
# for counties from the user's selected state.
# The program optionally allows the user to plot the data using a pie chart.
#
###########################################################
import pylab

def open_file():
    '''Prompt for file name, open file, return file pointer'''
    while True:
        try:
            filename = input("Input a file name: ")
            fp = open(filename)
            break
        except FileNotFoundError:
            print("Unable to open file. Please try again.")
    return fp


def read_file(fp):
    '''
    Collect information contained in a table in the file pointed to by fp.
    Each row produces a tuple in the output list.
    If a cell from the table is empty just assume the value is zero.
    Returns a list of tuples.
    '''
    # Skip the table's header line
    fp.readline()

    ret_list = []
    for line in fp:
        line = line.split(',')

        state = line[0]
        county = line[2]

        # Convert from thousands unit to single unit
        population = round(float(line[6] or 0)*1000, 0)

        # Water Usages
        fresh = float(line[114] or 0)
        salt = float(line[115] or 0)
        public = float(line[18] or 0)
        domestic = float(line[26] or 0)
        industrial = float(line[35] or 0)
        irrigation = float(line[45] or 0)
        livestock = float(line[59] or 0)

        tup = (state, county, population, fresh, salt, public, domestic, \
            industrial, irrigation, livestock)
        ret_list.append(tup)

    return ret_list


def compute_usage(state_list):
    '''
    Compute water usage for the counties in state_list.
    state_list is a list of tuples. Each tuple contains the state abbreviation,
    the county name, population, fresh water usage, and salt water usage.
    Returns a tuple of information about each county's water usage.
    '''
    ret_list = []
    for county_info in state_list:
        county_name = county_info[1]
        county_population = county_info[2]
        total_water_usage = county_info[3] + county_info[4]
        fresh_per_person = county_info[3] / county_population
        tup = (county_name, county_population, total_water_usage, \
            fresh_per_person)
        ret_list.append(tup)

    return ret_list


def compute_county_usage(county):
    '''
    Compute water usage for the county.
    County is a tuple of information for the county.
    Returns a tuple of information about the county's water usage.
    '''
    # County expects a list of tuples and returns a list tuples.
    # Wrap the function so that it operates on single tuple.
    return compute_usage([county])[0]


def extract_data(data_list, state):
    '''
    Make a list of tuples from data_list that contain information for state.
    state is a string representation of the desired state's abbreviation.
    Each tuple contains a state abbreviation in the first index.
    Returns a sub-list of data_list.
    '''
    return [x for x in data_list if state == x[0]]


def display_data(state_list, state_requested):
    '''Plot the data for state_requested contained in state_list.'''

    # Print table's title and header
    title = '{:^88s}'.format("Water Usage in " + state_requested + " for 2010")
    header = '{:22s} {:>22s} {:>22s} {:>22s}'.format("County", \
            "Population", "Total (Mgal/day)", "Per Person (Mgal/person)")
    print(title)
    print(header)

    # Get the data we want to display
    county_list = []
    if state_requested == 'ALL':
        county_list = state_list
    else:
        county_list = extract_data(state_list, state_requested)

    # Print table's data
    for county in county_list:
        county_water_usage = compute_county_usage(county)

        row_fmt = '{:22s} {:>22,.0f} {:>22.2f} {:>22.4f}'
        count_name_str = county_water_usage[0]
        county_population_flt = county_water_usage[1]
        total_water_usage_flt = county_water_usage[2]
        per_person_flt = county_water_usage[3]

        print(row_fmt.format(count_name_str, county_population_flt, \
            total_water_usage_flt, per_person_flt))


def plot_water_usage(some_list, plt_title):
    '''
    Creates a list "y" containing the water usage in Mgal/d of all counties.
    Y should have a length of 5. The list "y" is used to create a pie chart
    displaying the water distribution of the five groups.

    This function is provided by the project.
    '''
    # accumulate public, domestic, industrial, irrigation, and livestock data
    y = [0]*5

    for item in some_list:
        y[0] += item[5]
        y[1] += item[6]
        y[2] += item[7]
        y[3] += item[8]
        y[4] += item[9]

    # compute the percentages.
    total = sum(y)
    if total == 0.:
        total = 1.
    y = [round(x/total * 100, 2) for x in y]

    color_list = ['b','g','r','c','m']
    pylab.title(plt_title)
    USERS = ("Public", "Domestic", "Industrial", "Irrigation", "Livestock")
    pylab.pie(y, labels=USERS, colors=color_list)
    pylab.show()
    #pylab.savefig("plot.png")  # uncomment to save plot to a file


def get_user_input():
    '''
    Prompt for which state to get data for.
    Ask if the user wants data for all states.
    Ask if the user would like to quit.
    '''

    STATES = ('AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY')
    user_input = ''
    while True:
        user_input = input("\nEnter state code or 'all' or 'quit': ")
        user_input = user_input.upper()
        valid_input = user_input in STATES
        valid_input = valid_input or user_input in ['ALL', 'QUIT']
        if valid_input:
            break
        else:
            print("Error in state code.  Please try again.")

    return user_input


def main():
    print("Water Usage Data from the US and its States and Territories.\n")

    fp = open_file()
    data_list = read_file(fp)
    fp.close()

    while True:
        # Gets state code (for one or all states) or quit
        user_input = get_user_input()
        if user_input == 'QUIT':
            break

        display_data(data_list, user_input)

        answer = input("\nDo you want to plot? ").lower()
        if answer == 'yes':
            state_requested = user_input
            title = '{:^88s}'.format("Water Usage in " + state_requested + \
                " for 2010")

            county_list = extract_data(data_list, state_requested)
            plot_water_usage(county_list, title)


if __name__ == "__main__":
    main()
