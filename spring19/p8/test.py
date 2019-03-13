# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math, ast

PASS = "PASS"
TEXT_FORMAT = "text"
Question = collections.namedtuple("Question", ["number", "weight", "format"])




questions = [
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),    
]
question_nums = set([q.number for q in questions])


# JSON and plaintext values
expected_json = {
    "1": {'nm0000131': 'John Cusack',
                  'nm0000154': 'Mel Gibson',
                  'nm0000163': 'Dustin Hoffman',
                  'nm0000418': 'Danny Glover',
                  'nm0000432': 'Gene Hackman',
                  'nm0000997': 'Gary Busey',
                  'nm0001149': 'Richard Donner',
                  'nm0001219': 'Gary Fleder',
                  'nm0752751': 'Mitchell Ryan',
                  'tt0313542': 'Runaway Jury',
                  'tt0093409': 'Lethal Weapon'},
    "2": 'Runaway Jury',
    "3": ['Runaway Jury', 'Lethal Weapon'],
    "4": ['nm0000997', 'nm0001219'],
    "5":[{'title': 'tt0313542',
  'year': 2003,
  'rating': 7.1,
  'directors': ['nm0001219'],
  'actors': ['nm0000131', 'nm0000432', 'nm0000163'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'tt0093409',
  'year': 1987,
  'rating': 7.6,
  'directors': ['nm0001149'],
  'actors': ['nm0000154', 'nm0000418', 'nm0000997', 'nm0752751'],
  'genres': ['Action', 'Crime', 'Thriller']}],
    "6":3,
    "7":'nm0752751',
    "8":'Runaway Jury',
    "9":['Richard Donner'],
    "10":['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
    "11":[{'title': 'Runaway Jury',
  'year': 2003,
  'rating': 7.1,
  'directors': ['Gary Fleder'],
  'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'Lethal Weapon',
  'year': 1987,
  'rating': 7.6,
  'directors': ['Richard Donner'],
  'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
  'genres': ['Action', 'Crime', 'Thriller']}],
    "12":[('Martin Ritt', 32),
 ('Eldar Ryazanov', 31),
 ('Cecil B. DeMille', 30),
 ('Lee H. Katzin', 30),
 ('John Huston', 30),
 ('Robert Siodmak', 30),
 ('Richard Thorpe', 29)],
    "13":21,
    "14":28,
    "15":1996,
    "16":['15 Minutes',
 '2012',
 '300',
 '3000 Miles to Graceland',
 '7 Men from Now',
 '8 Million Ways to Die',
 'A Colt Is My Passport',
 'A Cry in the Wild',
 'A Girl in Every Port',
 'Abstraction',
 'Across 110th Street',
 'Against All Flags',
 'Against All Odds',
 'Alien Nation',
 'American Hero',
 'American Sniper',
 'Another Meltdown',
 'Arsenal',
 'Attack on Titan: Part 1',
 'Avenging Angelo',
 'Babylon 5: Thirdspace',
 'Backdraft',
 'Bad Ass 3: Bad Asses on the Bayou',
 'Bandido!',
 'Batman',
 'Batman Begins',
 'Beau Geste',
 'Best Seller',
 'Best of the Best',
 'Best of the Best II',
 'Betrayal',
 'Beyond the Ring',
 'Beyond the Trophy',
 'Big Bad John',
 'Big Trouble in Little China',
 'Blind Justice',
 'Blizhniy Boy: The Ultimate Fighter',
 'Blood Alley',
 'Blood and Sweat',
 'Blood on the Moon',
 'Bloodsucking Bastards',
 'Blowing Wild',
 'Blown Away',
 'Blue Steel',
 'Brannigan',
 'Breakdown',
 'Breaking Point',
 'Bulletproof',
 'Camino',
 'Capricorn One',
 'Cell',
 'Children of Wax',
 'City Beneath the Sea',
 'Cloudy with a Chance of Meatballs',
 'Come Back Charleston Blue',
 'Command Decision',
 'Con Air',
 'Confessions of a Pit Fighter',
 'Conflict of Interest',
 'Conquest of the Planet of the Apes',
 'Convicted',
 'Convoy',
 'D.C. Cab',
 'Darc',
 'Dark Angel',
 'Deaden',
 'Death Proof',
 'Den of Lions',
 'Depth Charge',
 'Destruction Los Angeles',
 'Dick Tracy',
 'Dog Tags',
 'Dragon Ball Z: Bojack Unbound',
 'Dragon Ball: The Path to Power',
 'DragonHeart',
 'Dreamscape',
 'Dunkirk',
 'East of Sumatra',
 'Enemy Mine',
 'Eraser',
 'Escape from L.A.',
 'Escape from New York',
 'Executive Decision',
 'Exists',
 'Extortion',
 'Facade',
 'Fantastic Four',
 'Fastest',
 'Federal Protection',
 'Final Chapter: Walking Tall',
 'Flight Lieutenant',
 'Flight of the Intruder',
 'Flight of the Phoenix',
 'Flying Leathernecks',
 'Flying Tigers',
 'For the Love of Money',
 'Foreign Correspondent',
 'Fort Apache',
 'Freebie and the Bean',
 'Freefall',
 'Freelancers',
 'G.I. Joe: The Rise of Cobra',
 'Gang Related',
 'Git Along Little Dogies',
 'Grindhouse',
 'Grosse Pointe Blank',
 'Guido',
 'Guns for San Sebastian',
 'Hatari!',
 'Haywire',
 'Heaven Knows, Mr. Allison',
 'Heist',
 'Hell or High Water',
 "Hell's Belles",
 'Hellfighters',
 'Hercules and the Amazon Women',
 'Hercules: The Legendary Journeys - Hercules and the Lost Kingdom',
 'High Risk',
 'His Kind of Woman',
 "Hitman's Run",
 'Huo yun chuan qi',
 'I Cover the War!',
 'In Old California',
 'Inception',
 'Innerspace',
 'Iron Man',
 "It's a Mad Mad Mad Mad World",
 "Jake's Road",
 'Jane Got a Gun',
 'Jersey Justice',
 'Jet Pilot',
 'Judge Dredd',
 'Keeper of the City',
 'Kidnapped',
 'Killing Season',
 'Kin',
 'Lara Croft: Tomb Raider',
 'Last Run',
 'Last of the Comanches',
 'Legion',
 'Lethal Weapon',
 'Lethal Weapon 2',
 'Lethal Weapon 3',
 'Lethal Weapon 4',
 'Lolly-Madonna XXX',
 'Lost Command',
 'Machete',
 'Mad Max: Fury Road',
 'Man of the Forest',
 'McQ',
 'Mercy Streets',
 'Mexican Sunrise',
 'Midnight Ride',
 'Midnight Run',
 'Midway',
 'My Little Pony: The Movie',
 'My Outlaw Brother',
 'Nevada',
 'Nine Lives',
 'Nowhere Land',
 'OSS 117: Cairo, Nest of Spies',
 'Operation Dumbo Drop',
 'Pals of the Saddle',
 'Pandemic',
 'Panic in the Skies',
 'Paradise Canyon',
 'Past Perfect',
 'Pit Stop',
 'Plunder of the Sun',
 'Poseidon',
 'Power 98',
 'Predator 2',
 'Quick-draw Okatsu',
 'R.I.P.D.',
 'Race Against Time',
 'Rage at Dawn',
 'Ransom',
 'Reap the Wild Wind',
 'Red Line 7000',
 'Red River',
 'Restraining Order',
 'Revelation Road 2: The Sea of Glass and Fire',
 'Revelation Road: The Beginning of the End',
 'Revenge',
 'Riki-Oh: The Story of Ricky',
 'Rio 70',
 'Rio Bravo',
 'River of No Return',
 'Rollercoaster',
 'Rough Air: Danger on Flight 534',
 'Run All Night',
 'Run and Kill',
 'Runaway',
 'Runaway Train',
 'Samurai Cop',
 'Samurai Wolf II',
 'Sands of Iwo Jima',
 'Santa Fe Stampede',
 'Serenity',
 'Seventh Son',
 'Shadows in Paradise',
 'Shaft in Africa',
 'Shinsengumi: Assassins of Honor',
 'Shooter',
 'Showtime',
 'Sidekicks',
 'Silk',
 'Silverado',
 'Singularity',
 'Skin Traffik',
 'Smokey and the Bandit II',
 'Snipes',
 'Soldier',
 'Sometimes a Great Notion',
 'Somewhere in Sonora',
 'Souls at Sea',
 'Spawn of the North',
 'Spy Kids 2: Island of Lost Dreams',
 'Stand by for Action',
 'Star Trek III: The Search for Spock',
 'Star Wars: Episode I - The Phantom Menace',
 'Star Wars: Episode II - Attack of the Clones',
 'Star Wars: Episode III - Revenge of the Sith',
 'Starkweather',
 'Stroker Ace',
 'Sugarfoot',
 'Superman II',
 'Sweet Justice',
 'TRON',
 'TRON: Legacy',
 'Tango & Cash',
 'Texas Cyclone',
 'Texas Terror',
 'The Ambassador',
 'The Ambulance',
 'The Big Chance',
 'The Big Wheel',
 'The Bounty Hunter',
 'The Butcher',
 'The Chaser',
 'The Comancheros',
 'The Crimson Ghost',
 'The Dark Knight',
 'The Dark Knight Rises',
 'The Day After Tomorrow',
 'The Deadly Tower',
 'The Desperadoes',
 'The Destructors',
 'The Don Is Dead',
 'The Enemy Below',
 'The Fan',
 'The Guns of Navarone',
 'The Heir Apparent: Largo Winch',
 'The High and the Mighty',
 'The Hunley',
 'The Hunters',
 'The Hurricane Express',
 'The Immortals',
 'The Island',
 'The Killer Elite',
 'The Lone Ranger and the Lost City of Gold',
 'The Longest Day',
 'The Lost Capone',
 'The Lusty Men',
 'The Mark: Redemption',
 'The Matrix Reloaded',
 'The Mongols',
 'The New Frontier',
 'The Night Fighters',
 'The Outsider',
 'The Pope of Greenwich Village',
 'The Prince',
 'The Program',
 'The Return of Swamp Thing',
 'The Saint in London',
 'The Sea Chase',
 'The Secret Invasion',
 'The Shadow Men',
 'The Three Musketeers',
 'The Throwaways',
 'The Trail Beyond',
 'The Trouble with Spies',
 'The World in His Arms',
 'The Yakuza',
 'Thief',
 'Three Texas Steers',
 'Time Trackers',
 'Tombstone',
 'Tough Enough',
 'Tripwire',
 'Vantage Point',
 'Virginia City',
 'Wagon Wheels',
 'Wake Island',
 'Wake of the Red Witch',
 'War, Inc.',
 'White Lightning',
 'Wild Bill',
 'Young Billy Young'],
   "17":['11:59',
 '2 Bedroom 1 Bath',
 '3 Holes and a Smoking Gun',
 '3:10 to Yuma',
 'A Blade in the Dark',
 'A Cry in the Wild',
 'A Fatal Obsession',
 'A Killer in the Family',
 'A Vision of Murder: The Story of Donielle',
 'Advise & Consent',
 'American Violence',
 'Angels & Demons',
 'Another Meltdown',
 'Appointment in Honduras',
 'Arlington Road',
 'Arsenal',
 'Assignment: Paris',
 'At Any Price',
 'Bad Sister',
 'Bad Times at the El Royale',
 'Beneath the Darkness',
 'Blood Crime',
 'Blood Money',
 'Blowtorch',
 "Bluebeard's 10 Honeymoons",
 'BnB HELL',
 'Broken Embraces',
 'Broken Trust',
 'Calling All Police Cars',
 'Camino',
 'Cannibal Apocalypse',
 'Cape Fear',
 'Cape Fear',
 'Capricorn One',
 'Chappaquiddick',
 'Chernobyl Diaries',
 'City of Ghosts',
 'Class Warfare',
 'Cold Creek Manor',
 'Cold and Dark',
 'Complicity',
 'Con Air',
 'Cop Car',
 'Cop Land',
 'Countdown',
 'Crime Against Joe',
 'D.O.A.',
 'Darc',
 'Dark Angel',
 'Dark Blue',
 'Dark Was the Night',
 'Deadline',
 'Death Laid an Egg',
 'Death Proof',
 'Deathwatch',
 'Deliverance',
 'Den of Lions',
 'Depth Charge',
 'Descending Angel',
 "Devil's Due",
 'Digital Reaper',
 'Dog Eat Dog',
 'Domino One',
 'Drum',
 'Dying Room Only',
 'Eat',
 'Endangered Species',
 'Error in Judgment',
 'Executive Decision',
 'Experiment in Terror',
 'Eyes Wide Shut',
 'Eyes of Laura Mars',
 'Facade',
 'Fade to Black',
 'Fail-Safe',
 'Farewell, My Lovely',
 'Fatal Instinct',
 'Fate Is the Hunter',
 'Fear and Desire',
 'Fearless',
 'Fever',
 'Final Analysis',
 'Final Approach',
 'Flight of the Intruder',
 'Foreign Correspondent',
 'Full Moon',
 'Games',
 'Gotham',
 'Graves End',
 'Grindhouse',
 'Hangmen Also Die!',
 'Haywire',
 'Heat',
 "Heaven's Prisoners",
 'Heist',
 'Hell High',
 "Hell's Belles",
 'Honeymoon in Vegas',
 'Hostage Flight',
 'I Spit on Your Grave: Vengeance is Mine',
 'Identity',
 'Illusions',
 'In the Shadows',
 'Incident at Deception Ridge',
 'Insomnia',
 'Intoxicating',
 'Jagged Edge',
 "Jake's Road",
 'Jersey Justice',
 'Keeper of the City',
 'Kidnapped',
 'Killing Season',
 'Lady for a Night',
 'Lady in a Cage',
 'Lancer Spy',
 'Last Run',
 'Lethal Weapon',
 'Lethal Weapon 2',
 'Lethal Weapon 3',
 'Lethal Weapon 4',
 'Life in the Hole',
 'Limitless',
 'Listen',
 'Lonely Hearts',
 'Love, Cheat & Steal',
 'Luck of the Draw',
 'Lust Connection',
 "Ma Barker's Killer Brood",
 'Machete',
 'Madigan',
 'Madness',
 'Man Hunt',
 'Manson Family Vacation',
 'Mean Streets',
 'Memento',
 'Mexican Sunrise',
 'Midnight Ride',
 'Misery',
 'Mojave',
 'Night Has a Thousand Eyes',
 'Nightwatch',
 'One Good Turn',
 'One Shoe Makes It Murder',
 'Open Water 3: Cage Dive',
 'Pandemic',
 'Personal Column',
 'Poltergeist',
 'Portrait in Black',
 'Power 98',
 'Prime Suspect',
 'Project Solitude',
 'Purple Noon',
 'Q & A',
 'Question of Luck',
 'Rage in Heaven',
 'Ransom',
 'Raw Nerve',
 'Red Sheep',
 'Restraining Order',
 'Revenge',
 'Riki-Oh: The Story of Ricky',
 'Rough Air: Danger on Flight 534',
 'Roulette',
 'Rumors of Wars',
 'Runaway Jury',
 'Ryde',
 'Samurai Cop',
 'Saw',
 'Sensation',
 'Sleepers',
 'Slither',
 'Slow Burn',
 'Sorry, Wrong Number',
 "Soul's Midnight",
 'Stalked by My Doctor',
 'Stalked by My Doctor: The Return',
 'Starcrossed',
 'Stay',
 'Stealing Las Vegas',
 'Stone',
 'Stranded',
 'Stranger in the House',
 'Stranger on the Run',
 'Supernatural',
 'Surveillance',
 'Suspect',
 'Switchback',
 'Tennessee Waltz',
 'Terror on a Train',
 'The Air I Breathe',
 'The Alpha Caper',
 'The Ambassador',
 'The Art of the Steal',
 'The Bag Man',
 'The Big Heat',
 'The Brotherhood of the Bell',
 'The Butcher',
 'The Chaser',
 'The Contender',
 'The Cosmic Man',
 'The Da Vinci Code',
 'The Dark Knight Rises',
 'The Deadly Tower',
 'The Falcon Takes Over',
 'The Family',
 'The Gazebo',
 'The Ghost Writer',
 'The Good Shepherd',
 'The Grifters',
 'The Haunting Passion',
 'The Heir Apparent: Largo Winch',
 'The House of the Seven Gables',
 'The Impossible',
 'The Killer Elite',
 'The Last Mile',
 'The Mean Season',
 'The Money Trap',
 'The Night Walker',
 'The Prince',
 'The Raven',
 'The River Wild',
 'The Salamander',
 'The Score',
 'The Secret Agents',
 'The Serpent',
 'The Shadow Men',
 'The Shamrock Conspiracy',
 'The Sitter',
 'The Steam Experiment',
 'The Tall T',
 'The Throwaways',
 'The Untouchables',
 'The Walking Hills',
 'The Woman Who Sinned',
 'This World, Then the Fireworks',
 'Trial by Jury',
 'Tripwire',
 'Two for the Money',
 'Unconditional Love',
 'Undercurrent',
 'Victim of Desire',
 'Visitors of the Night',
 'Voyage',
 'War, Inc.',
 'Watch Me When I Kill',
 'We Need to Talk About Kevin',
 'Where Danger Lives',
 'Woman of Desire',
 'World Trade Center',
 "You Can't Have It"],
 "18":[(1921, 8.3), (1925, 8.2), (1919, 7.5), (1923, 7.3), (1962, 7.17)],
 "19":[(2013, 5.85), (2017, 5.84), (1935, 5.81), (2015, 5.79), (1934, 5.62)],
 "20":[(1928, 7.0),
 (1957, 6.91),
 (1947, 6.91),
 (1940, 6.9),
 (1918, 6.9),
 (1926, 6.9),
 (1985, 6.89),
 (1956, 6.88),
 (1948, 6.85)],


}
           
# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-301-test.ipynb'

    # re-execute it from the beginning
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook,encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = ''.join(actual_lines)
    actual = ast.literal_eval(actual)
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if extra:
                return "found unexpected entry in list: %s" % repr(list(extra)[0])
            elif missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
        except TypeError:
            # this happens when the list contains dicts.  Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    else:
        if expected != actual:
            expected_mismatch = True
            
    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    nb = rerun_notebook(orig_notebook)

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
