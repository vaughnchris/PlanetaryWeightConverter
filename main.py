from sys import exit
import matplotlib.pyplot as plt


def isInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def menu():
    # collect user inputs
    while True:
        print('''
       1. Mercury
       2. Venus
       3. Mars
       4. Jupiter
       5. Saturn
       6. Uranus
       7. Neptune
       0. Exit''')
        selection = input("\nEnter the planet #'s you wish to calculate for with spaces : ")
        selection_list = selection.strip().split()

        valid_selections = []
        has_error = False

        # Verify all inputs are valid before proceeding
        for item in selection_list:
            if isInteger(item) and (0 <= int(item) <= 7):
                valid_selections.append(int(item))
            else:
                has_error = True

        if has_error or not valid_selections:
            print("Error on input. Please enter again.")
            continue

        return valid_selections

def getPlanet(menuSelections):
    planets = {}
    # Iterate through the list of selections
    for item in menuSelections:
        # identify the planet and multiplier based on the user selection
        match int(item):
            case 1:
                planets['Mercury'] = 0.38
            case 2:
                planets['Venus'] = 0.91
            case 3:
                planets['Mars'] = 0.38
            case 4:
                planets['Jupiter'] = 2.34
            case 5:
                planets['Saturn'] = 1.06
            case 6:
                planets['Uranus'] = 0.92
            case 7:
                planets['Neptune'] = 1.19
            case 0:
                planets['Exit'] = 0
            case _:
                # If an incorrect planet number is selected present error and exit
                print("An incorrect menu choice was entered... Try again.")
    return planets


def getWeight():
    while True:
        # Get raw input first, then validate it
        earthWeight_input = input('Enter your weight on Earth: ')
        if isFloat(earthWeight_input) and float(earthWeight_input) > 0:
            return float(earthWeight_input)
        else:
            print("Error on input. Please enter again.")
            continue


# Create the main program entry point
def start():
    print("PLANETARY WEIGHT CALCULATOR", '\n')
    while True:
        menuItems = menu()
        planets = getPlanet(menuItems)

        if 'Exit' in planets:
            exit(0)

        earthWeight = getWeight()

        # Lists to hold data for our graph
        planet_names = ['Earth']
        calculated_weights = [earthWeight]

        # Print the results and gather data for the graph
        for planet_name, multiplier in planets.items():
            planet_weight = earthWeight * multiplier
            print(f"{earthWeight:.2f} Earth pounds is equal to {planet_weight:.2f} {planet_name} pounds.")

            # Add data to our lists
            planet_names.append(planet_name)
            calculated_weights.append(planet_weight)

        # --- NEW GRAPHING CODE ---
        # Create a figure and axis
        fig, ax = plt.subplots()
        bars = ax.bar(planet_names, calculated_weights, color='skyblue')

        # Add labels and a title
        ax.set_xlabel('Planets')
        ax.set_ylabel('Weight (lbs)')
        ax.set_title('Your Weight on Different Planets')

        # Create annotation for tooltip
        annot = ax.annotate("", xy=(0, 0), xytext=(0, 10),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.8),
                            ha='center')
        annot.set_visible(False)

        def update_annot(bar):
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_height()
            annot.xy = (x, y)
            annot.set_text(f"{y:.2f} lbs")

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                for bar in bars:
                    cont, _ = bar.contains(event)
                    if cont:
                        update_annot(bar)
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)

        # Display the graph in a new window
        plt.show()

    return None


start()