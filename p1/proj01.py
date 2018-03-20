###########################################################
#  Computer Project #1
#
# Receive string A representing number of rods from user
# Convert A to a number X
# Convert X from rods to meters, furlongs, miles, and feet
#     To convert X from unit a to unit b using the conversion factor a_per_b
#        divide X by a_per_b
#        or
#        multiply X by b_per_a
# Output conversions
# Compute time to walk N rods at some speed of miles per hour
# Output walking time
# All numbers are expected to be floats
#
###########################################################

# Conversion factors and constants
METER_PER_ROD = 5.0292
RODS_PER_FURLONG = 40.0
METERS_PER_MILE = 1609.34
METERS_PER_FOOT = 0.3048
MILES_PER_HOUR = 3.1
MINUTES_PER_HOUR = 60.0

# Get number of rods from user's input
number_of_rods_str = input("Input rods: ")
number_of_rods = float(number_of_rods_str)
print("You input", round(number_of_rods, 3), "rods.")
print("")

# Convert rods to different units and print results
number_of_meters = number_of_rods * METER_PER_ROD
number_of_miles = number_of_meters / METERS_PER_MILE
number_of_feet = number_of_meters / METERS_PER_FOOT
number_of_furlongs = number_of_rods / RODS_PER_FURLONG

print("Conversions")
print("Meters:", round(number_of_meters, 3))
print("Feet:", round(number_of_feet, 3))
print("Miles:", round(number_of_miles, 3))
print("Furlongs:", round(number_of_furlongs, 3))

# Calculate and print how much time it takes to walk a certain distance in rods
number_of_miles = number_of_meters / METERS_PER_MILE
number_of_hours = number_of_miles / MILES_PER_HOUR
number_of_minutes = number_of_hours * MINUTES_PER_HOUR

print("Minutes to walk", number_of_rods, "rods:", round(number_of_minutes, 3))

