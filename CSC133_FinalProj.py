"""

CSC 133: Modelling and Simulation
Final Project

Quantifying Luck: Monte Carlo Analysis of Gacha System
Submitted By: Reggie Nicole C. Cuberos
Submitted On: June 26, 2023

"""

import random
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
from scipy.stats import skew
from scipy.stats import kurtosis


# DEFINING CONSTANTS
BASE_PROB = .006
BONUS_PROB = .06
WISH_PRIMO_PRICE = 160

def median(list):
    return stat.median(list)

def mode(list):
    return stat.mode(list)

# no_of_pulls -> Number of pulls to simulate, by default 1
# current_pity -> Current pity of the Player, currently 0
# is_guaranteed -> Determines if the player is guaranteed or not
def simulate_wish(no_of_pulls=1, current_pity=0, is_guaranteed=False):  # SETTING DEFAULT VALUES
    is_guaranteed = is_guaranteed
    current_pity = current_pity
    pity_180 = current_pity
    current_probability = BASE_PROB
    results_5star = []

    for i in range(no_of_pulls):
        if current_pity >= 73:
            current_probability += BONUS_PROB
        random_number = random.randint(0, 1000) / 1000.0  # Generate random number between 0 and 1.0
        if random_number < current_probability:
            if not is_guaranteed:  # Handle's 50-50
                win_5050 = random.choice([0, 1])
                if win_5050 == 1:  # 50-50 win
                    result = ("Win_50", pity_180)
                    results_5star.append(result)
                    is_guaranteed = False
                    current_pity = 0
                    current_probability = BASE_PROB
                    pity_180 = 0
                    return results_5star
                else:  # lost 50-50
                    result = ("lose", pity_180)
                    results_5star.append(result)
                    is_guaranteed = True
                    current_pity = 0
                    current_probability = BASE_PROB
            else:  # guarantee
                result = ("Win_G", pity_180)
                results_5star.append(result)
                is_guaranteed = False
                current_pity = 0
                current_probability = BASE_PROB
                pity_180 = 0
                return results_5star

        current_pity += 1  # Adds pity if not 5-star
        pity_180 += 1
        '''Note:
                The current_probability acts as a wall, wherein only numbers within its range 0 to current_probability would be considered a win.
                If the number generated in the random_number is greater than the current_probability (outside the range) then its considered as a loss.'''
    return results_5star


NO_OF_PULLS = 90  # Maximum number of pulls to do
NO_OF_PLAYERS = 150000

win_g_results = []  # STORES ALL NUMBER OF PULLS TO WIN LIMITED 5 STAR, CUMMULATIVE RESULT OF EACH PLAYER
lose_results = []  # STORES ALL NUMBER OF PULLS TO LOSE LIMITED 5 STAR, CUMMULATIVE RESULT OF EACH PLAYER
win_50_results = []
win_results = []

min_pulls_win_50 = float('inf')
max_pulls_win_g = float('-inf')
player_min_pulls_win_50 = None
player_max_pulls_win_g = None

for i in range(NO_OF_PLAYERS):
    result = simulate_wish(no_of_pulls=NO_OF_PULLS)

    for res, pity_counter in result:
        if res == "Win_50":
            if pity_counter > 0:  # Exclude players who won at 0 pity
                win_50_results.append(pity_counter)
                if pity_counter < min_pulls_win_50:
                    min_pulls_win_50 = pity_counter
                    player_min_pulls_win_50 = [i + 1]  # Add 1 to adjust player numbering
                elif pity_counter == min_pulls_win_50:
                    player_min_pulls_win_50.append(i + 1)  # Add 1 to adjust player numbering
        elif res == "Win_G":
            if pity_counter > 0:  # Exclude players who won at 0 pity
                win_g_results.append(pity_counter)
                if pity_counter > max_pulls_win_g:
                    max_pulls_win_g = pity_counter
                    player_max_pulls_win_g = [i + 1]  # Add 1 to adjust player numbering
                elif pity_counter == max_pulls_win_g:
                    player_max_pulls_win_g.append(i + 1)  # Add 1 to adjust player numbering
        else:
            lose_results.append(pity_counter)
    if NO_OF_PULLS <= 1000:  # PRINTS THE RESULTS OF EACH PLAYER
        print(f"Player {i + 1}: {result}")

# ALL WINS (50-50 and Guaranteed)
win_results = win_50_results.copy()
win_results.extend(win_g_results)


#Measures the frequency of players according to its parameters
mode_50 = mode(win_50_results) 
mode_g = mode(win_g_results)
mode_l = mode(lose_results)

probable_primo_cost_win_50 = mode_50 * WISH_PRIMO_PRICE
probable_primo_cost_guaranteed_wins = mode_g * WISH_PRIMO_PRICE
probable_primo_cost_lose = mode_l * WISH_PRIMO_PRICE

print("\n")
print("GENERAL RESULTS ----------")
print(f"Number of pulls: {NO_OF_PULLS}")
print(f"Number of players: {NO_OF_PLAYERS}")
print("\n")

print("Pulls to win 50/50")
print("Probable number of Pulls needed to win 50/50: ", mode_50)
print(f"Average primo cost to win: {probable_primo_cost_win_50}")
print("\n")

print("Pulls to lose")
print("Probable number of Pulls spent to lose: ", mode_l)
print(f"Average primo cost to lose: {probable_primo_cost_lose}")
print("\n")

print("Pulls to win in Guaranteed")
print("Probable number of Pulls needed to win the guarantee: ", mode_g)
print(f"Average primo cost to win: {probable_primo_cost_guaranteed_wins}")
print("\n")

print("Player with the least amount of pulls (won 50/50):")
print(f"Player {player_min_pulls_win_50} with {min_pulls_win_50} pulls")

print("Player with the largest amount of pulls (guaranteed pull):")
print(f"Player {player_max_pulls_win_g} with {max_pulls_win_g} pulls")
print("\n")

#Further Analysis of the Graph, Only Applicable for 90 pulls
med = median(win_results)
print("Median of Data Set: ", med)
print("\n")

print("Skewness of the Distribution:", str(skew(win_results, axis=0, bias=True)))
print("Kurtosis of the Distribution:", str(kurtosis(win_results, axis=0, bias=True)))


print("\n")



if NO_OF_PULLS <= 10:  # PRINT LANG SIYA IF GAMAY RA, IF DAGHAN ANG PULLS DI NA MAG PRINT MAPUNO ANG TERMINAL
    print("\n")
    print("Results Array ----- ")
    print("Pulls to lose")
    print(f"Results: {lose_results}")
    print("Pulls to lose")
    print(f"Results: {lose_results}")

#Plotting of Results
x = np.arange(NO_OF_PULLS)
y = np.bincount(win_results, minlength=NO_OF_PULLS)

plt.bar(x, y)

plt.title('Genshin Wish Simulator')
plt.xlabel('Pity')
plt.ylabel('Frequency of Wins')

plt.show()


