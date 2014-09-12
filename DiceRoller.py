__name__ = "DiceRoller"
import random as r

def roll(d, n = 1, b = 0):
    total = b
    for x in range(n):
        total+= r.randint(1, d)
    return total

def initiative(bonus):
    return r.randint(1,20) + bonus
    
def attack(bonus):
    attacks = []
    for n in bonus:
        atk = (r.randint(1, 20)) + n
        attacks.append(atk)
    return attacks

def getInitiative(entrants):
    l = entrants
    for charactor in l:
        inp = raw_input("Have Roll for %s" % charactor.Flavor['charactor_name'])
        if inp == "Y":
            num = int(raw_input("Roll = "))
            charactor.initiative = num
        else:
            charactor.initiative = initiative(charactor.Stat['dex'][1])
    return sorted(l, key = lambda charactor: charactor.initiative)
