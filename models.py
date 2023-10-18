class Player:
    def __init__(self, id):
        self.id = id
        self.level = 0
        self.money = {'money':0, 'gold':0, 'energy':0}
        self.state_leader = None
        self.commander = None
        self.rating = 0
        self.perks = {'str':0, 'edu':0, 'end':0}
        self.region = None
        self.state = None
        self.residency = None
        self.workpermits = {}
        self.governor = None
        self.economics = None
        self.foreign = None
        self.party = None
    
    def set_level(self, value):
        self.level = value

    def set_money(self, element, value):
        self.money[element] = value
    
    def set_state_leader(self, value):
        self.state_leader = value

    def set_commander(self, value):
        self.commander = value

    def set_rating(self, value):
        self.rating = value

    def set_perk(self, element, value):
        self.perks[element] = value

    def set_perks(self, str, edu, end):
        self.perks['str'] = str
        self.perks['edu'] = edu
        self.perks['end'] = end
    
    def set_region(self, value):
        self.region = value
    
    def set_state(self, value):
        self.state = value
    
    def set_residency(self, value):
        self.residency = value
    
    def set_workpermits(self, value):
        self.workpermits = value
    
    def set_governor(self, value):
        self.governor = value
    
    def set_economics(self, value):
        self.economics = value
    
    def set_foreign(self, value):
        self.foreign = value
    
    def set_party(self, value):
        self.party = value
    
    def __str__(self):
        return str(self.id)

players = {0: Player(0)}

def get_player(id):
    if id in players:
        return players[id]
    else:
        player = Player(id)
        players[id] = player
        return player


class State:
    def __init__(self, id):
        self.id = id
        self.leader = None
        self.commander = None
        self.economics = None
        self.foreign = None
        self.government_form = ''
        self.autonomies = []
        self.regions = []
        self.num_of_regions = 0
        self.citizens = []
        self.num_of_citizens = 0
        self.residents = []
        self.num_of_residents = 0
        self.budget = {
            'money': 0,
            'gold': 0,
            'oil': 0,
            'ore': 0,
            'uranium': 0,
            'diamonds': 0,
            }
        self.wars = []
        self.borders = ''

    def set_leader(self, value):
        self.leader = value
    
    def set_commander(self, value):
        self.commander = value
    
    def set_economics(self, value):
        self.economics = value
    
    def set_foreign(self, value):
        self.foreign = value
    
    def set_government_form(self, value):
        self.government_form = value
    
    def set_budget(self, element, value):
        self.budget[element] = value
    
    def set_borders(self, value):
        self.borders = value
    
    def set_wars(self, value):
        self.wars = value
    
    def add_war(self, value):
        self.wars.append(value)
    
    def set_regions(self, value):
        self.regions = value
    
    def set_num_of_regions(self, value):
        self.num_of_regions = value
    
    def set_citizens(self, value):
        self.citizens = value
    
    def set_num_of_citizens(self, value):
        self.num_of_citizens = value
    
    def set_residents(self, value):
        self.residents = value
    
    def set_num_of_residents(self, value):
        self.num_of_residents = value
    
    def set_autonomies(self, value):
        self.autonomies = value
    
    def __str__(self):
        return str(self.id)

class Autonomy:
    def __init__(self, id):
        self.id = id
        self.governor = players[0]
        self.regions = []
        self.budget = {
            'money': 0,
            'gold': 0,
            'oil': 0,
            'ore': 0,
            'uranium': 0,
            'diamonds': 0,
            }
    
    def set_governor(self, value):
        self.governor = value
    
    def set_regions(self, value):
        self.regions = value
    
    def set_budget(self, element, value):
        self.budget[element] = value
    
    def __str__(self):
        return str(self.id)

class Region:
    def __init__(self, id):
        self.id = id
        self.state = None
        self.autonomy = None
        self.buildings = {
            'military academy': 0,
            'hospital': 0,
            'military base': 0,
            'school': 0,
            'missile system': 0,
            'sea port': 0,
            'power plant': 0,
            'space port': 0,
            'airport': 0,
            'house fund': 0
        }
        self.rating = 0
        self.residents = []
        self.num_of_residents = 0
        self.citizens = []
        self.num_of_citizens = 0
        self.initial_attack_damage = 0
        self.initial_defend_damage = 0
        self.tax = 0
        self.market_tax = 0
        self.sea_access = False
        self.resources = {
            'gold': 0,
            'oil': 0,
            'ore': 0,
            'uranium': 0,
            'diamonds': 0,
        }
        self.deep_resources = {
            'gold': 0,
            'oil': 0,
            'ore': 0,
            'uranium': 0,
            'diamonds': 0,
        }
        self.indexes = {
            'health': 0,
            'military': 0,
            'education': 0,
            'development': 0,
        }
        self.border_regions = []
    
    def set_state(self, value):
        self.state = value
    
    def set_autonomy(self, value):
        self.autonomy = value
    
    def set_buildings(self, element, value):
        self.buildings[element] = value
    
    def set_rating(self, value):
        self.rating = value

    def set_residents(self, value):
        self.residents = value
    
    def set_num_of_residents(self, value):
        self.num_of_residents = value
    
    def set_citizens(self, value):
        self.citizens = value
    
    def set_num_of_citizens(self, value):
        self.num_of_citizens = value
    
    def set_initial_attack_damage(self, value):
        self.initial_attack_damage = value
    
    def set_initial_defend_damage(self, value):
        self.initial_defend_damage = value
    
    def set_tax(self, value):
        self.tax = value

    def set_market_tax(self, value):
        self.market_tax = value

    def set_sea_access(self, value):
        self.sea_access = value

    def set_resources(self, element, value):
        self.resources[element] = value

    def set_deep_resources(self, element, value):
        self.deep_resources[element] = value

    def set_indexes(self, element, value):
        self.indexes[element] = value
    
    def set_border_regions(self, value):
        self.border_regions = value
    
    def __str__(self):
        return str(self.id)

states = {0: State(0)}
autonomies = {0: Autonomy(0)}
regions = {0: Region(0)}

def get_state(id):
    if id in states:
        return states[id]
    else:
        state = State(id)
        states[id] = state
        return state

def get_region(id):
    if id in regions:
        return regions[id]
    else:
        region = Region(id)
        regions[id] = region
        return region

def get_autonomy(id):
    if id in autonomies:
        return autonomies[id]
    else:
        autonomy = Autonomy(id)
        autonomies[id] = autonomy
        return autonomy


class Party:
    def __init__(self, id):
        self.id = id
        self.leader = None
        self.location = None
        self.secretaries = []
        self.members = []

    def set_leader(self, value):
        self.leader = value

    def set_location(self, value):
        self.location = value

    def set_secretaries(self, value):
        self.secretaries = value

    def set_members(self, value):
        self.members = value
    
    def __str__(self):
        return str(self.id)

parties = {0: Party(0)}

def get_party(id):
    if id in parties:
        return parties[id]
    else:
        party = Party(id)
        parties[id] = party
        return party