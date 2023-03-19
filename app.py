"""
Student name(s): Pranav Patil, Nisha Balaji
Student email(s): ppatil@caltech.edu, nbalaji@caltech.edu

Check the nutrients you have gotten from your red door orders!
Also check your balance, etc.
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
# to get password
import getpass

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True

class Auth:
    def __init__(self):
        self.authenticated_user = None
        self.is_admin = None

    def logged_in(self):
        return self.authenticated_user != None

    def check_admin(self):
        return self.is_admin == True

    def logout(self):
        self.authenticated_user = None
        self.is_admin = None

auth = Auth()

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306', 
          password='adminpw',
          database='final',
          auth_plugin='mysql_native_password'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def check_admin_priv(username):
    """
    Checks if the logged in user is an administrator. If this was an API, 
    is_admin would be included in the Success response. However, we want 
    to ensure for security reasons that you can't check the admin status
    of other users. otherwise it would help an adversary with enumeration
    or determining which accounts to focus attacks on.
    """
    if auth.authenticated_user == username:
        cursor = conn.cursor()
        sql = 'SELECT is_admin FROM user WHERE username=\'%s\';' % (username, )
        try:
            cursor.execute(sql)
            # row = cursor.fetchone()
            rows = cursor.fetchall()
            for row in rows:
                (user_admin, ) = (row) # tuple unpacking!
                return True if user_admin == 1 else False
        except mysql.connector.Error as err:
            # If you're testing, it's helpful to see more details printed.
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr('Admin access check failed. Please contact an administrator.')
    else:
        sys.stderr('Insufficient permissions for this operation. You must be logged in first.')

def get_menu():
    """
    get the menu items and prices. if there is a user logged in, 
    it will automatically order by the most often ordered thing

    returns list of tuples of (id, name, price) for each menu item
    """
    if auth.logged_in():
        # Remember to pass arguments as a tuple like so to prevent SQL
        # injection.
        sql = '''SELECT item_id, item_name, price_usd FROM
(
    SELECT item_id, COUNT(item_id)-1 AS num FROM
    (
        SELECT item_id 
        FROM orders NATURAL JOIN user NATURAL JOIN orders_items 
        WHERE username=\'%s\'
            UNION ALL 
        SELECT item_id FROM item
    ) AS temp
    GROUP BY item_id
    ORDER BY num DESC
) AS or_items NATURAL LEFT JOIN item;''' % (auth.authenticated_user, )
    else:
        sql = 'SELECT item_id, item_name, price_usd FROM item;'

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        menu = []
        for row in rows:
            menu.append(row)
        return menu
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('Menu get failed. Please contact an administrator.')

def get_ingredients():
    """
    get the ingredients and all relevant details

    returns list of tuples of (id, name) of ingredients
    """
    sql = 'SELECT ingredient_id, ingredient_name FROM ingr_details;'

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        menu = []
        for row in rows:
            menu.append(row)
        return menu
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('Ingredients get failed. Please contact an administrator.')

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)
def login(username, password):
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT authenticate(\'%s\', \'%s\');' % (username, password)
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            (authenticated, ) = (row) # tuple unpacking!
            if authenticated == 1:
                auth.authenticated_user = username
                auth.is_admin = check_admin_priv(username)
                return True
            else:
                auth.authenticated_user = None
                auth.is_admin = None
                return False
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('Login check failed. Please contact an administrator.')

def send_order_out(item_ids):
    """
    creates an order with the specified item_ids in iterable
    """
    if len(item_ids) == 0:
        print ("You can't have an empty order!")
        return
    
    if not auth.logged_in():
        print ("How did you get here???")
        return
    
    sql = 'CALL create_order(\'%s\', \'%s\');' % (auth.authenticated_user, ",".join([str(x) for x in item_ids]), )

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('Order creation failed. Please contact an administrator.')

def submit_menu_item (name, price, ingr_and_amounts):
    """
    name:
        name of menu item
    price:
        price of menu item
    ingr_and_amounts:
        list of (ingredient id, amount of ingredient)
    """
    
    sql = 'CALL create_menu_item(\'%s\', %.2f, "%s", "%s");' % (
        name, 
        price, 
        ",".join([str(x[0]) for x in ingr_and_amounts]),
        ",".join(["{:.2f}".format(x[1]) for x in ingr_and_amounts]),
    )

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('Menu item creation failed. Please contact an administrator.')

def retrieve_nutrients_of_item (item_id):
    """
    item_name:
        name of the menu item
    """

    sql = 'SELECT protein_in_item(item_id) AS total_protein, carbs_in_item(item_id) AS total_carbs, fats_in_item(item_id) AS total_fats, sugars_in_item(item_id) AS total_sugars FROM item WHERE item_id = "%s";' % (item_id)

    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        nutrients = []
        for row in rows:
            nutrients.append(row)
        return nutrients
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('Nutrients get failed. Please contact an administrator.')


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print()
    print('What would you like to do? ')
    
    print('  (m) - View menu')
    print('  (d) - Get nutrients of a menu item')
    if not auth.logged_in():
        print('  (l) - Log in')
    elif not auth.check_admin():
        print('  (v) - View my order history')
        print('  (c) - Create an order')
        print('  (x) - Log out')
    else:
        print('  (n) - Add a menu item')
        print('  (x) - Log out')

    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    print()
    if ans == 'q':
        quit_ui()
    elif ans == 'm':
        show_menu()
    elif ans == 'd':
        get_nutrients()
    elif ans == 'l' and not auth.logged_in():
        login_prompt()
    elif ans == 'x' and auth.logged_in():
        logout_prompt()
    elif ans == 'n' and auth.logged_in() and auth.check_admin():
        create_menu_item()
    elif ans == 'c' and auth.logged_in() and not auth.check_admin():
        create_order_menu()
    elif ans == 'v' and auth.logged_in() and not auth.check_admin():
        pass
    else:
        print ("Invalid option")


def login_prompt():
    """
    asks for username and password but hides password with *****
    will attempt to login
    """
    user_input = input('Enter your username: ')
    pw_input = getpass.getpass('Enter your password: ')

    print()

    result = login(user_input, pw_input)
    if result:
        print (f"Login succeeded! Hi there, {auth.authenticated_user}!")
    else:
        print (f"Login failed. You're not the real {user_input} it seems...")


def logout_prompt():
    """
    logs user out, and doesn't assume that they're logged in
    """
    if auth.logged_in():
        print (f"Goodbye, {auth.authenticated_user}... I hope to see you again.")
        auth.logout()
    else:
        print ("Hey! You're not logged in. How'd you get here you hacker :(")

def show_menu():
    menu = get_menu()

    if auth.logged_in():
        print (f"Oh, hi {auth.authenticated_user}, you're logged in!")
        print (f"Here's a personalized menu with what you order most on top. Seems like you really like the {menu[0][1]}!")
    else:
        print ("Here's the menu:")
    print ()

    for item_id, item_name, price_usd in menu:
        print (f"{item_name.ljust(30)}${price_usd}")

    print ()

def get_nutrients():
    menu = get_menu()
    order_ids = set()

    if not auth.logged_in():
        print ("What are you doing here???")
        return

    print ("Let's find your nutrients!")

    while True:
        print ()
        # print menu at the beginning always
        for i in range(len(menu)):
            item_id, item_name, price_usd = menu[i]
            print (f"[{i+1}] {item_name.ljust(30)}${price_usd}")
        print ('[c] Cancel')
        print ()

        ans = input('For which item would you like to check nutrients? ').lower()

        if ans == 'c':
            return
        try:
            ans_num = int(ans)
            if ans_num >= 1 and ans_num <= len(menu):
                item_id = ans_num
                break
            else:
                print ("Invalid input")
                continue
        except:
            print ("Invalid input")
            continue

    nutrients = retrieve_nutrients_of_item(item_id)

    print('Here are the nutrients for your item:')
    print()
    
    for p, c, f, s in nutrients:
        print (f"{p} grams of protein")
        print (f"{c} grams of carbs")
        print (f"{f} grams of fat")
        print (f"{s} grams of sugar")

def create_order_menu():
    """
    prompts for all items that user wants to add to the order
    then submits order!
    """
    menu = get_menu()
    order_ids = set()

    if not auth.logged_in():
        print ("What are you doing here???")
        return

    print ("Let's create your order!")

    while True:
        print ()
        # print menu at the beginning always
        for i in range(len(menu)):
            item_id, item_name, price_usd = menu[i]
            print (f"[{i+1}] {item_name.ljust(30)}${price_usd}")
        print ('[s] Submit')
        print ('[c] Cancel')
        print ()

        # prompt for which they want
        ans = input('What would you like to add? (or repeat an option to remove it): ').lower()

        # stop asking for new stuff
        if ans == 's':
            break
        elif ans == 'c':
            return
        try:
            ans_num = int(ans)
            if ans_num >= 1 and ans_num <= len(menu):
                if ans_num-1 not in order_ids:
                    order_ids.add(ans_num-1)
                    print (f"Adding {menu[ans_num-1][1]}")
                else:
                    order_ids.remove(ans_num-1)
                    print (f"Removing {menu[ans_num-1][1]}")
            else:
                print ("Invalid input")
                continue
        except:
            print ("Invalid input")
            continue
        print ()
        print (f"Here's what you have so far: {', '.join([menu[i][1] for i in order_ids])}")
        print (f"Your subtotal (pre-tax) is: ${sum([menu[i][2] for i in order_ids]):.2f}")
        print ()
        print ("What's your next item?")

    send_order_out([menu[i][0] for i in order_ids])
    print ("Submitted order!")


def create_menu_item():
    """
    prompts for all items that user wants to add to the order
    then submits order!
    """
    ingredients = get_ingredients()
    ingr_amts = {}

    if not auth.logged_in() or not auth.check_admin():
        print ("What are you doing here???")
        return

    print ("Let's create a menu item!")
    item_name = input("What is the name of the new menu item? ")
    try:
        item_price = float(input(f"What is the price of {item_name}? "))
    except:
        print ("Error: invalid price. ")
        return

    while True:
        print ()
        # print menu at the beginning always
        for i in range(len(ingredients)):
            ingr_id, ingr_name = ingredients[i]
            print (f"[{i+1}] {ingr_name}")
        print ('[s] Submit')
        print ('[c] Cancel')
        print ()

        # prompt for which they want
        ans = input('What would you like to add? (or repeat an option to remove it): ').lower()

        # stop asking for new stuff
        if ans == 's':
            break
        elif ans == 'c':
            return
        try:
            ans_num = int(ans)
            amount = float(input("How much of this ingredient do you want (in grams): "))
        except:
            print ("Invalid input")
            continue
        if ans_num >= 1 and ans_num <= len(ingredients):
            ingr_name = ingredients[ans_num-1][1]
            if ans_num-1 not in ingr_amts:
                ingr_amts[ans_num-1] = amount
                print (f"Adding {amount:.2f} of {ingr_name}")
            else:
                del ingr_amts[ans_num-1]
                print (f"Removing {ingr_name}")
        else:
            print ("Invalid input")
            continue
        print ()
        print (f"Here's what you have so far: {', '.join([f'{ingredients[i][1]} ({ingr_amts[i]:.2f}g)' for i in ingr_amts])}")
        print ()
        print ("What's your next ingredient?")

    submit_menu_item(item_name, item_price, [(ingredients[i][0], ingr_amts[i]) for i in ingr_amts])
    print ("Created menu item!")

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    while True:
        show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
