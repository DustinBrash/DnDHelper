__name__ = "CharGen"
import DiceRoller
import re
class charactor(object):
    stats = (
        'hit dice', 'current hp', 'current total hp', 'normal hp', 'current ac', 'normal ac',
        'level', 'str', 'dex', 'con', 'int', 'wis', 'cha', 'fort',
        'reflex', 'will', 'BaB', 'speed', 'cls', 'alignment', 
    )
    
    def __init__(self, listStat):
        self.Stat = {}
        self.Weapons = {}
        self.Feats = []
        self.Skills = {}
        self.Equipment = []
        
        for n in range(len(charactor.stats)):
            self.Stat[charactor.stats[n]] = listStat[n]
        
    def __repr__(self):
        stringy =''
        for entry in self.stats:
            stringy += "STAT " + entry + ": " + str(self.Stat[entry]) + '\n'
        stringy += '\n'
        for key, value in self.Weapons.iteritems():
            stringy += 'WEAPON' + '\n\n' + key + '\n'
            for keyb, valueb in value.info.iteritems():
                stringy += keyb + ': ' + str(valueb) + '\n'
        stringy += '\n'
        for feat in self.Feats:
            stringy += "FEAT " + feat + '\n'
        stringy += '\n'
        for key, value in self.Skills.iteritems():
            stringy += "SKILL " + key + ': ' + str(value) + '\n'
        return stringy
    
    def add_weapon(self, weapon):
        name = weapon.info['name']
        self.Weapons[name] = weapon

    def add_feat(self, feat):
        self.Feats.append(feat)

    def get_stat(self, stat):
        num = self.Stat[stat]
        num = num / 2 - 5
        return num

    def add_skill(self, name, ability, ranks = 0, armor_penalty = 0):
        self.Skills[name] = ranks + self.get_stat(ability) - armor_penalty

    def is_hit(self, num):
        return num >= self.Stat['current_ac']
            
    def attacks(self, weapon, BaB):
        l = []
        bonus = self.get_stat('strn') + weapon.info['attack bonus']
        for n in BaB:
            l.append(n + bonus)
        return attack(l)

    def damage(self, weapon, n):        
        l = []
        num = weapon.info['damage'][0]
        dice_type = weapon.info['damage'][1]
        bonus = weapon.info['damage'][2]
        for x in range(n):
            l.append(roll(dice_type, num, bonus))
        return l
        
    def save(self, roll, dc, check):
        defend = roll + self.Stat[check]
        return defend >= dc
        
    def get_flat_footed(self):
        dex, ac = self.get_stat('dex'), self.Stat['current_ac']        
        if dex < 0:
            return ac + dex
        else:
            return ac - dex
        
    def get_touch_ac(self):
        return (10 + self.get_stat('dex'))

    def search(self, term):
        term_check = True
        l = str(self).split()
        check = re.compile(term, re.IGNORECASE)
        for word in l:
            m = check.search(word)
            try:
                print m.group()
                break
            except:
                term_check = False
        if not term_check:
            print 'No match'

    def damaged(self, damage):
        self.Stat['current hp'] -= damage
        return None
    
class NPC(charactor):
    levels = (
        0, 1000, 3000, 6000, 10000, 15000,
        21000, 28000, 36000, 45000, 55000,
        66000, 78000, 91000, 105000, 120000,
        136000, 153000, 171000, 190000
    )
    flavor = (
        'height', 'weight', 'age', 'race', 'xp',
        'gender', 'charactor name', 'extra'
    )
    def __init__(self, listStat, listFlavor):
        super(NPC, self).__init__(listStat)
        self.Flavor = {}
        for n in range(len(NPC.flavor)):
            self.Flavor[NPC.flavor[n]] = listFlavor[n]

    def __repr__(self):
        stringy = super(NPC, self).__repr__()
        for entry in self.flavor:
            stringy += "FLAVOR " + entry + ": " + str(self.Flavor[entry]) + '\n'
        return stringy
        
    def level_up(self):
        #add BaB
        #add Saves
        #Add hit dice
        
        level = self.Stat['level']
        if NPC.levels[level] <= self.Flavor['xp']:
            level += 1
        if NPC.levels[level] <= self.Flavor['xp']:
            self.Flavor['xp'] = NPC.levels[level] - 1
        if NPC.levels[level] > self.Flavor['xp']:
            for levels in range(len(NPC.levels)):
                if self.Flavor['xp'] > NPC.levels[levels]:
                    continue
                else:
                    level = levels + 1
                    break
        self.Stat['level'] = level

    def level_up_check(self):
        check = False
        if NPC.levels[level] <= self.Flavor['xp']:
            check = True
        return check
    
    def add_xp(self, num):
        self.Flavor['xp'] += num
        self.level_up_check()
        return (self.Flavor['xp'], self.Stat['level'])

class PC(NPC):    
    def __init__(self, listStat, listFlavor, pc):        
        super(PC, self).__init__(listStat, listFlavor)
        self.Flavor['player name'] = pc

    def __repr__(self):
        stringy = super(PC, self).__repr__()
        return stringy

class Weapon(object):
    weapon_attr = (
        'name', 'attack bonus', 'damage',
        'critical' , 'range', 'type', 'extra'
    )
    def __init__(self, weapon_attributes):
        self.info = {}
        for n in range(len(Weapon.weapon_attr)):
            attr = Weapon.weapon_attr[n]
            self.info[attr] = weapon_attributes[n]
    def __repr__(self):
        return self.info['name']

stat = [1] * 18
stat.append('human')
stat.append('LG')
flavor =[5.9, 120, 137, 'elf', 0, 'male', 'havok', 'silver hair, red eyes']
player = 'Dustin'
dustin = PC(stat, flavor, player)
weapon = ['longsword', 2, '1d8', 'x3/19-20', 0, 'slashing', 'lol']
