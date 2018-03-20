################################################################################
# Computer Project 8
#
# Parses data about tropical storms from a file provided by the user.
# Allows the user to display and plot the data.
#
# Given the data file, the program builds a map of maps that contains
# information for the hurricanes. Intuitively, a year is mapped to the
# hurricanes that occured during the year and each hurricane is mapped to a list
# of data points that describe the hurricane.
#
# The map of maps, call it D, is a dictionary that contains dictionaries for
# values. D's keys are each a year string. The value for a key in D is another
# dictionary, Dk, whose keys are each a hurricane name string. The value for a
# key in Dk is a list of data point tuples that describe the hurricane.
# D looks like this
# {
#   '2000': {
#     'Earl': [ data point tuples ]
#     'Darla': [ data point tuples ]
#   }
#   '2001': {
#     'Johnson': [ data point tuples ]
#     ...
#   }
#   ...
# }
#
# To display hurricane data for a year we'll use information from the dictionary
# D[year]. For each hurricane in D[year] we display the hurricane's name,
# maximum attained wind speed, the coordiantes and date that the maximum wind
# speed was recorded and the hurricane's name.
#
# If the user wants to display a graphical plot for the year, then a list is
# built for each hurricane attribute in {name, max wind speed, path coordinates}
# The name list is alphabetically sorted. The ith hurricane's name, max wind
# speed and path coordinates are all found in name[i], max_wind_speed[i] and
# path_coordiantes[i].
# These lists are sent to the plot function which then creates the plots.
#
################################################################################
import pylab as py
from operator import itemgetter

def open_file():
    '''Prompts for a file name and opens the file for reading if it exists.
    If the file does not exists, print an error and retry.
    Returns: file pointer.'''

    while True:
        try:
            filename = input('Input a file name: ')
            fp = open(filename)
            break
        except:
            print('Unable to open file. Please try again.')
    return fp

def update_dictionary(dictionary, year:str, hurricane_name:str, data:tuple):
    '''Adds the hurricane and its data to the dictionary[year] dictionary.
    year: the year the hurricane occured in (string)
    hurricane_name: the name of the hurricane (string)
    data: a description of the hurricane (tuple)'''

    if year not in dictionary:
        dictionary[year] = dict()
    if hurricane_name not in dictionary[year]:
        dictionary[year][hurricane_name] = []

    dictionary[year][hurricane_name].append(data)

def create_dictionary(fp):
    '''Creates a map of maps from data contained in the file pointed at by fp.
    Maps years to hurricanes that occured in year. Each hurricane in a year is
    mapped to a list of data about the hurricane. Returns the map of maps.'''

    di = dict()
    for line in fp:
        data = line.split()

        year = data[0]
        hurricane_name = data[1]
        date = data[5]

        try:
            lat = float(data[3])
        except:
            lat = 0.

        try:
            lon = float(data[4])
        except:
            lon = 0.

        try:
            wind = float(data[6])
        except:
            wind = 0.

        try:
            pressure = float(data[7])
        except:
            pressure = 0.

        tup = (lat, lon, date, wind, pressure)
        update_dictionary(di, year, hurricane_name, tup)

    return di

def display_table(dictionary, year : str):
    '''Displays information for each hurricane that occurred during the year.
    year: the year to display hurricane data for (string)'''

    # Print headers
    print('{:^70s}'.format('Peak Wind Speed for the Hurricanes in ' + year))
    fmt_str = '{:15s}{:>15s}{:>20s}{:>15s}'
    print(fmt_str.format('Name', 'Coordinates', 'Wind Speed (knots)', 'Date'))
    names = sorted(dictionary[year].keys())

    # For indexing into data point tuples contained in dic[year][hurricane][i]
    LAT_INDX = 0
    LON_INDX = 1
    DATE_INDX = 2
    SPEED_INDX = 3
    PRESSURE_INDX = 4
    def getter(c):
        return (c[SPEED_INDX], c[LAT_INDX], c[LON_INDX], c[DATE_INDX])

    # Use data points with max speed and latitude
    fmt_str = '{:15s}( {:.2f},{:.2f}){:>20.2f}{:>15s}'
    for hurricane in names:
        data = dictionary[year][hurricane]
        data = sorted(data, key=getter)
        # data point with maximum values is at end
        data_point = data[-1]
        speed, lat, lon, date = getter(data_point)

        print(fmt_str.format(hurricane, lat, lon, speed, date))

def get_years(dictionary):
    '''Returns: the range of years in dictionary.keys()'''

    years = dictionary.keys()
    return (min(years), max(years))

def prepare_plot(dictionary, year : str):
    '''Creates everything that is required for plotting. Creates a list of
    names, a list of paths, and a list of max speeds.
    year: the year of hurricanes to prepare the plot for (string)
    Returns: tuple containing the created lists'''

    year_dict = dictionary[year]
    names = sorted(year_dict.keys())
    LAT_INDX = 0
    LON_INDX = 1
    SPEED_INDX = 3
    def getter(c):
        return (c[SPEED_INDX], c[LAT_INDX], c[LON_INDX])

    # Create a list of paths. Each path is a list of coordinates.
    paths = []
    # Create list of max speeds
    max_speeds = []
    for hurricane in names:
        data_points = year_dict[hurricane]
        # data_points = sorted(data_points, key=getter)

        path = []
        for data in data_points:
            coord = (data[LAT_INDX], data[LON_INDX])
            path.append(coord)
        paths.append(path)

        max_speeds.append(max(data_points, key=getter)[SPEED_INDX])

    return (names, paths, max_speeds)

def plot_map(year:str, num_hurricanes:int, names:list, coordinates:list):
    '''Plots the map of hurricane paths.
    names: list of hurricane name strings (list)
    year: the year that the hurricanes occured in (string)
    num_hurricanes: number of paths on the plot (int)
    The ith hurricane's name is in names[i] and the ith hurricane's path is in
    coordinates[i].'''

    # The the RGB list of the background image
    img = py.imread('world-map.jpg')

    # Set the max values for the latitude and longitude of the map
    max_longitude, max_latitude = 180, 90

    # Set the background image on the plot
    py.imshow(img,extent=[-max_longitude,max_longitude,\
                          -max_latitude,max_latitude])

    # Set the corners of the map to cover the Atlantic Region
    xshift = (50,190)
    yshift = (90,30)

    # Show the atlantic ocean region
    py.xlim((-max_longitude+xshift[0],max_longitude-xshift[1]))
    py.ylim((-max_latitude+yshift[0],max_latitude-yshift[1]))

    # Generate the colormap and select the colors for each hurricane
    cmap = py.get_cmap('gnuplot')
    colors = [cmap(i/num_hurricanes) for i in range(num_hurricanes)]


    # plot each hurricane's trajectory
    for i,key in enumerate(names):
        lat = [ lat for lat,lon in coordinates[i] ]
        lon = [ lon for lat,lon in coordinates[i] ]
        py.plot(lon,lat,color=colors[i],label=key)


     # Set the legend at the bottom of the plot
    py.legend(bbox_to_anchor=(0.,-0.5, 1., 0.102),loc=0, ncol=3, mode='expand',\
              borderaxespad=0., fontsize=10)

    # Set the labels and titles of the plot
    py.xlabel('Longitude (degrees)')
    py.ylabel('Latitude (degrees)')
    py.title('Hurricane Trajectories for {}'.format(year))
    py.show() # show the full map

def plot_wind_chart(year:str, num_hurricanes:int, names:list, max_speed:list):
    '''Shows a 2d plot where names is the x coord and max_speed is the y coord.
    names: hurricane name strings (list)
    year: the year that the hurricanes occured in (string)
    max_speed: the max speed of each hurricane (list)
    num_hurricanes: number of points on the plot (int)
    The ith hurricanes name is in names[i] and the ith hurricane's max_speed is
    in max_speed[i].'''

    # Set the value of the category
    cat_limit = [ [v for i in range(num_hurricanes)]
                 for v in [64,83,96,113,137] ]


    # Colors for the category plots
    COLORS = ['g','b','y','m','r']

    # Plot the Wind Speed of Hurricane
    for i in range(5):
        py.plot(range(num_hurricanes),cat_limit[i], COLORS[i],
                label='category-{:d}'.format(i+1))

    # Set the legend for the categories
    py.legend(bbox_to_anchor=(1.05, 1.), loc=2,\
              borderaxespad=0., fontsize=10)

    # Set the x-axis to be the names
    py.xticks(range(num_hurricanes), names, rotation='vertical')
    py.ylim(0,180) # Set the limit of the wind speed

    # Set the axis labels and title
    py.ylabel('Wind Speed (knots)')
    py.xlabel('Hurricane Name')
    py.title('Max Hurricane Wind Speed for {}'.format(year))
    py.plot(range(num_hurricanes), max_speed) # plot the wind speed plot
    py.show() # Show the plot

def get_user_input(years: list):
    '''Repeatedly asks the user for input until the user enters valid input.
    The user's input must either be 'quit' or a year that is in years. This
    function should give a list of possible years to the user, but doesn't.
    years: a list of strings that are years'''

    user_input = ''
    while True:
        user_input = input("Enter the year to show hurricane data or 'quit': ")
        user_input = user_input.lower()

        valid_input = user_input in years or user_input == 'quit'
        if valid_input:
            break
        else:
            print('Error with the year key! Try another year')
    return user_input

def main():
    '''Parses hurricane information from a file provided by the user. Allows the
    user to display and plot the data.'''

    fp = open_file()
    dictionary = create_dictionary(fp)

    print('Hurricane Record Software')
    min_year, max_year = get_years(dictionary)
    print('Records from {:4s} to {:4s}'.format(min_year, max_year))

    user_input = get_user_input(dictionary.keys())
    user_quit = user_input == 'quit'
    year = user_input
    while not user_quit:

        display_table(dictionary, year)

        user_input = input('\nDo you want to plot? ').lower()
        wants_plot = user_input == 'yes'
        if wants_plot:
            names, coordinates, max_speed = prepare_plot(dictionary, year)
            num_hurricanes = len(names)
            plot_map(year, num_hurricanes, names, coordinates)
            plot_wind_chart(year, num_hurricanes, names, max_speed)

        # Get valid year key or quit
        user_input = get_user_input(dictionary.keys())
        user_quit = user_input == 'quit'
        year = user_input

if __name__ == '__main__':
    main()
