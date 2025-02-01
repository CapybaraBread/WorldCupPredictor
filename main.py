import random

group_D = {
    "Франция": 0.95,
    "Дания": 0.88,
    "Австралия": 0.75,
    "Тунис": 0.80
}

group_E = {
    "Германия": 0.85,
    "Япония": 0.65,
    "Испания": 0.85,
    "Коста-Рика": 0.55
}

def simulate_group(group, matches):
    tournament_table = {team: 0 for team in group.keys()}
    num_simulations = 1000

    for team1, team2 in matches:
        rating_team1 = group[team1]
        rating_team2 = group[team2]
        prob_team1 = rating_team1 / (rating_team1 + rating_team2)

        wins_team1 = sum(random.random() <= prob_team1 for _ in range(num_simulations))
        wins_team2 = num_simulations - wins_team1


        winner = team1 if wins_team1 > wins_team2 else team2
        tournament_table[winner] += 3

    sorted_table = sorted(tournament_table.items(), key=lambda x: x[1], reverse=True)
    return sorted_table


def generate_matches(group):
    teams = list(group.keys())
    return [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]

matches_D = generate_matches(group_D)
matches_E = generate_matches(group_E)

results_D = simulate_group(group_D, matches_D)
results_E = simulate_group(group_E, matches_E)

inter_group_matches = [
    (results_D[0][0], results_E[0][0]),
    (results_D[1][0], results_E[1][0]),
    (results_D[2][0], results_E[2][0])
]

def simulate_knockout_match(team1, team2, group_D, group_E, num_simulations=1000):
    rating_team1 = group_D.get(team1, group_E.get(team1))
    rating_team2 = group_D.get(team2, group_E.get(team2))
    prob_team1 = rating_team1 / (rating_team1 + rating_team2)

    wins_team1 = sum(random.random() <= prob_team1 for _ in range(num_simulations))
    wins_team2 = num_simulations - wins_team1

    return team1 if wins_team1 > wins_team2 else team2

winners = [simulate_knockout_match(team1, team2, group_D, group_E) for team1, team2 in inter_group_matches]

num_tournaments = 10000
champion_counts = {team: 0 for team in list(group_D.keys()) + list(group_E.keys())}
finalist_counts = {team: 0 for team in list(group_D.keys()) + list(group_E.keys())}
podium_counts = {team: 0 for team in list(group_D.keys()) + list(group_E.keys())}

for _ in range(num_tournaments):
    sim_results_D = simulate_group(group_D, matches_D)
    sim_results_E = simulate_group(group_E, matches_E)
    
    semifinal_matches = [
        (sim_results_D[0][0], sim_results_E[1][0]),
        (sim_results_E[0][0], sim_results_D[1][0])
    ]
    
    finalists = [simulate_knockout_match(team1, team2, group_D, group_E) for team1, team2 in semifinal_matches]
    for team in finalists:
        finalist_counts[team] += 1

    champion = simulate_knockout_match(finalists[0], finalists[1], group_D, group_E)
    champion_counts[champion] += 1
    
    for team in finalists:
        podium_counts[team] += 1
    
    third_place_winner = simulate_knockout_match(semifinal_matches[0][0], semifinal_matches[1][0], group_D, group_E)
    podium_counts[third_place_winner] += 1

champion_probs = {team: (champion_counts[team] / num_tournaments) * 100 for team in champion_counts}
finalist_probs = {team: (finalist_counts[team] / num_tournaments) * 100 for team in finalist_counts}
podium_probs = {team: (podium_counts[team] / num_tournaments) * 100 for team in podium_counts}

probabilities = {
    "champion_probs": champion_probs,
    "finalist_probs": finalist_probs,
    "podium_probs": podium_probs
}

print(probabilities)
