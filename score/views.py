from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import requests, json
from score.calc import *

# @cache_page(60 * 15)
def index(request, name=None, number=None, hero_id=None):
    """ Renders our mostly static homepage... with room to expand! """
    context = { 'name':name, 'number':number, 'hero_id':hero_id }
    return render(request, 'score/index.html', context)

@cache_page(60 * 15)
def profile(request):
    """ Wraps d3 api calls for player profiles """
    if "name" not in request.GET or "number" not in request.GET:
        return HttpResponseBadRequest('Missing Required Fields')

    name = request.GET['name']
    number = request.GET['number']

    r = requests.get('http://us.battle.net/api/d3/profile/%s-%s/' % (name, number))
    return HttpResponse(r.text)

@cache_page(60 * 5)
def hero(request):
    """ Wraps d3 api calls for heroes """
    if "name" not in request.GET or "number" not in request.GET or "hero_id" not in request.GET:
        return HttpResponseBadRequest('Missing Required Fields')

    name = request.GET['name']
    number = request.GET['number']
    hero_id = request.GET['hero_id']

    if not name or not number or not hero_id:
        return HttpResponseBadRequest()

    # Get hero info
    r = requests.get('http://us.battle.net/api/d3/profile/%s-%s/hero/%s' % (name, number, hero_id))
    heroData = r.json()

    # Grab all item info
    for slot,itemData in heroData['items'].iteritems():
        itemDetail = _get_item(itemData['tooltipParams'])
        heroData['items'][slot] = itemDetail

    # Parse item info
    gearStats = parseItems(heroData['items'])

    def getDPS(item):
        if not 'dps' in item:
            return 0
        return (item['dps']['min'] + item['dps']['max'] / 2)

    # Calculate score
    # Base DPS
    damage = getDPS(heroData['items']['mainHand']) + getDPS(heroData['items']['offHand'])

    # Raw bonus damage
    # damage = damage + gearStats['damageBonus']
    # Elite bonus
    damage = damage * (1 + (gearStats['eliteBonus'] / 100))

    # Priamry stat damage multiplier
    if heroData['class'] in ('wizard','witch-doctor'):
        damage = damage * (heroData['stats']['intelligence'] / 100)
    elif heroData['class'] in ('crusader','barbarian'):
        damage = damage * (heroData['stats']['strength'] / 100)
    elif heroData['class'] in ('demon-hunter','monk'):
        damage = damage * (heroData['stats']['dexterity'] / 100)

    # Elemental
    eleBonus = (gearStats['coldBonus'],
            gearStats['fireBonus'],
            gearStats['arcaneBonus'],
            gearStats['holyBonus'],
            gearStats['poisonBonus'],
            gearStats['physicalBonus'])
    damage = damage * (1 + (max(eleBonus) / 100))

    # Attack speed
    # damage = damage * (1 + (gearStats['attackSpeed'] / 100))


    # Criticals
    critDamage = damage \
            * (.05 + (gearStats['critChance'] / 100)) \
            * (.5 + (gearStats['critDamage'] / 100))
    damage = damage + critDamage

    survivability = 0

    # Report hero and score
    heroData['_damage_score'] = damage
    heroData['_surv_score'] = survivability
    heroData['gearStats'] = gearStats

    return HttpResponse(json.dumps(heroData))

def _get_item(tooltipParam):
    r = requests.get('http://us.battle.net/api/d3/data/%s' % (tooltipParam,))
    return r.json()
