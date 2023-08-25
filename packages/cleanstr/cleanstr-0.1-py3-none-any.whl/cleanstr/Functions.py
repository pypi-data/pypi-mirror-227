def get_cleaned_alpha(s):
  ### remove special characters, numbers, punctuation etc
  import re
  return re.sub('[^A-Za-z]+', '', s) ## just keep the letters

def get_cleaned_numeric(s):
  ### just keep the numbers
  import re
  return re.sub('[^0-9]+', '', s)


def get_cleaned_int(s):
  ### find valid int, assume at most one decimal
  import re
  if isinstance(s,int):
      return s
  elif '.' in s:
      return int(s.split(".")[0])
  else:
      return int(re.sub('[^0-9]+', '', s))

def get_cleaned_alpha_numeric(s):
  ### just alpha and numeric
  import re
  return re.sub('[^A-Za-z0-9]+', '', s)

class cleanupName:

    def __init__(self):
      import nltk

      nltk.download('wordnet', quiet=True)
      nltk.download('punkt', quiet=True)
      nltk.download('averaged_perceptron_tagger', quiet=True)

      ## define lemmatizer

      self.lemmatizer=nltk.stem.WordNetLemmatizer()


    def _get_profane_words(self):

        profane_words_1=['4r5e', '5h1t', '5hit', 'len', 'a$$', 'a$$hole', 'a2m', 'a55', 'a55hole', 'a_s_s', 'adult', 'aeolus', 'ahole', 'amateur', 'anal', 'analprobe', 'anilingus', 'anus', 'ar5e', 'areola', 'areole', 'arrse', 'arse', 'arsehole', 'ass', 'ass-fucker', 'assbang', 'assbanged', 'assbangs', 'asses', 'assfuck', 'assfucker', 'assfukka', 'assh0le', 'asshat', 'assho1e', 'asshole', 'assholes', 'assmaster', 'assmucus ', 'assmunch', 'asswhole', 'asswipe', 'asswipes', 'autoerotic', 'azazel', 'azz', 'b!tch', 'b00bs', 'b17ch', 'b1tch', 'babe', 'babes', 'ballbag', 'ballsack', 'bang', 'bangbros', 'banger', 'bareback', 'barf', 'bastard', 'bastards', 'bawdy', 'beaner', 'beardedclam', 'beastial', 'beastiality', 'beatch', 'beater', 'beaver', 'beer', 'beeyotch', 'bellend', 'beotch', 'bestial', 'bestiality', 'bi+ch', 'biatch', 'bigtits', 'bimbo', 'bimbos', 'birdlock', 'bitch', 'bitched', 'bitcher', 'bitchers', 'bitches', 'bitchin', 'bitching', 'bitchy', 'bloody', 'blow', 'blowjob', 'blowjobs', 'blumpkin ', 'bod', 'bodily', 'boink', 'boiolas', 'bollock', 'bollocks', 'bollok', 'bone', 'boned', 'boner', 'boners', 'bong', 'boob', 'boobies', 'boobs', 'booby', 'booger', 'bookie', 'booobs', 'boooobs', 'booooobs', 'booooooobs', 'bootee', 'bootie', 'booty', 'booze', 'boozer', 'boozy', 'bosom', 'bosomy', 'bowel', 'bowels', 'bra', 'brassiere', 'breast', 'breasts', 'buceta', 'bugger', 'bukkake', 'bullshit', 'bullshits', 'bullshitted', 'bullturds', 'bum', 'bung', 'busty', 'butt', 'buttfuck', 'buttfucker', 'butthole', 'buttmuch', 'buttplug', 'c-0-c-k', 'c-o-c-k', 'c-u-n-t', 'c.0.c.k', 'c.o.c.k.', 'c.u.n.t', 'c0ck', 'c0cksucker', 'caca', 'cahone', 'cameltoe', 'carpetmuncher', 'cawk', 'cervix', 'chinc', 'chincs', 'chink', 'choade ', 'chode', 'chodes', 'cipa', 'cl1t', 'climax', 'clit', 'clitoris', 'clitorus', 'clits', 'clitty', 'clusterfuck', 'cnut', 'cocain', 'cocaine', 'cock', 'cock-sucker', 'cockblock', 'cockface', 'cockhead', 'cockholster', 'cockknocker', 'cockmunch', 'cockmuncher', 'cocks', 'cocksmoker', 'cocksuck', 'cocksucked', 'cocksucker', 'cocksucking', 'cocksucks', 'cocksuka', 'cocksukka', 'coital', 'cok', 'cokmuncher', 'coksucka', 'commie', 'condom', 'corksucker', 'cornhole ', 'crack', 'cracker', 'crackwhore', 'crap', 'crappy', 'cum', 'cumdump ', 'cummer', 'cummin', 'cumming', 'cums', 'cumshot', 'cumshots', 'cumslut', 'cumstain', 'cunilingus', 'cunillingus', 'cunnilingus', 'cunny', 'cunt', 'cunt-struck ', 'cuntbag ', 'cuntface', 'cunthunter', 'cuntlick', 'cuntlick ', 'cuntlicker', 'cuntlicker ', 'cuntlicking ', 'cunts', 'cuntsicle ', 'cyalis', 'cyberfuc', 'cyberfuck ', 'cyberfucked', 'cyberfucker', 'cyberfuckers', 'cyberfucking', 'd0ng', 'd0uch3', 'd0uche', 'd1ck', 'd1ld0', 'd1ldo', 'dago', 'dagos', 'dammit', 'damn', 'damned', 'damnit', 'dawgie-style', 'dick', 'dick-ish', 'dickbag', 'dickdipper', 'dickface', 'dickflipper', 'dickhead', 'dickheads', 'dickish', 'dickripper', 'dicksipper', 'dickweed', 'dickwhipper', 'dickzipper', 'diddle', 'dike', 'dildo', 'dildos', 'diligaf', 'dillweed', 'dimwit', 'dingle', 'dink', 'dinks', 'dipship', 'dirsa', 'dlck', 'dog-fucker', 'doggie-style', 'doggiestyle', 'doggin', 'dogging', 'doggy-style', 'donkeyribber', 'doofus', 'doosh', 'dopey', 'douch3', 'douche', 'douchebag', 'douchebags', 'douchey', 'drunk', 'duche', 'dumass', 'dumbass', 'dumbasses', 'dummy', 'dyke', 'dykes', 'ejaculate', 'ejaculated', 'ejaculates', 'ejaculating', 'ejaculatings', 'ejaculation', 'ejakulate', 'enlargement', 'erect', 'erection', 'erotic', 'essohbee', 'extacy', 'extasy', 'f-u-c-k', 'f.u.c.k', 'f4nny', 'f_u_c_k', 'facial ', 'fack', 'fag', 'fagg', 'fagged', 'fagging', 'faggit', 'faggitt', 'faggot', 'faggs', 'fagot', 'fagots', 'fags', 'faig', 'faigt', 'fanny', 'fannybandit', 'fannyflaps', 'fannyfucker', 'fanyy', 'fart', 'fartknocker', 'fat', 'fatass', 'fcuk', 'fcuker', 'fcuking', 'feck', 'fecker', 'felch', 'felcher', 'felching', 'fellate', 'fellatio', 'feltch', 'feltcher', 'fingerfuck', 'fingerfucked', 'fingerfucker ', 'fingerfuckers', 'fingerfucking', 'fingerfucks', 'fisted', 'fistfuck', 'fistfucked', 'fistfucker ', 'fistfuckers', 'fistfucking', 'fistfuckings', 'fistfucks', 'fisting', 'fisty', 'flange', 'floozy', 'foad', 'fondle', 'foobar', 'fook', 'fooker', 'foreskin', 'freex', 'frigg', 'frigga', 'fubar', 'fuck', 'fuck ', 'fuck-ass ', 'fuck-bitch ', 'fuck-tard', 'fucka', 'fuckass', 'fucked', 'fucker', 'fuckers', 'fuckface', 'fuckhead', 'fuckheads', 'fuckin', 'fucking', 'fuckings', 'fuckingshitmotherfucker', 'fuckme', 'fuckmeat ', 'fucknugget', 'fucknut', 'fuckoff', 'fucks', 'fucktard', 'fucktoy ', 'fuckup', 'fuckwad', 'fuckwhit', 'fuckwit', 'fudgepacker', 'fuk', 'fuker', 'fukker', 'fukkin', 'fuks', 'fukwhit', 'fukwit', 'fux', 'fux0r', 'fvck', 'fxck', 'g-spot', 'gae', 'gai', 'gang-bang ', 'gangbang', 'gangbang ', 'gangbanged', 'gangbangs', 'ganja', 'gay', 'gaylord', 'gays', 'gaysex', 'gey', 'gfy', 'ghay', 'ghey', 'gigolo', 'glans', 'goatse', 'god', 'god-dam', 'god-damned', 'godamn', 'godamnit', 'goddam', 'goddammit', 'goddamn', 'goddamned', 'goldenshower', 'gonad', 'gonads', 'gook', 'gooks', 'gringo', 'gspot', 'gtfo', 'guido', 'h0m0', 'h0mo', 'handjob', 'hardcoresex', 'he11', 'hebe', 'heeb', 'hell', 'hemp', 'heroin', 'herp', 'herpes', 'herpy', 'heshe', 'hitler', 'hiv', 'hoar', 'hoare', 'hobag', 'hoer', 'hom0', 'homey', 'homo', 'homoerotic', 'homoey', 'honky', 'hooch', 'hookah', 'hooker', 'hoor', 'hootch', 'hooter', 'hooters']
        profane_words_2=['hore', 'horniest', 'horny', 'hotsex', 'hump', 'humped', 'humping', 'hymen', 'inbred', 'incest', 'injun', 'j3rk0ff', 'jack-off', 'jackass', 'jackhole', 'jackoff', 'jap', 'japs', 'jerk', 'jerk-off', 'jerk0ff', 'jerked', 'jerkoff', 'jism', 'jiz', 'jizm', 'jizz', 'jizzed', 'junkie', 'junky', 'kawk', 'kike', 'kikes', 'kill', 'kinky', 'kkk', 'klan', 'knob', 'knobead', 'knobed', 'knobend', 'knobhead', 'knobjocky', 'knobjokey', 'kock', 'kondum', 'kondums', 'kooch', 'kooches', 'kootch', 'kraut', 'kum', 'kummer', 'kumming', 'kums', 'kunilingus', 'kwif ', 'kyke', 'l3i+ch', 'l3itch', 'labia', 'lech', 'leper', 'lesbians', 'lesbo', 'lesbos', 'lez', 'lezbian', 'lezbians', 'lezbo', 'lezbos', 'lezzie', 'lezzies', 'lezzy', 'lmao', 'lmfao', 'loin', 'loins', 'lube', 'lust', 'lusting', 'lusty', 'm-fucking', 'm0f0', 'm0fo', 'm45terbate', 'ma5terb8', 'ma5terbate', 'mafugly ', 'mams', 'masochist', 'massa', 'master-bate', 'masterb8', 'masterbat*', 'masterbat3', 'masterbate', 'masterbating', 'masterbation', 'masterbations', 'masturbate', 'masturbating', 'masturbation', 'menses', 'menstruate', 'menstruation', 'meth', 'mo-fo', 'mof0', 'mofo', 'molest', 'moolie', 'moron', 'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked', 'mothafucker', 'mothafuckers', 'mothafuckin', 'mothafucking', 'mothafuckings', 'mothafucks', 'motherfuck', 'motherfucka', 'motherfucked', 'motherfucker', 'motherfuckers', 'motherfuckin', 'motherfucking', 'motherfuckings', 'motherfuckka', 'motherfucks', 'mtherfucker', 'mthrfucker', 'mthrfucking', 'muff', 'muffdiver', 'murder', 'mutha', 'muthafecker', 'muthafuckaz', 'muthafucker', 'muthafuckker', 'muther', 'mutherfucker', 'mutherfucking', 'muthrfucking', 'n1gga', 'n1gger', 'nad', 'nads', 'naked', 'napalm', 'nappy', 'nazi', 'nazism', 'negro', 'nigg3r', 'nigg4h', 'nigga', 'niggah', 'niggas', 'niggaz', 'nigger', 'niggers', 'niggle', 'niglet', 'nimrod', 'ninny', 'nipple', 'ngo', 'nob', 'nobhead', 'nobjocky', 'nobjokey', 'nooky', 'numbnuts', 'nutsack', 'nympho', 'omg', 'opiate', 'opium', 'oral', 'orally', 'organ', 'orgasim ', 'orgasims ', 'orgasm', 'orgasmic', 'orgasms ', 'orgies', 'orgy', 'ovary', 'ovum', 'ovums', 'p.u.s.s.y.', 'p0rn', 'paddy', 'paki', 'pantie', 'panties', 'panty', 'pastie', 'pasty', 'pawn', 'pcp', 'pecker', 'pedo', 'pedophile', 'pedophilia', 'pedophiliac', 'pee', 'peepee', 'penetrate', 'penetration', 'penial', 'penile', 'penis', 'penisfucker', 'perversion', 'peyote', 'phalli', 'phallic', 'phonesex', 'phuck', 'phuk', 'phuked', 'phuking', 'phukked', 'phukking', 'phuks', 'phuq', 'pigfucker', 'pillowbiter', 'pimp', 'pimpis', 'pinko', 'piss', 'piss-off', 'pissed', 'pisser', 'pissers', 'pisses ', 'pissflaps', 'pissin', 'pissing', 'pissoff', 'pissoff ', 'pms', 'polack', 'pollock', 'poon', 'poontang', 'poop', 'porn', 'porno', 'pornography', 'pornos', 'pot', 'potty', 'prick', 'pricks', 'prig', 'pron', 'prostitute', 'prude', 'pube', 'pubic', 'pubis', 'punkass', 'punky', 'puss', 'pusse', 'pussi', 'pussies', 'pussy', 'pussypounder', 'pussys', 'puto', 'queaf', 'queaf ', 'queef', 'queer', 'queero', 'queers', 'quicky', 'quim', 'r-tard', 'racy', 'rape', 'raped', 'raper', 'rapist', 'raunch', 'rectal', 'rectum', 'rectus', 'reefer', 'reetard', 'reich', 'retard', 'retarded', 'revue', 'rimjaw', 'rimjob', 'rimming', 'ritard', 'rtard', 'rum', 'rump', 'rumprammer', 'ruski', 's-h-1-t', 's-h-i-t', 's-o-b', 's.h.i.t.', 's.o.b.', 's0b', 's_h_i_t', 'sadism', 'sadist', 'sandbar ', 'scag', 'scantily', 'schizo', 'schlong', 'screw', 'screwed', 'screwing', 'scroat', 'scrog', 'scrot', 'scrote', 'scrotum', 'scrud', 'scum', 'seaman', 'seamen', 'seduce', 'semen', 'sex', 'sexual', 'sh!+', 'sh!t', 'sh1t', 'shag', 'shagger', 'shaggin', 'shagging', 'shamedame', 'shemale', 'shi+', 'shit', 'shitdick', 'shite', 'shiteater', 'shited', 'shitey', 'shitface', 'shitfuck', 'shitfull', 'shithead', 'shithole', 'shithouse', 'shiting', 'shitings', 'shits', 'shitt', 'shitted', 'shitter', 'shitters', 'shitting', 'shittings', 'shitty', 'shiz', 'sissy', 'skag', 'skank', 'slave', 'sleaze', 'sleazy', 'slope ', 'slut', 'slutdumper', 'slutkiss', 'sluts', 'smegma', 'smut', 'smutty', 'snatch', 'sniper', 'snuff', 'sodom', 'son-of-a-bitch', 'souse', 'soused', 'spac', 'sperm', 'spic', 'spick', 'spik', 'spiks', 'spooge', 'spunk', 'steamy', 'stfu', 'stiffy', 'stoned', 'strip', 'stroke', 'stupid', 'suck', 'sucked', 'sucking', 'sumofabiatch', 't1t', 't1tt1e5', 't1tties', 'tampon', 'tard', 'tawdry', 'teabagging', 'teat', 'teets', 'teez', 'terd', 'teste', 'testee', 'testes', 'testical', 'testicle', 'testis', 'thrust', 'thug', 'tinkle', 'tit', 'titfuck', 'titi', 'tits', 'titt', 'tittie5', 'tittiefucker', 'titties', 'titty', 'tittyfuck', 'tittyfucker', 'tittywank', 'titwank', 'toke', 'toots', 'tosser', 'tramp', 'transsexual', 'trashy', 'tubgirl', 'turd', 'tush', 'tw4t', 'twat', 'twathead', 'twats', 'twatty', 'twunt', 'twunter', 'ugly', 'undies', 'unwed', 'urinal', 'urine', 'uterus', 'uzi', 'v14gra', 'v1gra', 'vag', 'vagina', 'valium', 'viagra', 'virgin', 'vixen', 'vodka', 'vomit', 'voyeur', 'vulgar', 'vulva', 'w00se', 'wad', 'wank', 'wanker', 'wanky', 'wazoo', 'wedgie', 'weed', 'weenie', 'weewee', 'weiner', 'weirdo', 'wench', 'wetback', 'wh0re', 'wh0reface', 'whitey', 'whiz', 'whoar', 'whoralicious', 'whore', 'whorealicious', 'whored', 'whoreface', 'whorehopper', 'whorehouse', 'whores', 'whoring', 'wigger', 'womb', 'woody', 'wop', 'wtf', 'x-rated', 'xrated', 'xxx', 'yeasty', 'yobbo', 'zoophile']
        profane_words=profane_words_1 + profane_words_2

        return profane_words

    def _get_possessive_adjectives(self):
        return ['my', 'your', 'his', 'her', 'its', 'our', 'their', 'whose']

    def _get_adjectives(self):
        adjectives=sorted(['affable', 'aloof', 'ambitious', 'amiable', 'arrogant', 'audacious', 'bashful', 'bellicose', 'belligerent', 'bighearted', 'blithe', 'boastful', 'boisterous', 'bony', 'boorish', 'bossy', 'buff', 'buxom', 'calculating', 'callous', 'carefree', 'charming', 'chatty', 'cheerful', 'chic', 'childlike', 'chirpy', 'chiseled', 'churlish', 'classy', 'clumsy', 'conceited', 'condescending', 'confident', 'convivial', 'coquettish', 'cowardly', 'coy', 'crass', 'creepy', 'cruel', 'cunning', 'curvaceous', 'cute', 'deceitful', 'deferential', 'devoted', 'devout', 'diplomatic', 'disagreeable', 'disdainful', 'disheveled', 'domineering', 'dowdy', 'drab', 'dull', 'dwarfish',  'easygoing', 'ebullient', 'eclectic', 'edgy', 'effete', 'egotistical', 'elegant', 'enchanting', 'energetic', 'ethereal', 'evasive', 'excitable', 'exuberant', 'faithful', 'fervid', 'fierce', 'flamboyant', 'formidable', 'freewheeling', 'gallant', 'garrulous', 'gauche', 'gaunt', 'generous', 'genial', 'gentle', 'glamorous', 'gluttonous', 'graceful', 'gregarious', 'grouchy', 'guarded', 'gullible', 'heavyset', 'heroic', 'homely', 'honorable', 'hotheaded', 'hypercritical', 'imaginative', 'immature', 'impertinent', 'imperturbable', 'indolent', 'industrious', 'innocent', 'intrepid', 'irascible', 'irresponsible', 'jealous', 'jittery', 'jocular', 'jovial', 'kooky', 'lanky', 'lazy', 'lean', 'lethargic', 'levelheaded', 'lithe', 'loathsome', 'loutish', 'lovable', 'magnanimous', 'manipulative', 'mature', 'meddlesome', 'mellow', 'mendacious', 'mercurial', 'minimalistic', 'misanthropic', 'mischievous', 'miserly', 'modest', 'modest', 'moody', 'morose', 'narcissistic', 'naïve', 'nosy', 'oafish', 'obedient', 'obnoxious', 'obsequious', 'obstinate', 'odious', 'opinionated', 'optimistic', 'outgoing', 'outspoken', 'passionate', 'passive', 'patient', 'patronizing', 'paunchy', 'peculiar', 'pensive', 'petite', 'petulant', 'placid', 'playful', 'plump', 'polished', 'pugnacious', 'pusillanimous', 'quarrelsome', 'querulous', 'quixotic', 'ravishing', 'rebellious', 'reckless', 'reclusive', 'respectable', 'reticent', 'romantic', 'rotund', 'rumpled', 'sadistic', 'sanguine', 'sardonic', 'saturnine', 'scruffy', 'sensible', 'sexy', 'shrewd', 'sickly', 'sincere', 'sociable', 'spartan', 'spunky', 'squat', 'statuesque', 'stingy', 'stocky', 'stout', 'studious', 'surly', 'svelte', 'swanky', 'sylphlike', 'tactless', 'tetchy', 'timid', 'towering', 'trendy', 'truculent', 'trusting', 'unctuous', 'unreliable', 'vain', 'verbose', 'vibrant', 'vicious', 'vivacious', 'voluptuous', 'voracious', 'vulnerable', 'wicked', 'willowy', 'wily', 'winsome', 'wiry', 'witty', 'youthful', 'zaftig', 'zany', 'zealous'])

        return adjectives

    def _get_adverbs(self):
        adverbs=['abnormally', 'absentmindedly', 'accidentally', 'actually', 'adventurously', 'afterwards', 'almost', 'always', 'annually', 'anxiously', 'arrogantly', 'awkwardly', 'bashfully', 'beautifully', 'bitterly', 'bleakly', 'blindly', 'blissfully', 'boastfully', 'boldly', 'bravely', 'briefly', 'brightly', 'briskly', 'broadly', 'busily', 'calmly', 'carefully', 'carelessly', 'cautiously', 'certainly', 'cheerfully', 'clearly', 'cleverly', 'closely', 'coaxingly', 'colorfully', 'commonly', 'continually', 'coolly', 'correctly', 'courageously', 'crossly', 'cruelly', 'curiously', 'daily', 'daintily', 'dearly', 'deceivingly', 'deeply', 'defiantly', 'deliberately', 'delightfully', 'diligently', 'dimly', 'doubtfully', 'dreamily', 'easily', 'elegantly', 'energetically', 'enormously', 'enthusiastically', 'equally', 'especially', 'even', 'evenly', 'eventually', 'exactly', 'excitedly', 'extremely', 'fairly', 'faithfully', 'famously', 'far', 'fast', 'fatally', 'ferociously', 'fervently', 'fiercely', 'fondly', 'foolishly', 'fortunately', 'frankly', 'frantically', 'freely', 'frenetically', 'frightfully', 'fully', 'furiously', 'generally', 'generously', 'gently', 'gladly', 'gleefully', 'gracefully', 'gratefully', 'greatly', 'greedily', 'happily', 'hastily', 'healthily', 'heavily', 'helpfully', 'helplessly', 'highly', 'honestly', 'hopelessly', 'hourly', 'hungrily', 'immediately', 'innocently', 'inquisitively', 'instantly', 'intensely', 'intently', 'interestingly', 'inwardly', 'irritably', 'jaggedly', 'jealously', 'jovially', 'joyfully', 'joyously', 'jubilantly', 'judgmentally', 'justly', 'keenly', 'kiddingly', 'kindheartedly', 'kindly', 'knavishly', 'knowingly', 'knowledgeably', 'kookily', 'lazily', 'les', 'lightly', 'likely', 'limply', 'loftily', 'longingly', 'loosely', 'loudly', 'lovingly', 'loyally', 'madly', 'majestically', 'meaningfully', 'mechanically', 'merrily', 'miserably', 'mockingly', 'monthly', 'more', 'mortally', 'mostly', 'mysteriously', 'naturally', 'hopelessly', 'hourly', 'hungrily', 'immediately', 'innocently', 'inquisitively', 'instantly', 'intensely', 'intently', 'interestingly', 'inwardly', 'irritably', 'jaggedly', 'jealously', 'jovially', 'joyfully', 'joyously', 'jubilantly', 'judgmentally', 'justly', 'keenly', 'kiddingly', 'kindheartedly', 'kindly', 'knavishly', 'knowingly', 'knowledgeably', 'kookily', 'lazily', 'less', 'lightly', 'likely', 'limply', 'loftily', 'longingly', 'loosely', 'loudly', 'lovingly', 'loyally', 'madly', 'majestically', 'meaningfully', 'mechanically', 'merrily', 'miserably', 'mockingly', 'monthly', 'more', 'mortally', 'mostly', 'mysteriously', 'naturally', 'nearly', 'neatly', 'nervously', 'never', 'nicely', 'noisily', 'not', 'obediently', 'obnoxiously', 'oddly', 'offensively', 'officially', 'often', 'only', 'openly', 'optimistically', 'overconfidently', 'painfully', 'partially', 'patiently', 'perfectly', 'physically', 'playfully', 'politely', 'poorly', 'positively', 'potentially', 'powerfully', 'promptly', 'properly', 'punctually', 'quaintly', 'queasily', 'queerly', 'questionably', 'quicker', 'quickly', 'quietly', 'quirkily', 'quizzically', 'randomly', 'rapidly', 'rarely', 'readily', 'really', 'reassuringly', 'recklessly', 'regularly', 'reluctantly', 'repeatedly', 'reproachfully', 'restfully', 'righteously', 'rightfully', 'rigidly', 'roughly', 'rudely', 'safely', 'scarcely', 'scarily', 'searchingly', 'sedately', 'seemingly', 'seldom', 'selfishly', 'separately', 'seriously', 'shakily', 'sharply', 'sheepishly', 'shrilly', 'shyly', 'silently', 'sleepily', 'slowly', 'smoothly', 'softly', 'solemnly', 'solidly', 'sometimes', 'speedily', 'stealthily', 'sternly', 'strictly', 'successfully', 'suddenly', 'supposedly', 'surprisingly', 'suspiciously', 'sweetly', 'swiftly', 'sympathetically', 'tenderly', 'tensely', 'terribly', 'thankfully', 'thoroughly', 'thoughtfully', 'tightly', 'tomorrow', 'too', 'tremendously', 'triumphantly', 'truly', 'truthfully', 'rightfully', 'scarcely', 'searchingly', 'sedately', 'seemingly', 'selfishly', 'separately', 'seriously', 'sheepishly', 'smoothly', 'solemnly', 'sometimes', 'speedily', 'stealthily', 'successfully', 'suddenly', 'supposedly', 'surprisingly', 'suspiciously', 'sympathetically', 'tenderly', 'thankfully', 'thoroughly', 'thoughtfully', 'tomorrow', 'tremendously', 'triumphantly', 'truthfully', 'ultimately', 'unabashedly', 'unaccountably', 'unbearably', 'unethically', 'unexpectedly', 'unfortunately', 'unimpressively', 'unnaturally', 'unnecessarily', 'upbeat', 'upright', 'upside-down', 'upward', 'urgently', 'usefully', 'uselessly', 'usually', 'utterly', 'vacantly', 'vaguely', 'vainly', 'valiantly', 'vastly', 'verbally', 'very', 'viciously', 'victoriously', 'violently', 'vivaciously', 'voluntarily', 'warmly', 'weakly', 'wearily', 'wetly', 'wholly', 'wildly', 'willfully', 'wisely', 'woefully', 'wonderfully', 'worriedly', 'wrongly', 'yawningly', 'yearly', 'yearningly', 'yesterday', 'yieldingly', 'youthfully', 'zealously', 'zestfully', 'zestily']

        return adverbs

    def _get_body_parts_name(self):
        body_parts=['abdomen', 'ankle', 'arm', 'armpit', 'back', 'belly', 'buttock', 'chest', 'ear', 'elbow', 'eye', 'face', 'foot', 'forearm', 'forehead', 'hair', 'head', 'hip', 'instep', 'knee', 'leg', 'mouth', 'navel', 'neck', 'nose', 'shoulder', 'thigh', 'thumb', 'toenail', 'toes', 'waist', 'wrist']
        return body_parts

    def _get_slang_body_parts(self):
        slang_body_parts=['abs', 'arse', 'ass', 'baby blues', 'beak', 'beer belly', 'behind', 'belly', 'belly button', 'boobs', 'booty', 'buns', 'butt', 'cans', 'choppers', 'cock', 'cooch', 'cooter', 'dick', 'dogs', 'dome', 'duff', 'family jewels', 'fanny', 'genitals', 'girls', 'girly bits', 'gray matter', 'guns', 'gut', 'guts', 'heinie', 'honker', 'jugs', 'manhood', 'mitts', 'mug', 'nether regions', 'noggin', 'noodle', 'nut', 'paws', 'peepers', 'pie hole', 'pot belly', 'private', 'private parts', 'pussy', 'rack', 'rear end', 'schnozz', 'six-pack', 'smarts', 'snatch', 'spare tire', 'ta-tas', 'tail', 'ticker', 'tits', 'tootsies', 'trap', 'tummy', 'tush', 'twins', 'vag', 'vajayjay', 'washboard abs', 'wee-wee', 'weenie']
        return slang_body_parts

    def _get_common_slangs(self):

        slangs_1=['#ff', '(u)', '*$', '**//', ',!!!!', '/r/', '02', '10q', '1174', '121', '123', '1337', '14', '142n8ly', '143', '1432', '14aa41', '182', '187', '19', '1daful', '1v4', '2', '20', '24/7', '2b', '2b or not 2b', '2b@', '2bz4uqt', '2b~not2b', '2d4', '2day', '2dloo', '2g2b4g', '2g2bt', '2moro', '2nite', '2qt', '2u2', '303', '4', '403', '404', '411', '420', '459', '4col', '4e', '4eae', '4eva', '4ever', '4fs', '4nr', '4q', '511', '53x', '5fs', '747', '775', '8', '831', '86', '88', '8t', '9', '99', '996', '::poof::', '<3', '?^', '@+', '@teotd', '\\m/', '^5', '^rup^', '^urs', 'a/n', 'a/s/l/p', 'a2d', 'a3', 'aaaaa', 'aaf', 'aak', 'aamof', 'aamoi', 'aap', 'aar', 'aar8', 'aatk', 'aayf', 'ab', 'ab/abt', 'abc', 'abcd', 'abh', 'abithiwtitb', 'abk', 'abt2', 'acc', 'acd', 'ace', 'ack', 'acorn', 'adad', 'adbb', 'add', 'adidas', 'adih', 'adip', 'adm', 'adn', 'adr', 'advd', 'aeap', 'af', 'afagay', 'afahmasp', 'afaic', 'afaics', 'afaict', 'afaik', 'afair', 'afaiu', 'afaiui', 'afap', 'afayc', 'afc', 'afdn', 'afgo', 'afiaa', 'afiniafi', 'afj', 'afk', 'afpoe', 'aft', 'afu', 'afw', 'afz', 'agb', 'agig', 'agkwe', 'ai', 'aiamu', 'aight', 'aih', 'aimb', 'aimp', 'airhead', 'aisb', 'aisi', 'aitr', 'aka or a.k.a.', 'alcon', 'alf', 'allnighter', 'alol', 'alotbsol', 'altg', 'alw', 'ama', 'amap', 'ambw', 'amf', 'aml', 'amosc', 'amp', 'amrmtyfts', 'anfawfos', 'anfscd', 'angb', 'aoas', 'aob', 'aon', 'aor', 'aoyp', 'ap', 'apac', 'apu', 'ar', 'as', 'asafp', 'asamof', 'asap', 'asaygt', 'asl', 'aslmh', 'asmr', 'atab', 'atbims', 'atc', 'atm', 'atsl', 'atst', 'atw', 'atwd', 'aunt', 'auntm', 'awc', 'awesome', 'awgthtgtta', 'awhfy', 'awltp', 'awniac', 'awol', 'aws', 'awttw', 'ax', 'ayc', 'ayeg', 'ayfkmwts', 'ayk', 'aymm', 'ayor', 'aysos', 'aytmtb', 'ayv', 'b', 'b&e', 'b&f', 'b/c', 'b/w', 'b2a', 'b2b', 'b2b2c', 'b2c', 'b2d', 'b2e', 'b2g', 'b4', 'b4n', 'b4u', 'b4yki', 'b@u or bak@u', 'babe', 'bac', 'bae', 'baeb', 'baesbo', 'bag', 'bail', 'ball', 'bame', 'bamf', 'banana', 'barb', 'base', 'basic', 'bazillion', 'bb', 'bb4n', 'bbamfic', 'bbb', 'bbbg', 'bbfbbm', 'bbfn', 'bbiab', 'bbiaf', 'bbias', 'bbiaw', 'bbl', 'bbmfic', 'bbq', 'bbr', 'bbs', 'bbsd', 'bbsl', 'bbt', 'bbw', 'bc', 'bcbg', 'bcbs', 'bcnu', 'bcoz', 'bd', 'bdbi5m', 'bdc', 'bde', 'bdn', 'bdoa', 'bdsm', 'beemer', 'beg', 'beos', 'bestie', 'bf', 'bf4l', 'bfbo', 'bfd', 'bfe', 'bff', 'bff', 'bffn', 'bfftte', 'bffw', 'bfg', 'bfn', 'bfr', 'bgbc', 'bgf', 'bhg', 'bhimbgo', 'bhof', 'bi', 'bi5', 'bibi', 'bif', 'big', 'bil', 'bimbo', 'bio', 'bioiya', 'bion', 'bioye', 'bioyiop', 'bioyn', 'bitch', 'bitch', 'bitd', 'bitfob', 'biz', 'bj', 'bka', 'bl', 'blast', 'blbblb', 'bld', 'blkbry', 'blzrd', 'bm', 'bmf', 'bmgwl', 'bmoc', 'bmof', 'bmota', 'bms', 'bmw', 'bn', 'bndn', 'bnf', 'bo', 'boaisy', 'boat', 'bobfoc', 'boctaae', 'bod', 'bofh', 'boh', 'bohica', 'bol', 'bon', 'bonkers', 'book', 'botec', 'botl', 'botoh', 'botus', 'bplm', 'br', 'brb', 'break', 'brics', 'brl', 'bro', 'bro', 'brt', 'bruf', 'bs', 'bsaaw', 'bsbd&ne', 'bseg', 'bsf', 'bsod', 'bt', 'bta', 'btd', 'btdt', 'btdtgts', 'btfldy', 'btfo', 'bthoom', 'bti', 'btn', 'btoiya', 'btr', 'btsoom', 'btte', 'bttp', 'bttt', 'btw', 'btwbo', 'btwitiailwu', 'btyc', 'btyd', 'buck', 'buff', 'buhbye', 'bummed', 'bump', 'bw', 'bwdik', 'bwi', 'bwl', 'bwo', 'bwtm', 'byki', 'bykt', 'byoa', 'byob', 'byod', 'byop', 'byow', 'bytme', 'bz', 'c', 'c ya', 'c%d', 'c%l', 'c&g', 'c-p', 'c-t', 'c/p', 'c/s', 'c4n', 'caac', 'cal', 'cas', 'cb', 'cbb', 'cbd', 'cbf', 'cbj', 'cbm', 'cbot', 'cbt', 'cc', 'ccot', 'ccw', 'cd', 'cd9', 'cf', 'cfv', 'cha', 'cheesy', 'chicken', 'chln', 'ciao', 'cico', 'cicyhw', 'cil', 'cinba', 'cito', 'cld', 'clm', 'cm', 'cmao', 'cmap', 'cmb', 'cmf', 'cmiw', 'cmsu', 'cmu', 'cn', 'cnp', 'cob', 'cobras', 'cod', 'cof$', 'cofs', 'col', 'con', 'coo', 'cool', 'cos', 'cot', 'couch', 'courses', 'cpa', 'cpc', 'cpg', 'cpl', 'cqrt', 'cqts', 'craft', 'crap', 'crap', 'crash', 'crat', 'craws', 'crb', 'crbt', 'crd', 'crdtchck', 'cringe', 'cringeworthy', 'croak', 'crs', 'crtla', 'cruising', 'crush', 'cs']
        slangs_2=['cs&f', 'csa', 'csabr', 'csl', 'csn', 'ct', 'cta', 'ctc', 'ctfd', 'ctfo', 'ctfu', 'ctmq', 'cto', 'cu', 'cu46', 'cua', 'cuatsc', 'cuatu', 'cul', 'cul8r', 'cuns', 'cunt', 'cuol', 'cupl', 'cushy', 'custom', 'cuwta', 'cuz', 'cwot', 'cwyl', 'cx', 'cxo', 'cy', 'cye', 'cyl', 'cym', 'cyo', 'cyoh', 'cyt', 'd', 'd&m', 'd/c', 'd00d', 'd2d', 'd8', 'da', 'dafuq', 'damhikt', 'darfc', 'dash', 'dba', 'dbabai', 'dbbswf', 'dbd', 'dbeyr', 'dbmib', 'dd', 'ddas', 'ddg', 'ddsos', 'ddwi', 'dead', 'deck', 'deep', 'def', 'defo', 'degt', 'dem', 'denial', 'detweet', 'dewd', 'dey', 'df', 'dfik', 'dfla', 'dftba', 'dfu', 'dfwly', 'dga', 'dgaf', 'dgara', 'dgt', 'dgtg', 'dgyf', 'dh', 'dhyb', 'diaf', 'dic', 'difbet', 'dilligad', 'dilligas', 'dink', 'dino', 'dinosaur', 'dinr', 'dirft', 'disto', 'ditch', 'ditr', 'ditto', 'dityid', 'djm', 'dk', 'dkdc', 'dl', 'dltbbb', 'dltm', 'dm', 'dmi', 'dnbl8', 'dnc', 'dnd', 'dnf', 'dnpmpl', 'dnr', 'doc', 'doe', 'doei', 'dog', 'doh', 'doin', 'dope', 'dord', 'dos', 'douche', 'dough', 'dp', 'dps', 'dpup', 'dqmot', 'dqydj', 'drb', 'drcowoto', 'drib', 'dsl', 'dstr8', 'dtc', 'dtf', 'dtk', 'dtr', 'dtrt', 'dude', 'dui', 'dum', 'dump', 'dunno', 'dunno', 'dur', 'durs', 'dusl', 'dust', 'dw', 'dw2h', 'dwb', 'dwbh', 'dweet', 'dwh', 'dwi', 'dwpkotl', 'dws', 'dwwwi', 'dwym', 'dyac', 'dyd', 'dyfm', 'dyhab', 'dyhag', 'dyjhiw', 'dyli', 'dynamite', 'dyofdw', 'dystsott', 'e123', 'e2ho', 'eabos', 'eadd', 'eak', 'eapfs', 'earful', 'edm', 'ee', 'ee or ees', 'effin', 'eft', 'eg', 'egot', 'ehe', 'eht', 'eip', 'elol', 'em', 'embm', 'emdr', 'emea', 'emfbi', 'emfji', 'eml', 'emp', 'emrtw', 'emsg', 'eod', 'eol', 'eom', 'eot', 'eow','esad', 'esadyfa', 'esemed', 'esfoad', 'esg', 'esh', 'esmf', 'eso', 'eta', 'etla', 'etx', 'every1', 'evre1', 'ewi', 'eyd', 'eyeball', 'eyepopping', 'eyfd', 'f', 'f/u', 'f2f', 'f2fmail', 'f2t', 'f4f', 'faangs', 'faf', 'fah', 'fap', 'faql', 'fasb', 'fatc', 'fatm', 'fav', 'fawc', 'fawomft', 'fay', 'fb', 'fbi', 'fbks', 'fbocd', 'fcfs', 'fcol', 'fcs', 'fdff', 'fdgb', 'fdu', 'fear', 'fenderbender', 'ff', 'ff&pn', 'ffa', 'ffs', 'fft', 'fgdai', 'fgf', 'fho', 'fif', 'fifo', 'figjam', 'figmo', 'figs', 'fiik', 'fil', 'filf', 'filo', 'filth', 'fine', 'finsta', 'fire', 'first', 'fish', 'fitb', 'fitymi', 'fkm', 'fla', 'flicks', 'flotus', 'fluid', 'fml', 'fmltwia', 'fmot', 'fmtyewtk', 'fmuta', 'fng', 'fo', 'foad', 'foaf', 'foag', 'fob', 'foc', 'foe', 'fofl', 'fogc', 'foh', 'fol', 'folo', 'fomc', 'fomcl', 'fomo', 'fomof', 'foot', 'fos', 'fouo', 'fpo', 'freebie', 'frog', 'frzn', 'fs', 'fsbo', 'fsr', 'fstow', 'fsu', 'ftad', 'ftasb', 'ftbl', 'ftbomh', 'ftc', 'fte', 'ftf', 'ftfoi', 'ftl', 'ftlog', 'ftn', 'ftr', 'ftrf', 'fttb', 'ftw', 'fu2', 'fub', 'fubar', 'fubarbundy', 'fubb', 'fubyoyo', 'fud', 'fujimo', 'fum', 'fumf', 'fupa', 'furtb', 'fuw', 'fwb', 'fwd', 'fwiw', 'fwot', 'fya', 'fyc', 'fye', 'fyeo', 'fyf', 'fyi', 'fyifv', 'fyltge', 'fym', 'fysbigtbabn', 'g', 'g1', 'g2g', 'g2glys', 'g4i', 'g4n', 'g9', 'g98t', 'ga', 'gafa', 'gafl', 'gafyk', 'gagfi', 'gahoy', 'galgal', 'galher', 'galhim', 'ganb', 'gap', 'gas', 'gawd', 'gb', 'gbg', 'gbh', 'gbp', 'gbtw', 'gc', 'gd', 'gd&r', 'gd&rf', 'gdi', 'gdpr', 'gdw', 'gf', 'gfe', 'gff', 'gfi', 'gfn', 'gfon', 'gfr', 'gftd', 'gftu', 'gfy', 'gfymf', 'gg', 'gga', 'gggg', 'ggn', 'ggoh', 'ggp', 'ggpbl', 'ggy', 'ghm', 'ghosted', 'gic', 'gidk', 'gig', 'gigatt', 'gigo', 'gilf', 'gimme', 'gist', 'git', 'giwist', 'gj', 'gjp', 'gl', 'gla', 'glawd', 'glb', 'glbt', 'glg', 'glgh', 'glitch', 'glws', 'glyasdi', 'gm', 'gmab', 'gmafb', 'gmh', 'gmily', 'gmta', 'gmta asdo', 'gmtft', 'gn', 'gn8', 'gnblfy', 'gnoc', 'gns', 'gnsd', 'go', 'goat', 'goat', 'gob', 'gok', 'gol', 'golf', 'gomb', 'gonna', 'good job', 'goof', 'gork', 'gos', 'gospel', 'gotdpwyd', 'gotp', 'gotta', 'gowi', 'goyhh', 'gpoy', 'gqmf', 'gr&d', 'gr2br', 'gr8', 'grand', 'gras', 'gratz', 'grobr', 'grrlz', 'grrr', 'grub', 'grx', 'gsc', 'gsoas', 'gsoh', 'gstg', 'gsw', 'gsyjdwurmnkh', 'gt', 'gtasc', 'gtfo', 'gtfooh', 'gtg', 'gtgb', 'gtgp', 'gth', 'gtk', 'gtl', 'gtm', 'gtp', 'gtrm', 'gts']
        slangs_3=['gtsy', 'gud', 'guts', 'guvment', 'gwi', 'gwot', 'gws', 'gyhooya', 'gylabtw', 'gypo', 'h&k', 'h/o', 'h/p', 'h2cus', 'h2s', 'h4u', 'h4xx0r', 'h9', 'hadvd', 'hafta', 'hag1', 'hagd', 'hagn', 'hago', 'hahaha', 'hak', 'hand', 'hangry', 'har', 'hawtlw', 'hay', 'hb', 'hbastd', 'hbb', 'hbib', 'hbic', 'hbo', 'hbtu', 'hbu', 'hcc', 'hd', 'hdgfs', 'hdm', 'hea', 'heave', 'helllo', 'hello', 'hey', 'heyy', 'hf', 'hhfo', 'hhh', 'hhis', 'hho1/2k', 'hhoj', 'hhok', 'hhos', 'hhtyay', 'hi 5', 'hig', 'hih', 'hiooc', 'hippo', 'hitaks', 'hmfic', 'hmfwicc', 'hml', 'hmot', 'hmu', 'hnti', 'hntw', 'hny', 'ho', 'hodl', 'hoha', 'hoic', 'hola', 'hologram', 'hook', 'hot', 'hot pic', 'howru', 'hoyew', 'hp', 'hpoa', 'hppo', 'hr', 'hrcn', 'hsay', 'hsiab', 'hsik', 'ht', 'htb', 'hth', 'htnoth', 'hu', 'hua', 'huggle', 'hugz', 'huh', 'hunty', 'hustle', 'huya', 'hv', 'hwevr', 'hwga', 'hx', 'i 1-d-r', 'i <3 i', 'i <3 u', 'i h8 it', 'i&i', 'i-d-l', 'iac', 'iae', 'iagtkom', 'iaits', 'ianac', 'ianadbipootv', 'ianae', 'ianal', 'iannngc', 'iasap4u', 'iat', 'iaw', 'iaym', 'ibgybg', 'ibiwisi', 'ibk', 'ibrb', 'ibt', 'ibtc', 'ibtd', 'ibtl', 'ic', 'icbw', 'icbwicbm', 'iccl', 'icihicpcl', 'ico-911', 'icw', 'icwum', 'icyc', 'icymi', 'id', 'id10t', 'idbi', 'idc', 'idek', 'idewtk', 'idgad', 'idgaf', 'idgara', 'idghp', 'idgi', 'idiftl', 'idiot', 'idk', 'idk, my bff jill', 'idkabtt', 'idkwtd', 'idky', 'idm', 'idnkt', 'idrk', 'idst', 'idta', 'idtbbf', 'idts', 'idwtub', 'ief', 'if/ib', 'ifab', 'ifh8tabx', 'ifu', 'igers', 'iggp', 'igtp', 'igws', 'igwst', 'igyhtbt', 'iha', 'ihaim', 'ihnc', 'ihno', 'ihr', 'ihtfp', 'ihu', 'ihy', 'iiabdfi', 'iiio', 'iimad', 'iinm', 'iir', 'iirc', 'iit', 'iitlyto', 'iitm', 'iitywimwybmad', 'iitywybmad', 'iiwii', 'iiwm', 'ij', 'ijpmp', 'ijs', 'ijwtk', 'ijwts', 'ikaloplt', 'ikr', 'ikwym', 'ikyabwai', 'ilbcnu', 'ilbcnul8r', 'ilf/md', 'iliciscomk', 'ilmj', 'iluaaf', 'ily2', 'im', 'im2bz2p', 'imao', 'imco', 'ime', 'imezru', 'imf', 'imfao', 'imfkd^', 'imgc', 'imheiuo', 'imhif', 'imho', 'imjs', 'imml', 'imnerho', 'imnsho', 'imoo', 'imowha', 'impov', 'imr', 'ims', 'inbd', 'inch', 'incydk', 'inmp', 'innw', 'inpo', 'inucosm', 'ioh', 'ion', 'iono', 'iot', 'iottco', 'iou', 'ioud', 'iow', 'ipn', 'irl', 'irl', 'irncot', 'isagn', 'ish', 'iso', 'iss', 'issoys', 'issygti', 'istm', 'istr', 'iswc', 'iswym', 'isyals', 'ita', 'itfa', 'itgft', 'itigbs', 'itm', 'itma', 'itmfa', 'its', 'its a d8', 'itsfwi', 'ium', 'iuri', 'iwalu', 'iwbaptakyaiysta', 'iwbni', 'iwfu', 'iwfy', 'iwiwu', 'iwsn', 'iwtkcr', 'iyam', 'iyaoyas', 'iycssnasdsaaa', 'iyd', 'iydmma', 'iyfd', 'iyfeg', 'iykwim', 'iykwimaityd', 'iynaegbtm', 'iyo', 'iyq', 'iyss', 'iyswim', 'i’mma', 'j/c', 'j/j', 'j/k', 'j/o', 'j/p', 'j/w', 'j2lyk', 'j4f', 'j4g', 'j4t or jft', 'j5m', 'jad', 'jafo', 'jafs', 'jas', 'jata', 'jc', 'jdi', 'jdmj', 'jealz', 'jeomk', 'jerk', 'jfc', 'jfh', 'jfi', 'jgh', 'jgmb', 'jho', 'jhom', 'jhomf', 'jic', 'jk', 'jly', 'jm2c', 'jmdtp30', 'jmo', 'jock', 'joml', 'jomo', 'joott', 'joy', 'jp', 'js', 'jso', 'jsu', 'jsyk', 'jt', 'jtlyk', 'jtol', 'jtou', 'juadlam', 'junkie', 'k', 'k', 'kab', 'kb', 'kbd', 'kc', 'kcco', 'kewl', 'kfb', 'kfy -or- k4y', 'khyf', 'kibo', 'kick', 'killer', 'kinda', 'kippers', 'kir', 'kiss', 'kitty', 'kity', 'kk', 'kkk', 'kma', 'kmba', 'kmfha', 'kmim', 'kmp', 'kmria', 'kms', 'kmsla', 'kmuf', 'kmwa', 'kotc', 'kotl', 'kpc', 'ks', 'kthxbye', 'kudt', 'kutgw', 'kwim', 'kwsta', 'kybc', 'kyfc', 'kync', 'kypo', 'kysoti', 'l', 'l&r', 'l/m', 'l8tr', 'l?^', 'l@u', 'labatyd', 'lafw', 'lagnaf', 'lago', 'lame', 'laoj', 'laq', 'last', 'lb', 'lb?w/c', 'lbh', 'lbr and lgr', 'lbs', 'lbug or lbig', 'ld', 'ldimedilligaf', 'ldr', 'ldttwa', 'lesm', 'lf', 'lfl', 'lfti', 'lfu', 'lgbt', 'lgbtq+', 'lggbdtttiqqaapp', 'lgmas', 'lgtm', 'lgy', 'lh', 'lh6', 'lhk', 'lhm', 'lho', 'lhos', 'lhso', 'lhu', 'lifo', 'lig', 'lins', 'lir', 'lis', 'lit', 'ljbf', 'lkitr', 'll', 'llap', 'llom', 'llt', 'llta', 'lly', 'lm46', 'lm4a~##zzzz>', 'lmao', 'lmbao', 'lmbpo', 'lmfao', 'lmfo', 'lmho', 'lmirl', 'lmk', 'lmkhtwofy', 'lmoa', 'lmp', 'lmr', 'lms', 'lmso', 'lmta', 'lmtc', 'lmtcb', 'lo', 'loal', 'lob', 'logo', 'lok', 'lol', 'lol wuss', 'lololol', 'lolpmp', 'lolrotf&icgu', 'lolz', 'loml', 'lonh', 'lool', 'loomm', 'lopsod', 'lore', 'loser', 'lowkey', 'lpc', 'lpos']
        slangs_4=['lrf', 'lrt', 'lsb', 'lshitipal', 'lshmbh', 'lsv', 'ltf', 'lthtt', 'ltic', 'ltio', 'ltm', 'ltns', 'ltnt', 'ltotd', 'ltr', 'ltrp', 'lts', 'lttic', 'lulz', 'lumtp', 'lumu', 'lumumi', 'luser', 'lusm', 'lvl', 'lwr', 'lwu', 'lwys', 'ly4e', 'lyaaf', 'lyb', 'lycylbb', 'lykyamy', 'lyl', 'lylab', 'lylas', 'lylb', 'lymi', 'lysouaq', 'lysyb', 'lywamh', 'm', 'm2ny', 'm4c', 'm4m', 'm4w', 'm8 or m8s', 'mamil', 'mb', 'mbf', 'mbn', 'mbrfn', 'mc', 'mcm', 'md', 'mdms', 'mdr', 'mego', 'meh', 'mejr', 'meltdown', 'merp', 'mf', 'mfbty', 'mfd', 'mfg', 'mfic', 'mfrc', 'mfwic', 'mhbfy', 'mhhm', 'mhoty', 'mhyf', 'mih', 'mihap', 'mil', 'milf', 'mins', 'mistweet', 'mitin', 'miwi', 'mkop', 'mla', 'mlas', 'mlm', 'mlylt', 'mm', 'mmha2u', 'mmk', 'mml', 'mmyt', 'mo', 'mob', 'mof', 'mofo', 'mompl', 'moobs', 'mooc', 'mop', 'morf', 'mos', 'mot', 'motas', 'motd', 'motos', 'motss', 'mov', 'mpfb', 'mra', 'mrm', 'mrph', 'mrt', 'msg', 'msm', 'msmd', 'msnuw', 'msta', 'mstm', 'mt', 'mtbf', 'mtf', 'mtfbwy', 'mtla', 'mtmmfbwy', 'mtsbwy', 'mtsitn', 'mu', 'muah or mwah', 'mubar', 'mulc', 'musl', 'musm', 'mva', 'mva no pi', 'mva w/pi', 'mvo', 'mvto', 'mwbrl', 'mws', 'myl', 'myob', 'myt', 'mywb', 'n', 'n pic', 'n-a-y-l', 'n/a', 'n/m', 'n/t', 'n1', 'n2m', 'n2mjchbu', 'na', 'nab', 'nadt', 'nagb', 'nalopkt', 'namailu', 'nascar', 'natc', 'natch', 'nato', 'navy', 'naz', 'nb', 'nb4t', 'nbd', 'nbfab', 'nbfabs', 'nbg', 'nbif', 'nblfy', 'nbs', 'nc', 'ncbd', 'ncg', 'nd', 'ndn', 'ne', 'ne-wayz', 'ne1', 'ne14kfc', 'ne1er', 'ne2h', 'neat', 'neet', 'nef', 'nej', 'nerd', 'nesec', 'netflix', 'nev', 'neweeter', 'news', 'nfbsk', 'nfc', 'nfe', 'nff', 'nfg', 'nfi', 'nfs', 'nft', 'nfw', 'ngb', 'ngh', 'ngl', 'nh', 'nhoh', 'ni4ni', 'nice', 'nidl', 'nifoc', 'nigyysob', 'nih', 'nim', 'nimby', 'nimjd', 'nimq', 'nimy', 'ninja', 'nino', 'nism', 'nitl', 'niywfd', 'njapf', 'nkd', 'nlb', 'nll', 'nltbro', 'nm', 'nm, u', 'nme', 'nmh', 'nmhjc', 'nmm', 'nmp', 'nmte', 'nmu', 'nn', 'nncimintfz', 'nnr', 'nnsh', 'nnww', 'no', 'no praw', 'no1', 'noa', 'nofi', 'noob', 'nos', 'noy', 'noyb', 'np', 'nqa', 'nqocd', 'nr', 'nrg', 'nrn', 'ns', 'nsa', 'nsb', 'nsfw', 'nss', 'nstlc', 'nta', 'ntabom', 'ntb', 'ntbm', 'ntbn', 'nth', 'ntim', 'ntimm', 'ntk', 'ntl', 'ntm', 'ntmu', 'nttawwt', 'ntw', 'ntymi', 'nub', 'nuff', 'nuts', 'nvm', 'nvng', 'nw', 'nwal', 'nwot', 'nwr', 'nwt', 'nyc', 'nycfs', 'o', 'o_o', 'oao', 'oatus', 'oaus', 'ob', 'obe', 'obf', 'obnr', 'obo', 'obs', 'obtw', 'obx', 'oc', 'ocd', 'od', 'oddball', 'odtaa', 'of', 'ofap', 'ofc', 'og', 'og', 'oh', 'oh', 'ohf', 'oic', 'oicu812', 'oirwis', 'oit', 'ok', 'ok', 'ol', 'oll', 'olli', 'oln', 'olo', 'om', 'omb', 'omdb', 'ome', 'omfg', 'omg', 'omg', 'omik', 'oml', 'omw', 'omwt', 'onid', 'onnta', 'onud', 'oo', 'ooak', 'ooc', 'oof', 'ooi', 'oomf', 'ooo', 'oos', 'oot', 'ootb', 'ootc', 'ootd', 'oott', 'ooyf', 'op', 'osif', 'osintot', 'ost', 'ot', 'otasoic', 'otb', 'otc', 'otf', 'oth', 'otl', 'otoh', 'otp', 'ots', 'ott', 'ottomh', 'otw', 'ousu', 'outta', 'ova', 'owtte', 'oz', 'p', 'p&c', 'p-za', 'p/u', 'p2c2e', 'p2u4uraqtp', 'p3r50n', 'p911', 'pa', 'pac', 'pans', 'pap', 'paronym', 'part', 'paw', 'pax', 'pb', 'pbb', 'pbem', 'pbiab', 'pbj', 'pc', 'pcm', 'pcmcia', 'pd', 'pda', 'pdoma', 'pdq', 'pds', 'peanuts', 'pebcac', 'pebcak', 'peep', 'peeps', 'pen15', 'pfa', 'pfc', 'pfm', 'phat', 'phb', 'phs', 'piaps', 'pibkac', 'picnic', 'pif', 'pimp', 'pimpl', 'pin', 'pir', 'pissed', 'pissed', 'pitmemboam', 'pix', 'plo', 'plokta', 'plos', 'pls', 'plu', 'plur', 'plz', 'pm', 'pmbi', 'pmf', 'pmfji', 'pmht', 'pmigbom', 'pmji', 'pml', 'pmn', 'pmp', 'pmsl', 'pnatmbc', 'pnattmbtc', 'pncah', 'pnd', 'po', 'po-mo', 'poa', 'poahf', 'poak', 'pod', 'poets', 'politweet', 'poms', 'pona', 'pop', 'pos', 'posc', 'posslq', 'potato', 'pots', 'potus', 'pov', 'pow', 'pp', 'ppc', 'ppl', 'ppppppp or 7p', 'pron', 'prt', 'prw', 'ps', 'psa', 'pse', 'pso', 'ptat', 'pth', 'ptl', 'ptmm', 'ptoyed', 'ptp', 'ptpop', 'puh', 'push', 'puter', 'pvp', 'pw', 'pwas', 'pwat', 'pwcb', 'pwms', 'pwn']
        slangs_5=['pwnt', 'pwoms', 'pwp', 'pyfb', 'pyop', 'q', 'q&a', 'q1', 'q2c', 'q416', 'q4u', 'qap', 'qb', 'qc', 'qed', 'qfe', 'qfmt', 'qft', 'qi', 'qix', 'qk', 'ql', 'qls', 'qotd', 'qotp', 'qq', 'qs', 'qt', 'quarterback', 'quick', 'qyb', 'r', 'r u da?', 'r u goin?', 'r u there?', 'r&d', 'r&r', 'raebnc', 'raf', 'rafo', 'rat', 'raw', 'rb@ya', 'rbay', 'rbf', 'rbtl', 'rbu', 'rc', 'rci', 'rdv', 're', 'redlyfe', 'rehi', 'reso', 'rfd', 'rfp', 'rfr', 'rfs', 'rgds', 'rgr', 'rhip', 'rhk', 'ri&w', 'rimjs', 'rino', 'rip', 'ripoff', 'riyl', 'rkba', 'rl', 'rlco', 'rlf', 'rlrt', 'rm', 'rmb', 'rmetth', 'rmlb', 'rmma', 'rmmm', 'rn', 'rnn', 'rny', 'rocking', 'rofl', 'roflmao', 'roflmaoastc', 'roflol', 'ror', 'rotfl', 'rotflmao', 'rotflmfao', 'rotflol', 'rotgl', 'rotglmao', 'rotm', 'rpg', 'rqb', 'rrq', 'rrr', 'rsn', 'rsvp', 'rt', 'rta', 'rtb', 'rtbm', 'rtbs', 'rtfaq', 'rtff', 'rtfm', 'rtfq', 'rth', 'rthx', 'rtk', 'rtm or rtfm', 'rts', 'rtsm', 'rtss', 'rttsd', 'rtwfq', 'ru/18', 'ru\\\\18', 'rufkm', 'ruh', 'rumcymhmd', 'rumorf', 'runts', 'ruok', 'rusos', 'rut', 'ruup4it', 'rx', 'ryfm', 'ryo', 'rys', 's', 's/n', 's/s', 's2g', 's2r', 's2u', 's3<==8', 's4b', 's4l', 's^', 'sadad', 'sahm', 'salty', 'sanm', 'sapfu', 'sb', 'sbi', 'sbta', 'sbug', 'sc', 'scnr', 'scotus', 'screw', 'scuicht', 'sdc', 'sdfb', 'sdfs', 'sdk', 'sec', 'sed', 'seg', 'sep', 'serpt', 'sete', 'sewag', 'sex', 'sf', 'sfaiaa', 'sfb', 'sfete', 'sfla', 'sfp', 'sfttm', 'sftw', 'sfx', 'sgtm', 'sh', 'shades', 'shady', 'shb', 'shhh', 'shid', 'shit', 'sht', 'shtf', 'shwaslomf', 'shxp', 'sic', 'sick', 'sicl', 'sics', 'sii', 'sil', 'sin', 'sip', 'sird', 'sit', 'sitcom', 'sitd', 'situbi', 'siup', 'siuya', 'siy', 'sj', 'sk8er', 'sk8r', 'sknkr', 'sl', 'slack', 'slan', 'slap', 'slaw', 'slirk', 'slm', 'slom', 'slt', 'sm', 'sm1', 'smaim', 'smao', 'smart', 'smb', 'smb2b', 'smc', 'smd', 'sme', 'smem', 'smh', 'smhd', 'smilf', 'smim', 'smize', 'sml', 'smop', 'sms(h)', 'smt', 'sn', 'snafu', 'snag', 'snert', 'snh', 'snif', 'snl', 'snnshwrs', 'snny', 'so', 'sob', 'sobt', 'soddi', 'soe', 'sogop', 'soh', 'sohf', 'soho', 'soi', 'soiar', 'soic', 'sok', 'solomo', 'some1', 'somf', 'somy', 'sooya', 'sop', 'sorg', 'sos', 'sosad', 'sosc', 'sot', 'sotmg', 'sow', 'spat', 'speet', 'spk', 'spoc', 'spt', 'srlb', 'sro', 'sroi', 'srsly', 'sry', 'ssa', 'ssc', 'ssdd', 'ssewba', 'ssia', 'sta', 'stbh', 'stbx', 'stby', 'std', 'stem', 'stfu', 'stfw', 'stg', 'sth', 'sthu', 'stm', 'stml', 'stow', 'stppynozgtw', 'str8', 'sts', 'stst', 'stw', 'stys', 'su', 'suac', 'suakm', 'sub', 'suck', 'sucks', 'sufid', 'sul', 'sup', 'sux', 'suyf', 'swag', 'swag', 'swak', 'swalbcakws', 'swalk', 'swdyt', 'sweet', 'sweet<3', 'swf', 'swim', 'swis', 'swit', 'swl', 'swmbo', 'swot', 'swu', 'swyp', 'sxe', 'syk', 'sys', 'syt', 't&c', 't+', 't2go', 't2ul', 't2ut', 't4p', 't@yl', 'ta', 'tabom', 'tabooma', 'taf', 'tafn', 'tahitmots', 'taks', 'tanj', 'tansit', 'tanstaafl', 'tap', 'tarfu', 'tas', 'taw', 'tayn', 'tb', 'tba', 'tbc', 'tbd', 'tbe', 'tbh', 'tbh', 'tbiu', 'tbt', 'tbu', 'tbyb', 'tc', 'tcb', 'tcfhog', 'tck', 'tcob', 'tcoy', 'td&h', 'tdm', 'tdtm', 'teog', 'teotwawki', 'test', 'tf', 'tfa', 'tfds', 'tff', 'tfh', 'tflms', 'tfm', 'tfmiu', 'tfn', 'tfs', 'tftc', 'tfthaot', 'tftt', 'tftu', 'tfw', 'tfx', 'tfys', 'tg4a', 'tgal', 'tgfad', 'tggtg', 'tgic', 'tgif', 'tgim', 'tgtsio', 'thirsty', 'thot', 'thx or tx or thks', 'tiail', 'tic', 'tigas', 'tight', 'til', 'tilf', 'tilii', 'time', 'timiti', 'tingle', 'tingtes', 'tinwis', 'tisc', 'tisl', 'tisnc', 'tisnf', 'tisnt', 'tjbnj', 'tk', 'tko', 'tku4uk', 'tl;dr', 'tla', 'tlc', 'tlgo', 'tlitbc', 'tlk2ul8r', 'tltr', 'tm', 'tma', 'tmalss', 'tmb', 'tmi', 'tmsaisti', 'tmsgo', 'tmtowtdi', 'tmtt', 'tna', 'tnc', 'tnln', 'tno', 'tnt', 'tntl', 'tnx', 'to go nookleer', 'tobal', 'tobg', 'tomtb', 'tool', 'toon', 'topca', 'tot', 'toy', 'tp', 'tpc', 'tpiyp', 'tps', 'tpt', 'tptb', 'tqm', 'tqrt', 'tram', 'trdmc', 'tripdub', 'trndo', 'troo', 'trp', 'ts', 'tsb', 'tsh', 'tsia', 'tsif', 'tsnf', 'tsob', 'tsr', 'tsra', 'tstb', 'tstl', 'tt', 'tta', 'ttbomk', 'ttfn', 'ttg', 'ttiot', 'ttksf']
        slangs_6=['ttmf', 'tts', 'ttt', 'ttth', 'ttthtfal', 'tttka', 'tttt', 'ttul', 'ttyawfn', 'ttyiaf', 'ttyl', 'ttyl8r', 'ttylxoxo', 'ttyob', 'ttys', 'ttyt', 'tvm4yem', 'tw', 'twars', 'twd', 'twhab', 'twhe', 'twimc', 'twit', 'twita', 'twiwi', 'twss', 'twtr', 'twu', 'txs', 'txt', 'txt im', 'txt msg', 'ty', 'tyclo', 'tyff', 'tyg', 'tyl', 'tyvm', 'u', 'u up', 'u-l', 'u2', 'u4e', 'u8', 'ubs', 'ucwap', 'udh82bme', 'udk', 'udm', 'ufn', 'ufuf', 'ug2bk', 'ugc', 'ugfsu', 'ugtr', 'umk', 'umpteen', 'unf', 'unoit', 'unpc', 'unt', 'untco', 'uok', 'up', 'upod', 'ur', 'ur2k', 'urapita', 'ursai', 'urw', 'urws', 'uryy4m', 'urz', 'usc', 'uscwap', 'usp', 'utm', 'uv', 'uwiwu', 'uwm', 'uwu', 'ux', 'v', 'value', 'vbd', 'vbg', 'vbmg', 'vbs', 'vc', 'vcda', 'veg', 'vfm', 'vgn', 'vibes', 'vilf', 'vip', 'viv', 'vm', 'vma', 'vod', 'vrbs', 'vsf', 'vvs', 'vwd', 'vwp', 'w', 'w wult', "w's^", 'w/', 'w/e', 'w/o', 'w/r/t', 'w00t', 'w4m', 'w8', 'w9', 'w@', 'waboc', 'wabom', 'waci', 'wad', 'wadr', 'waef', 'wafb', 'wafm', 'wafs', 'wafu', 'wag', 'wags', 'wak', 'wambam', 'wan2', 'wanna', 'wap', 'was', 'wasted', 'watcha', 'wati', 'watn', 'waw', 'wawi', 'way', 'wayd', 'wayn', 'wb', 'wbos', 'wbs', 'wbu', 'wc', 'wca', 'wckd', 'wcmtsu', 'wcw', 'wd', 'wdalyic', 'wddd', 'wdily', 'wdr', 'wdt', 'wdyjs', 'wdym', 'wdymbt', 'wdys', 'wdyt', 'we', 'weg', 'wenja', 'werja', 'werru', 'werubn', 'wetsu', 'wf', 'wfh', 'wfm', 'wg', 'wgaff', 'wgmgd', 'what’s', 'wheels', 'whiz', 'whydtm', 'wibamu', 'wibni', 'wiifm', 'wiify', 'wiiwii', 'wilb', 'wilco', 'wimp', 'wip', 'wirld', 'wisp', 'wit', 'witfits', 'witw', 'wk', 'wkewl', 'wknd', 'wkyp', 'wlmirl', 'wlu', 'wlu2', 'wmby', 'wmhgb', 'wmmows', 'wmpl', 'wndy', 'wnohgb', 'woa', 'wog', 'woke', 'wom', 'wombat', 'womobijo', 'womw', 'woot', 'wop', 'word', 'wot', 'wotam', 'wotd', 'wp', 'wrm', 'wrt', 'wru', 'wrud', 'wrudatm', 'wsu', 'wt', 'wtas', 'wtb', 'wtdb', 'wtf', 'wtfdyjs', 'wtfgda', 'wtfh', 'wtfwycm', 'wtfytt', 'wtg', 'wtg4a\\\\%/', 'wtgp', 'wth', 'wthin', 'wthow', 'wtmc', 'wtmi', 'wtn', 'wts', 'wtsds', 'wtshtf', 'wttm', 'wttp', 'wtwt', 'wubb', 'wubg', 'wud', 'wuf', 'wut', 'wuwh', 'wuwhima', 'wuz', 'wuz4dina', 'wuzup', 'wwba', 'wwd', 'wwg1wga', 'wwjd', 'wwno', 'wwsd', 'wwtt', 'www', 'wwy', 'wx', 'wycm', 'wyd', 'wyfm', 'wygiswypf', 'wym', 'wymyn', 'wyp', 'wyrn', 'wys', 'wysilob', 'wysiwyg', 'wyslpg', 'wyt', 'wytb', 'wyw', 'wywh', 'x', 'x-i-10', 'x.x', 'xaxa', 'xb', 'xbf', 'xc', 'xl', 'xlnt', 'xme', 'xo', 'xoxo', 'xoxozzz', 'xqzt', 'xtc', 'xxcc', 'y', 'ya yaya', 'yaba', 'yacc', 'yaf', 'yafiygi', 'yajwd', 'yaotm', 'yarbwyr', 'yatfm', 'yati', 'yaun', 'yb', 'ybf', 'ybs', 'yby', 'ybysa', 'ycmtsu', 'ycmu', 'yct', 'ydkm', 'yeppies', 'yf', 'ygbk', 'ygbsm', 'yglt', 'ygm', 'ygtbk', 'ygti', 'ygwypf', 'yhm', 'yic', 'yimby', 'yite', 'yiwgp', 'ykw', 'ykwim', 'ylh', 'yllo', 'ylw', 'ym', 'ymak', 'ymal', 'ymbkm', 'ymmd', 'ymmv', 'ymybnycsii', 'yngbt', 'yni', 'ynk', 'yobwoc', 'yoco', 'yofo', 'yolo', 'yolo', 'yooper', 'you', 'yoyo', 'yr', 'yro', 'yryocc', 'ys', 'ysan', 'ysdiw8', 'ysic', 'ysk', 'ysvw', 'ysyd', 'ytb', 'ytrnw', 'yts', 'yttm', 'yttt', 'yttwroomm', 'yumpi', 'yuppies', 'yvw', 'yw', 'ywia', 'yy4u', 'yyssw', 'z', 'zerg', 'zero', 'zit', 'zmg or zomg', 'zzz']

        slangs=slangs_1 + slangs_2 + slangs_3 + slangs_4 + slangs_5 + slangs_6

        return slangs

    def is_valid_name(self, name):
        import re
        if name in ['na','n/a','', ' ']:
          return False

        name=''.join([c for c in name if c.isalpha()])
        name=name.replace("-",' ').replace('_',' ').replace('.',' ').lower()

        if name in ['name','nome','hey', 'hi', 'hello', 'heyy', 'helllo', 'hola', 'first','last','test','notgiven','noname','valued customer','customer','value','anycart','albertsons','safeway']:
          return False

        profane_words=self._get_profane_words()
        _adverbs_0=[x for x in self._get_adverbs() if not x in ['daily','frankly','swiftly','solemnly']]
        _adverbs_1=[x.split("ly")[0] for x in _adverbs_0 if not x in ['daily','frankly','swiftly','solemnly']]
        adverbs=_adverbs_0+_adverbs_1
        adjectives=self._get_adjectives()
        body_parts=self._get_body_parts_name()
        slang_words=self._get_common_slangs()
        slang_body_parts=self._get_slang_body_parts()
        possessive_adjectives=self._get_possessive_adjectives()

        invalid_names=profane_words+adverbs+adjectives+slang_words

        ## check for patterns

        regex_patterns=['notgiven','noname','customer','value','anycart','albertsons','safeway']
        regex_patterns+=slang_body_parts

        ## make a set for fast lookup
        abusive_names_patterns=set(invalid_names + body_parts + slang_body_parts)
        possessive_adjectives_set=set(possessive_adjectives)
        ## if name is an abusive name, return True else, check if comes with some body part names, and check for abusive pattern name

        if name in abusive_names_patterns:
            return False

        else:
            for p in regex_patterns:
                pattern=re.compile(p)
                if re.findall(pattern=pattern, string=name):
                    name=name.replace(p,'')
                    name=self.lemmatizer.lemmatize(name)
                    name=name.replace("ly",'').replace('ing','')

                    if name in abusive_names_patterns:
                        return False
                    for a in possessive_adjectives_set:
                        if a in name:
                            return False

        return True

    # for p in abusive_names_patterns:
    #   patt=re.compile(p)
    #   if re.findall(pattern=patt, string=name):
    #     return False

    # return True

    def get_valid_name(self, name):

        if self.is_valid_name(name):
            name=''.join([c for c in name if c.isalpha()])
            name=name.replace("-",' ').replace('_',' ').replace('.',' ').lower()
            return name
        else:
            return ''

    def _get_abusive_words_list(self):

        profane_words=self._get_profane_words()
        _adverbs_0=[x for x in self._get_adverbs() if not x in ['daily','frankly','swiftly','sweetly','solemnly']]
        _adverbs_1=[x.split("ly")[0] for x in _adverbs_0 if not x in ['daily','frankly','swiftly','sweetly','solemnly']]
        adverbs=_adverbs_0+_adverbs_1
        adjectives=self._get_adjectives()
        body_parts=self._get_body_parts_name()
        slang_words=self._get_common_slangs()
        slang_body_parts=self._get_slang_body_parts()

        invalid_names=profane_words+adverbs+adjectives+slang_words+slang_body_parts

        ## check for patterns

        regex_patterns=['notgiven','noname','customer','value','anycart','albertsons','safeway']
        abusive_names_patterns=invalid_names
        abusive_names_patterns+=body_parts
        abusive_names_patterns=list(set(abusive_names_patterns))

        return abusive_names_patterns+regex_patterns


class similarityFunctions:

    """
    Implementation of various similarity and distance functions such as levenshtein distance, levenshtein ratio, damerauLevenshtein simi, jaro
    winkler simi, and generalized version of these which is weighted measure by taking subsets of strings as components and thier simi as measure.
    Also implemented hamming distance, and various string cleaning methods such as get cleaned version of alpha, alphnumeric strings
    """

    def __init__(self):
        pass


    #### Similarity functions¶

    def get_out_of_order_alpha_score(self,fn1,fn2):
        import re
        fn1=get_cleaned_alpha(fn1)
        fn2=get_cleaned_alpha(fn2)
        fn1s = re.split("\W+|_", fn2)
        fn2s = re.split("\W+|_", fn2)
        score = len(Counter(fn2s) & Counter(fn1s))/float(max(len(fn1s), len(fn2s)))
        return score


    def get_out_of_order_alpha_numeric_score(self,fn1,fn2):
        import re
        fn1=get_cleaned_alpha_numeric(fn1)
        fn2=get_cleaned_alpha_numeric(fn2)
        fn1s = re.split("\W+|_", fn2)
        fn2s = re.split("\W+|_", fn2)
        score = len(Counter(fn2s) & Counter(fn1s))/float(max(len(fn1s), len(fn2s)))
        return score


    def get_alpha_hamming_distance(self,s1,s2):
        import rapidfuzz
        s1=get_cleaned_alpha(s1);
        s2=get_cleaned_alpha(s2);
        if len(s1)==len(s2):
            return rapidfuzz.distance.Hamming.normalized_distance(s1,s2)
        if len(s1)>len(s2):
            t1=" "*(len(s1)-len(s2))+s2
            d1=rapidfuzz.distance.Hamming.normalized_distance(s1,t1)
            return d1
        else:
            t2=" "*(len(s2)-len(s1))+s1
            d2=rapidfuzz.distance.Hamming.normalized_distance(s2,t2)
        return d2


    def get_alpha_numeric_hamming_distance(self,s1,s2):
        import rapidfuzz
        s1=get_cleaned_alpha_numeric(s1);
        s2=get_cleaned_alpha_numeric(s2);
        if len(s1)==len(s2):
            return rapidfuzz.distance.Hamming.normalized_distance(s2,t2)
        if len(s1)>len(s2):
            t1=" "*(len(s1)-len(s2))+s2
            d1=rapidfuzz.distance.Hamming.normalized_distance(s2,t2)
            return d1
        else:
            t2=" "*(len(s2)-len(s1))+s1
            d2=rapidfuzz.distance.Hamming.normalized_distance(s2,t2)
            return d2


    def get_normalized_alpha_hamming_distance(self,s1,s2):
        fn1=get_cleaned_alpha(s1);
        fn2=get_cleaned_alpha(s2)
        hd=get_alpha_hamming_distance(fn1,fn2)
        if len(fn1)==0 and len(fn2)==0:
            return 0
        if len(s1)>len(s2):
            return hd/len(s1)
        else:
            return hd/len(s2)
        return d2


    def get_normalized_alpha_numeric_hamming_distance(self,s1,s2):
        fn1=get_cleaned_alpha_numeric(s1);
        fn2=get_cleaned_alpha_numeric(s2)
        hd=get_alpha_numeric_hamming_distance(fn1,fn2)
        if len(fn1)==0 and len(fn2)==0:
            return 0
        if len(s1)>len(s2):
            return hd/len(s1)
        else:
            return hd/len(s2)
        return d2


    def get_alpha_levenshtein_distance(self,s1,s2):
        import rapidfuzz
        fn1=get_cleaned_alpha(s1);
        fn2=get_cleaned_alpha(s2)
        return rapidfuzz.distance.Levenshtein.normalized_distance(fn1,fn2)


    def get_alpha_numeric_levenshtein_distance(self,s1,s2):
        import rapidfuzz
        fn1=get_cleaned_alpha_numeric(s1);
        fn2==get_cleaned_alpha_numeric(s2)
        return rapidfuzz.distance.JaroWinkler.normalized_distance(fn1,fn2)

    def get_alpha_damerauLevenshtein_similarity(self,s1,s2):
        import rapidfuzz
        fn1=get_cleaned_alpha(s1);
        fn2=get_cleaned_alpha(s2);
        return 1-rapidfuzz.distance.DamerauLevenshtein.normalized_distance(fn1,fn2)

    def get_alpha_numeric_damerauLevenshtein_similarity(self,s1,s2):
        import rapidfuzz
        fn1=get_cleaned_alpha_numeric(s1);
        fn2=get_cleaned_alpha_numeric(s2)
        return 1-rapidfuzz.distance.DamerauLevenshtein.normalized_distance(fn1,fn2)


    def get_alpha_jaro_winkler_similarity(self,s1,s2):
        import rapidfuzz
        fn1=get_cleaned_alpha(s1);
        fn2=get_cleaned_alpha(s2)
        return 1-rapidfuzz.distance.JaroWinkler.normalized_distance(fn1,fn2)


    def get_alpha_numeric_jaro_winkler_similarity(self,s1,s2):
        import rapidfuzz
        fn1=get_cleaned_alpha_numeric(s1);
        fn2=get_cleaned_alpha_numeric(s2)
        return rapidfuzz.distance.JaroWinkler.normalized_similarity(fn1,fn2)


    def get_generalized_jaro_winkler_similarity(self,s1,s2):
        from itertools import zip_longest
        if s1=='' or s2=='':
            return 0
        s1=s1.lower()
        s2=s2.lower()
        t1=''
        t2=''
        jw_dist=0; cnt=0
        for a,b in zip_longest(s1,s2):
            if a:
                t1=t1+a
            if b:
                t2=t2+b
            cnt+=1
            jw_dist+=self.get_alpha_numeric_jaro_winkler_similarity(t1,t2)
        return jw_dist/cnt

    def get_generalized_damerauLevenshtein_similarity(self,s1,s2):
        from itertools import zip_longest
        if s1=='' or s2=='':
            return 0
        s1=s1.lower()
        s2=s2.lower()
        t1=''
        t2=''
        simi=0; cnt=0
        for a,b in zip_longest(s1,s2):
            if a:
                t1=t1+a
            if b:
                t2=t2+b
            cnt+=1
            simi+=self.get_alpha_numeric_damerauLevenshtein_similarity(t1,t2)
        return simi/cnt
