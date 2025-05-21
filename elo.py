from pip._vendor import requests
import json
import re
from datetime import datetime
import matplotlib.pyplot as plt


def retrieve_messages(channelId):
    """
    Using json and requests, get the message logs of the discord server. store the results into a file
    args:
        channelId (int): the specific id to get the correct message channel
    """

    match_logs = []

    headers = {
        'authorization': ''
    }

    # make the request to the API endpoint
    r = requests.get(f'https://discord.com/api/v9/channels/{channelId}/messages', headers=headers)

    # parse the response to get the messages
    jsonn = json.loads(r.text)

    cutoff = datetime(2025, 5, 1)

    
    filtered_messages = [
    msg for msg in jsonn if datetime.fromisoformat(msg["timestamp"]).replace(tzinfo=None) >= cutoff
    ]
    

    # store the json value into a list - this will be used later for elo calculations 
    for value in filtered_messages:
        match_logs.append(value['content'])

    return match_logs
        
def get_rating(team):
    """
    Get the current elo rating for the team in question. Check the 

    args:
        team (str): the team
    """
    if team not in ratings:
        ratings[team] = 1500
    return ratings[team]

def update_win_loss(team, result):
    # initial check to see if they exist within the record
    if team not in win_loss_records:
        win_loss_records[team] = []

    # second check for the result of the match
    if result == 1:
        win_loss_records[team].append("W")
    else:
        win_loss_records[team].append("L")
    

def expected(r1, r2):
    return 1 / (1 + 10 ** ((r2 - r1) / 400))

def update_elo(winner, loser):
    winner, loser = winner.strip().title(), loser.strip().title()

    # get the elo of the winner and loser
    r_winner, r_loser= get_rating(winner), get_rating(loser)

    # get the wins and losses for each team
    update_win_loss(winner, 1), update_win_loss(loser, 0)

    # calculate the expected elo based on the result of the match
    expected_win, expected_loss = expected(r_winner, r_loser), expected(r_loser, r_winner)

    # calculate the elos. here the K factor is represented by the int value of 32
    ratings[winner] = r_winner + 32 * (1 - expected_win)
    ratings[loser] = r_loser + 32 * (0 - expected_loss)

def substitute_team_numbers(line):
    for code, name in team_map.items():
        if code in line.lower():
            line = re.sub(code, name, line, flags=re.IGNORECASE)
    return line


def parse_line(message):
    """
    """
    line = substitute_team_numbers(message)
    # create patterns to try and 
    patterns = [
        r"(.+?)\s+won against\s+(.+)",
        r"(.+?)\s+win against\s+(.+)",
        r"(.+?)\s+beat\s+(.+)",
        r"(.+?)\s+victors vs\s+(.+?) via .*",
        r"(.+?)\s+won again against the same team",  # Needs context
        r"(.+?)\s+won against\s+(.+)"
    ]

    # 
    result = None

    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            team1 = match.group(1)
            try:
                team2 = match.group(2)
                result =  (team1, team2)
            except IndexError:
                result =  ("repeat_win", team1)
            

    return result

def win_loss_ratio(team):
    wins = 0
    losses = 0

    for r in win_loss_records[team]:
        if r == "W":
            wins += 1
        else:
            losses += 1

    return wins if losses == 0 else wins / losses


def process_games():
    """
    read the matchlogs and calculate the elo for each team participating 
    args:
        match_logs (file): matchlog file for this months 2 headed giant
    """
    for line in match_logs:
        result = parse_line(line)
        if result:
            winner, loser = result
            update_elo(winner, loser)
           

def print_ratings():
    """
    Display the elo ratings and win/loss ratio for each team 
    """
    # display the elo ratings
    for team, rating in sorted(ratings.items(), key=lambda x: -x[1]):
        print(f"{team}: \n Elo ---> {rating:.1f} \n Win/Loss --> {win_loss_ratio(team):.1f}")
    


      
# main guard 
if __name__ == "__main__":

    # TODO make a main function and stop using globals - this works for now but is ugly and needs to be made better


    ratings = {}
    # Team number to name mapping - mock setup of names for test
    
    win_loss_records = {}

    team_map = {
        "team 1": "Mogg Mob",
        "team 2": "Null",
        "team 3": "Stompo",
        "team 4": "2 Guys 1 Lotus",
        "team 5": "John Beater",
        "team 6": "Dauntless Crusaders",
        "team 7": "Professional Rawdoggers",
    }

    # welcomeId = "1364374887879278687"
    matchlogsId =  "1367423785074163712"
    # match_logs = retrieve_messages(matchlogsId)

    match_logs = ['team 4 won against team 5', 
                'team 7 win against team 1', 
                'team 3 victors vs team 7 via infinite#1', 
                'team 4 won against team 1', 
                'team 6 won against team 5', 
                'team 7 win against team 3', 
                'team 7 win against team 3', 
                'team 6 won against team 3', 
                'team 6 won against team 3', 
                'team 5 beat team 7', 
                'Team 4 beat Team 7', 
                'Team 4 beat team 7']

    process_games()
    print_ratings()

    # Prepare data
    sorted_teams = sorted(ratings.items(), key=lambda x: -x[1])
    teams = [team for team, _ in sorted_teams]
    elos = [ratings[team] for team in teams]
    ratios = [win_loss_ratio(team) for team in teams]
    x = range(len(teams))

    ### 1. Vertical Bar Chart with Win/Loss ratio line

    fig, ax1 = plt.subplots(figsize=(8,5))

    bars = ax1.bar(x, elos, color='skyblue', label='Elo Rating')
    ax1.set_ylabel('Elo Rating')
    ax1.set_xlabel('Teams')
    ax1.set_xticks(x)
    ax1.set_xticklabels(teams, rotation=45)
    ax1.set_ylim(0, max(elos)*1.15)
    ax1.set_title('Elo Ratings and Win/Loss Ratio')

    # Labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + 10, f'{elos[i]:.0f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Win/Loss ratio on secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(x, ratios, color='orange', marker='o', label='Win/Loss Ratio')
    ax2.set_ylabel('Win/Loss Ratio')
    ax2.set_ylim(0, max(ratios)*1.15)

    # Legends
    # ax1.legend(loc='lower left')
    # ax2.legend(loc='lower left')

    plt.tight_layout()
    plt.show()

