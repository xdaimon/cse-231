###########################################################
# Computer Project #2
#
# Calculate amount of change for a payment on some price.
#
# Repeat while user input not equal to 'q'
#     Display number of coins remaining in stock
#     Request non negative price for item to be purchased and ask to quit
#     Request number of dollars to use for payment
#     Loop while payment < price
#         Request number of dollars to use for payment
#     If payment == price print "No Change"
#     Otherwise
#     Compute change
#         Minimize the number of coins we use for change by using as many large
#         denomination coins as possible before using any coins of smaller value
#
#         An amount of change Y is equal to n coins, each of value X, plus some
#         number of pennies p such that p <= X. So
#         Y == n * X + p
#         We can find n by dividing both sides by X and throwing out any
#         fractional part, that is by compute the quotient of Y divided by X.
#
# purchase price, payment, and change will be kept in cents
#
###########################################################

# We start with 40 coins in stock
quarters_stock = 10
dimes_stock = 10
nickels_stock = 10
pennies_stock = 10

DOLLARS_TO_CENTS = 100
QUARTERS_TO_CENTS = 25
DIMES_TO_CENTS = 10
NICKELS_TO_CENTS = 5

print("\nWelcome to change-making program.")

print("\nStock: {} quarters, {} dimes, {} nickels, and {} pennies".format(
    quarters_stock, dimes_stock, nickels_stock, pennies_stock))

input_str = input("\nEnter the purchase price (xx.xx) or 'q' to quit: ")

while input_str != 'q':

    price_float = float(input_str)
    if price_float < 0.0:
        print("Error: purchase price must be non-negative.")
    else:
        payment_float = float(input("\nInput dollars paid (int): "))
        # Payment must be at least equal to price
        while payment_float < price_float:
            print("Error: insufficient payment.")
            payment_float = float(input("\nInput dollars paid (int): "))

        # Calculate amount of change to make
        price_int = round(DOLLARS_TO_CENTS * price_float)
        payment_int = round(DOLLARS_TO_CENTS * payment_float)
        change_int = payment_int - price_int

        if change_int == 0:
            print("No change.")
        else:
            # Make change

            quarters_change = 0
            dimes_change = 0
            nickels_change = 0
            pennies_change = 0

            # Quarters
            # We can only use coins of value X to make an amount of change C
            # such that C >= X
            if change_int >= QUARTERS_TO_CENTS:
                quarters_change = change_int // QUARTERS_TO_CENTS
                # We cannot use more quarters than we have in stock
                if quarters_change > quarters_stock:
                    quarters_change = quarters_stock
            # Remove amount of change that we've made with quarters from the
            # amount of change that remains to be made
            change_int -= QUARTERS_TO_CENTS * quarters_change

            # Dimes
            if change_int >= DIMES_TO_CENTS:
                dimes_change = change_int // DIMES_TO_CENTS
                if dimes_change > dimes_stock:
                    dimes_change = dimes_stock
            change_int -= DIMES_TO_CENTS * dimes_change

            # Nickels
            if change_int >= NICKELS_TO_CENTS:
                nickels_change = change_int // NICKELS_TO_CENTS
                if nickels_change > nickels_stock:
                    nickels_change = nickels_stock
            change_int -= NICKELS_TO_CENTS * nickels_change

            # Pennies
            pennies_change = change_int
            if pennies_change > pennies_stock:
                print("Error: ran out of coins.")
                break

            # Remove coins used from stock
            quarters_stock -= quarters_change
            dimes_stock -= dimes_change
            nickels_stock -= nickels_change
            pennies_stock -= pennies_change

            # Output number of coins used to make change
            print("\nCollect change below:")
            if quarters_change:
                print("Quarters:", quarters_change)
            if dimes_change:
                print("Dimes:", dimes_change)
            if nickels_change:
                print("Nickels:", nickels_change)
            if pennies_change:
                print("Pennies:", pennies_change)

    print("\nStock: {} quarters, {} dimes, {} nickels, and {} pennies" \
        .format(quarters_stock, dimes_stock, nickels_stock, pennies_stock))

    input_str = input("\nEnter the purchase price (xx.xx) or 'q' to quit: ")

