STAT_TABLE = (
    # Tri
    ('Crit_Damage_Percent','critDamage'),
    ('Crit_Percent_Bonus_Capped','critChance'),
    ('Attacks_Per_Second_Percent','attackSpeed'),

    # Primary Stats
    ('Intelligence_item','intelligence'),
    ('Strength_item','strength'),
    ('Dexterity_item','dexterity'),
    ('Vitality_item','vitality'),

    # Defensive
    ('Armor_Bonus_Item', 'armor'),
    ('Armor_Item', 'armor'),
    ### Resist all is a special case ###

    # +Elemental Damage
    ('Damage_Dealt_Percent_Bonus#Cold','coldBonus'),
    ('Damage_Dealt_Percent_Bonus#Fire','fireBonus'),
    ('Damage_Dealt_Percent_Bonus#Arcane','arcaneBonus'),
    ('Damage_Dealt_Percent_Bonus#Holy','holyBonus'),
    ('Damage_Dealt_Percent_Bonus#Physical','physicalBonus'),
    ('Damage_Dealt_Percent_Bonus#Poison','poisonBonus'),

    # Elite Damage
    ('Damage_Percent_Bonus_Vs_Elites', 'eliteBonus'),

    # Utility
    ('Movement_Scalar','moveSpeed'),
)


def parseItems(items):
    gearStats = {}
    for _,stat in STAT_TABLE:
        gearStats[stat] = 0

    def valueOf(attr):
        return (attr['min'] + attr['max']) / 2

    def searchStats(attrs):
        for (attrString, gearStat) in STAT_TABLE:
            if attrString in attrs:
                val = valueOf(attrs[attrString])
                if ('Percent' in attrString) or ('Scalar' in attrString):
                    val = val * 100
                gearStats[gearStat] = gearStats[gearStat] + val

    for slot,item in items.iteritems():
        searchStats(item['attributesRaw'])

        for gem in item['gems']:
            searchStats(gem['attributesRaw'])

    return gearStats
