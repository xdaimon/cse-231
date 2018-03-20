####################################################
# Computer Project 7
#
# This program maps a set IP addresses to a set of country names.
# In order to map an IP address to a country name we assign an IP address range
# to the country name. If an IP address falls within the IP address range for a
# country name, then that IP address is mapped to that country name.
#
# Given a file A of IP addresses and a file B of IP range to country name
# mappings, we want to display the 10 countries from B that have the most IP's
# in A.
#
# Convert the IP addresses from A to integers.
#     Take each octet and left pad with zeros until the octet has 3 digits.
#     Append these octets into a single integer.
# For each country, convert the IP addresses for the country's IP address range
# to integers, start_ip and end_ip.
# Now to check if an IP address belongs to a certain country, just check if
# start_ip <= IP address <= end_ip
#
# In the code we use three files instead of two. Instead of mapping IP's
# directly to country names, we first map IP's to country codes
# ('US' for 'United States') and then we map country codes to country names.
# So we have an extra file containing country code to country name mappings.
#
####################################################
import csv
import pylab
from operator import itemgetter

def open_file(message):
    """prompt for file name, open file, return file pointer"""
    while True:
        try:
            filename = input(message)
            fp = open(filename)
            break
        except FileNotFoundError:
            print("File is not found! Try Again!")
    return fp

def int_for_ip_str(ip_str):
    """Converts an ip string, in the format 10.234.31 or 10.234.31.0, to an
    int in the format 010234031000. The function handles input ip addresses with
    both 3 and 4 octets."""

    # Remove whitespace and separate into chunks delimited by '.'
    code_list = ip_str.strip().split('.')
    # Pad each code with zeros so that the code contains 3 digits
    code_list = [code.zfill(3) for code in code_list]

    OCTET_LEN = 3
    OCTETS_IN_IP = 4

    # Make sure we have a 12 character string before converting to an int
    code_list.append('0'*OCTET_LEN * (OCTETS_IN_IP - len(code_list)))
    ip_str = ''.join(code_list)

    return int(ip_str)

def read_ip_location(file):
    """Returns a list of tuples where each tuple contains an ip range and the
    country code owning that ip range.

    file is a list of x's where x is a list containing a start ip, an end ip
    and a country code.

    returns [(start_ip, end_ip, country_code), ... ]
    start_ip: 12-digit int
    end_ip: 12-digit int
    country_code: 2-char string
    """
    file = csv.reader(file)
    ip_range_for_country_list = []
    for range_info in file:
        start_ip_str = range_info[0]
        end_ip_str = range_info[1]
        country_code_str = range_info[2]

        start_ip_int = int_for_ip_str(start_ip_str)
        end_ip_int = int_for_ip_str(end_ip_str)

        tup = (start_ip_int, end_ip_int, country_code_str)
        ip_range_for_country_list.append(tup)

    return ip_range_for_country_list

def read_ip_attack(file):
    """Read a file of ip addresses and output a tuple for each address.
    Returns a list of tuples where each tuple is (the ip as an int, the ip as
    a string).
    """
    ip_list = []
    for ip_str in file:
        ip_str = ip_str.strip()

        ip_int = int_for_ip_str(ip_str)
        ip_str = ip_str + '.xxx'

        tup = (ip_int, ip_str)
        ip_list.append(tup)

    return ip_list

def read_country_name(file):
    """Read a file of country code -> country name mappings.
    Return a list of tuples where each tuple is (country_code, country_name).
    """
    country_code_name_map = []
    for line in file:
        country_name, country_code = line.strip().split(';')
        tup = (country_code, country_name)
        country_code_name_map.append(tup)
    return country_code_name_map

def locate_address(ip_list, ip_attack):
    """Find which country the ip in ip_attack belongs to.

    ip_list is a list of tuples where each tuple contains the range of ips and
    the name of the country that range belongs to.

    Each tuple is in the format (start_ip, end_ip, country_code).
    ip_list must be sorted based on start_ip in each tuple.
    """
    size = len(ip_list)

    country_code = None

    end = size
    mid = end//2
    start = 0
    while country_code is None:
        ip_mid = ip_list[mid][0]
        if ip_attack < ip_mid:
            end = mid
            mid = end//2
        elif ip_attack > ip_mid:
            start = mid
            mid = (end + start)//2
        else:
            country_code = ip_list[mid][2]

        if mid == end or mid == start:
            country_code = ip_list[mid][2]

    return country_code

def get_country_name(country_list, code):
    """Return the country name for the country code in code."""
    for country_code, country_name in country_list:
        if country_code == code:
            return country_name
    print('contry name not found for code')
    exit(-1)

def bar_plot(count_list, countries):
    pylab.figure(figsize=(10,6))
    pylab.bar(list(range(len(count_list))), count_list, tick_label = countries)
    pylab.title("Countries with highest number of attacks")
    pylab.xlabel("Countries")
    pylab.ylabel("Number of attacks")
    pylab.show()

def transpose(x):
    """Transpose a table.
    The ith element of x is plugged into the ith argument position of zip.
    That is the nth row of the table x is used as the nth argument to zip.

    Then zip forms a list using the jth element of each of its arguments.
    Zip forms a list using the jth element of each row of x. That is, zip takes
    the jth column of x and forms a list from that column.

    The result is the transpose of x if we take each list in the list of lists
    output by zip to be a row in a table.
    """
    return list(zip(*x))

def main():
    """Maps ip addresses to country names and outputs the countries that have
    the most ip addresses."""
    file = open_file("Enter the filename for the IP Address location list: ")
    ip_location_data = read_ip_location(file)
    file.close()

    file = open_file("Enter the filename for the IP Address attacks: ")
    attack_data = read_ip_attack(file)
    file.close()

    file = open_file("Enter the filename for the country codes: ")
    country_data = read_country_name(file)
    file.close()

    # Sort to make locate_address faster
    ip_location_data.sort()

    # Make a dictionary for finding country names easily
    country_code_dict = {}
    for country_code,country_name in country_data:
        country_code_dict[country_code] = country_name

    # Display data
    answer = input('\nDo you want to display all data? ').lower()
    if answer in ['yes', 'y']:
        fmt_str = 'The IP Address: {:19s}originated from {}'
        for ip_int,ip_str in attack_data:
            country_code = locate_address(ip_location_data, ip_int)
            # country_name = get_country_name(country_data, country_code)
            country_name = country_code_dict[country_code]
            print(fmt_str.format(ip_str, country_name))

    # Count number of attacks from some country
    country_count_dict = {}
    for attacker_ip in attack_data:
        attacker_ip_int = attacker_ip[0]
        country_code = locate_address(ip_location_data, attacker_ip_int)
        # Get counts for country, if country is not in dict then return 0
        attack_count = country_count_dict.get(country_code, 0)
        # Increment counts for country, if country not in dict add it to dict.
        country_count_dict[country_code] = attack_count + 1

    # Display number of attacks
    print("\nTop 10 Attack Countries")
    # Sort based on count and then based on country code string
    country_count_list = [x for x in country_count_dict.items()]
    country_count_list.sort(key=itemgetter(1,0), reverse=True)
    # Keep only the top ten
    country_count_list = country_count_list[:10]
    print('Country  Count')
    for country_count in country_count_list:
        country_code = country_count[0]
        count = country_count[1]
        print('{}{:12d}'.format(country_code, count))

    # Optionally plot a bar chart
    answer = input("\nDo you want to plot? ")
    if answer.lower() in ['yes', 'y']:
        count_list_T = transpose(count_list)
        countries = count_list_T[0]
        counts = count_list_T[1]
        bar_plot(counts, countries)

if __name__ == "__main__":
    main()


