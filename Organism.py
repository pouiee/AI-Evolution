import random

org_compendium = []
food_compendium = []


def status_report():
    print('organisms alive: ' + str(len(org_compendium)))
    print('food available: ' + str(len(food_compendium)))


def pass_time(env, turns, elapsed_time=0):
    while turns > 0:
        env.food_grow()
        for org in org_compendium:
            org.move(env)
            if org.alive:
                org.attrition(env)
                org.set_age(1)
        reproduce(env)
        env.print_env()
        turns -= 1
        elapsed_time += 1
        if len(org_compendium) <= 0:
            print('death has overcome life at turn ' + str(elapsed_time))
            return
        print('********** ' + str(elapsed_time) + ' turns **********')
    env.print_env()


def output_org_list():
    for org in org_compendium:
        print(org.features)


def output_food_list():
    for food in food_compendium:
        food.to_string()


# genome/ reproduction functions
def create_first_genome():
    genome = []
    for i in range(4):
        genome.append(random.choice(['AB', 'BA']))
    return genome


def interpret_genome(genome=None):
    if genome is None:
        genome = create_first_genome()
    traits = {}
    behavior_dict = {
        'AB': 'Hostile',
        'BA': 'Docile',
        'BB': 'Not Viable'
    }
    size_dict = {
        'AB': 'Large',
        'BA': 'Small',
        'BB': 'Not Viable'
    }
    agility_dict = {
        'AB': 'Fast',
        'BA': 'Slow',
        'BB': 'Not Viable'
    }
    mutation_dict = {
        'AB': .2,
        'BA': .5,
        'BB': 'Not Viable'
    }
    traits['Behavior'] = behavior_dict.get(genome[0])
    traits['Size'] = size_dict.get(genome[1])
    traits['Agility'] = agility_dict.get(genome[2])
    traits['Mutation Chance'] = mutation_dict.get(genome[3])
    return traits


def mutate(genome):
    mutated_genome = []
    mutation_chance = interpret_genome(genome).get('Mutation Chance')
    for gene in range(len(genome) - 1):
        chance = random.uniform(0.0, mutation_chance)
        if chance < mutation_chance / 4:
            mutated_genome.append('BB')
        elif chance <= mutation_chance / 2:
            if genome == 'AB':
                mutated_genome.append('BA')
            else:
                mutated_genome.append('AB')
        else:
            mutated_genome.append(genome[gene])
    return genome


def inherit(mom_1, mom_2):
    new_genome = []
    for i in range(len(mom_1.genome)):
        if random.randint(0, 10) > 5:
            new_genome.insert(i, mom_1.genome[i])
        else:
            new_genome.insert(i, mom_2.genome[i])
    return mutate(new_genome)


# interaction with other organisms (consumption and reproduction)
def reproduce(env):
    temp_space = []
    for space in env.display:
        temp_space = [obj for obj in space if obj is Organism]
    if len(temp_space) >= 2:
        for i in range(len(temp_space)):
            if (i + 1) % 2 == 0:
                print(str(find_org(temp_space[i])) + ' and '
                      + str(find_org(temp_space[i - 1])) + ' are attempting reproduction')
                Organism(env, find_org(temp_space[i]).position,
                         inherit(find_org(temp_space[i]), find_org(temp_space[i - 1])))


def hunt(predator, prey):
    prey_value = prey.features['Health']
    while predator.alive and prey.alive:
        predator.hit(prey)
        if prey.alive:
            prey.hit(predator)
    if predator.alive:
        predator.set_health(prey_value)


def consume(env, org, food):
    if food in food_compendium:
        print(str(org.id) + ' foraged')
        if not org.features['Hostile']:
            org.set_health(food.value)
        else:
            org.set_health(food.value / 2)
        env.remove_food(food)
    elif org.features['Hostile'] and food in org_compendium and org != food:
        hunt(org, food)
        if not food.alive:
            env.remove_org(food)


# movement helper functions
def is_occupied(check_pos):
    if get_at_pos(check_pos):
        return True
    return False


def find_org(org_id):
    if org_id is int:
        for org in org_compendium:
            if org_id == org.id:
                return org
    elif org_id is str:
        for food in food_compendium:
            if org_id == food.id:
                return food


def get_at_pos(position):
    for org in org_compendium:
        if position == org.position:
            return org
    for food in food_compendium:
        if position == food.position:
            return food
    return None


def get_food_at_pos(hungry_org, position):
    if hungry_org.features['Hostile']:
        for org in org_compendium:
            if position == org.position and hungry_org != org:
                return org
    else:
        for food in food_compendium:
            if position == food.position:
                return food


class Organism:

    def __init__(self, env, pos, genome=create_first_genome()):
        self.position = pos
        self.genome = genome
        self.id = len(org_compendium) * 2
        org_compendium.insert(self.id, self)
        self.features = interpret_genome(genome)
        self.initialize_features()
        self.alive = True
        env.add_org(self)

    # Organism traits/ inherent properties
    def to_string(self):
        print('Id: {} Health: {} Position: {} Is Alive: {}'
              .format(self.id, self.features['Health'], self.position, self.alive))

    def initialize_features(self):
        self.initialize_behavior()
        self.initialize_health()
        self.initialize_attack()
        self.initialize_speed()
        self.features['Age'] = 0

    def initialize_speed(self):
        if self.features['Agility'] == 'Fast':
            self.features['Speed'] = 2
        else:
            self.features['Speed'] = 1

    def initialize_health(self):
        if self.features['Size'] == 'Large':
            self.features['Health'] = random.randint(75, 100)
        else:
            self.features['Health'] = random.randint(30, 55)

    def initialize_attack(self):
        if self.features['Size'] == 'Large':
            self.features['Attack'] = random.randint(35, 60)
        else:
            self.features['Attack'] = random.randint(15, 25)

    def initialize_behavior(self):
        if self.features['Behavior'] == 'Hostile':
            self.features['Hostile'] = True
        else:
            self.features['Hostile'] = False

    def set_position(self, new_position):
        self.position = new_position

    def set_health(self, health_change):
        self.features['Health'] += health_change

    def set_age(self, age_change):
        self.features['Age'] += age_change

    def attrition(self, env):
        if self.features['Age'] > 50:
            self.set_health(-10)
        elif self.features['Age'] > 25:
            self.set_health(-5)
        elif self.features['Age'] > 10:
            self.set_health(-2)
        else:
            self.set_health(-1)
        if self.features['Health'] <= 0:
            print(str(self.id) + ' starved')
            env.remove_org(self)

    # Organism move and fighting functions
    def move(self, env):
        start = self.position
        coin_flip = random.randint(0, 1)
        if coin_flip == 1:
            direction = 1
        else:
            direction = -1
        if len(env.display[start]) >= 2:
            consume(env, self, get_food_at_pos(self, start))
            if not self.alive:
                env.remove_org(self)
                return
            return
        destination = self.position + direction * self.features['Speed']
        if destination >= env.length or destination < 0:
            return
        elif is_occupied(destination):
            consume(env, self, get_at_pos(destination))
            if self.alive:
                env.modify_pos(self, start, destination)
            else:
                env.remove_org(self)
        else:
            env.modify_pos(self, start, destination)

    def hit(self, target):
        target.set_health(-1 * self.features['Attack'])
        if target.features['Health'] <= 0:
            print(str(target.id) + ' was killed')
            target.alive = False


class Food:

    def __init__(self, env, food_pos):
        self.position = food_pos
        self.id = len(food_compendium) * 2 + 1
        food_compendium.insert(self.id, self)
        self.value = random.randint(10, 15)
        env.add_food(self)
        self.features = {'Hostile': False, 'Age': 0}

    def get_older(self):
        self.features['Age'] += 1

    def to_string(self):
        print('Id: {} Food Value: {} Position: {}'
              .format(self.id, self.value, self.position))


class Environment:

    def __init__(self, env_len):
        self.length = env_len
        self.display = [[] for _ in range(env_len)]

    def add_food(self, food):
        self.display[food.position].append(food.id)

    def remove_food(self, food):
        self.display[food.position].remove(food.id)
        food_compendium.remove(food)

    def add_org(self, org):
        self.display[org.position].append(org.id)

    def remove_org(self, org):
        self.display[org.position].remove(org.id)
        org_compendium.remove(org)

    def modify_pos(self, org, initial_pos, final_pos):
        org.set_position(final_pos)
        self.display[final_pos].append(org.id)
        self.display[initial_pos].remove(org.id)

    def print_env(self):
        print(self.display)

    def food_grow(self):
        species = len(org_compendium)
        if species == 0:
            for i in range(int(self.length / 4)):
                Food(self, random.randint(0, self.length - 1))
        else:
            for i in range(int(self.length / random.randint(5, 10))):
                Food(self, random.randint(0, self.length - 1))
