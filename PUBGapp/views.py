import pandas as pd
from django.shortcuts import render
import joblib

# Create your views here.
solos = joblib.load('./models/SoloModel.pkl')
duos = joblib.load('./models/DuoModel.pkl')
squads = joblib.load('./models/SquadModel.pkl')


def index(request):
    return render(request, 'index.html')


def predictPlacement(request):
    temp = dict()
    temp['assists'] = float(request.POST.get('assistsVal'))
    temp['boosts'] = float(request.POST.get('boostsVal'))
    temp['DBNOs'] = float(request.POST.get('DBNOsVal'))
    temp['heals'] = float(request.POST.get('healsVal'))
    temp['killStreaks'] = float(request.POST.get('killstreaksVal'))
    temp['longestKill'] = float(request.POST.get('distancekillVal'))
    temp['matchDuration'] = float(request.POST.get('matchDurationVal'))
    temp['rankPoints'] = float(request.POST.get('rankVal'))
    temp['revives'] = float(request.POST.get('revivesVal'))
    temp['rideDistance'] = float(request.POST.get('rideDistanceVal'))
    temp['roadKills'] = float(request.POST.get('roadKillsVal'))
    temp['swimDistance'] = float(request.POST.get('SwimVal'))
    temp['teamKills'] = float(request.POST.get('teamKillsVal'))
    temp['vehicleDestroys'] = float(request.POST.get('vehicleDestroysVal'))
    temp['walkDistance'] = float(request.POST.get('walkVal'))
    temp['weaponsAcquired'] = float(request.POST.get('weaponsVal'))
    temp['players_in_match'] = float(request.POST.get('players_in_matchVal'))
    temp['players_in_team'] = float(request.POST.get('players_in_teamVal'))
    temp['kills_in_match'] = float(request.POST.get('kills_in_matchVal'))
    temp['damage_in_match'] = float(request.POST.get('damage_in_matchVal'))
    temp['percent_team_kill'] = float(request.POST.get('damage_in_matchVal'))
    temp['percent_team_damage'] = float(request.POST.get('teamKVal'))
    temp['headshot_rate'] = float(request.POST.get('headshot_rateVal'))
    temp['items'] = float(request.POST.get('itemsVal'))
    temp['total_distance'] = temp['walkDistance'] + temp['swimDistance'] + temp['rideDistance']
    temp['heals_and_boosts'] = temp['boosts'] + temp['heals']
    testData = pd.DataFrame({'x': temp}).transpose()
    if request.POST.get('matchType') == 'solo':
        testData['maxPlace'] = 97
        testData['numGroups'] = 95
        testData['percent_kill'] = testData['kills_in_match']/(testData['players_in_match']-1)
        testData['percent_damage'] = 0.00994
        testData['percent_team_damage'] = 0.010113
        result = solos.predict(testData[['assists', 'killStreaks', 'longestKill', 'matchDuration', 'maxPlace', 'numGroups', 'rankPoints', 'teamKills', 'vehicleDestroys', 'players_in_match', 'kills_in_match', 'percent_kill', 'damage_in_match', 'headshot_rate', 'heals_and_boosts', 'items', 'total_distance']])
    elif request.POST.get('matchType') == 'duo':
        testData['maxPlace'] = 50
        testData['numGroups'] = 48
        testData['percent_kill'] = testData['kills_in_match'] / (testData['players_in_match'] - testData['players_in_team'])
        testData['percent_damage'] = 0.010113
        testData['percent_team_damage'] = 0.021149
        result = duos.predict(testData[['assists', 'DBNOs', 'killStreaks', 'longestKill', 'matchDuration', 'maxPlace', 'numGroups', 'rankPoints', 'revives', 'teamKills', 'vehicleDestroys', 'players_in_match', 'players_in_team', 'kills_in_match', 'percent_kill', 'damage_in_match', 'percent_damage', 'percent_team_damage', 'headshot_rate', 'heals_and_boosts', 'items', 'total_distance']])
    else:
        testData['maxPlace'] = 28
        testData['numGroups'] = 28
        testData['percent_kill'] = testData['kills_in_match'] / (testData['players_in_match'] - testData['players_in_team'])
        testData['percent_damage'] = 0.010121
        testData['percent_team_damage'] = 0.040337
        result = squads.predict(testData[['assists', 'DBNOs', 'killStreaks', 'longestKill', 'matchDuration', 'maxPlace', 'numGroups', 'rankPoints', 'revives', 'teamKills', 'vehicleDestroys', 'players_in_match', 'players_in_team', 'kills_in_match', 'percent_kill', 'percent_team_kill', 'damage_in_match', 'percent_damage', 'percent_team_damage', 'headshot_rate', 'heals_and_boosts', 'items',  'total_distance']])
    result = {'prediction': abs(float(format(result[0], ".2f")))*100}

    return render(request, 'Result.html', result)
