GAME_NAME = """TIPS: TEXT-BASED INACCURATE PLAGARISM SIMULATOR"""

BACKGROUND_SQUARES = {'width': 18,'height': 18}
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_WIDTH = SCREEN_WIDTH/BACKGROUND_SQUARES['width']
GRID_HEIGHT = SCREEN_HEIGHT/BACKGROUND_SQUARES['height']
MAIN_MENU_BUTTON_WIDTH = 200

INITIATIVE_NUMBER_OF_POSIBILITIES = 10

MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 6

DEFAULT_MONEY_LIMIT = 500

DEFAULT_GAME_VERSION = 3
GAME_VERSION_OPTIONS = [1,2,3]

INITIATIVE_EXPLANATION = '''Initiative turned on. Units will roll initiative.'''
INITIATIVE_DISABLED_EXPLANATION = '''Initiative turned off. Units take their turns at the same time.'''

VARIANCE_EXPLANATION = '''Variability turned on. Units roll for initiative and damage.'''
VARIANCE_DISABLED_EXPLANATION = '''Variability turned off. Units always roll max for attacks and initiative.'''

WARNING_CHANGE_GAME_VERSION_BATTLE_CREATOR = '''Changing game version will recalculate the value of units. You may have to sell units in order to start the battle.
Are you sure you want to switch game version?'''

WARNING_OUTDATED_UNITS = '''Moving from a lower game version to a higher one will sell units from earlier versions.'''

ERROR_LOG_URI = "debug/errors.log"

FIREBASE_API_KEY = "AIzaSyC_MNFuibE5GlmJMqLqEkrjgoAGt-4DRk8"
#Unlike any other api key, Google says this is safe to expose, 
# so long as you restrict api requesttraffic to your billing expectations to prevent attacks

FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"

FIRESTORE_DB_NAME = "piono-pricing"

ARENA_SLOT_1 = {
    'first_unit_center': {'x': (GRID_WIDTH)*5 + GRID_WIDTH, 'y': (GRID_HEIGHT*2)},
    'unit_spacing': {'x': GRID_WIDTH, 'y': 0},
    'row_spacing': {'x': 0, 'y': GRID_HEIGHT}
}

ARENA_SLOT_2 = {
    'first_unit_center': {'x': (GRID_WIDTH)*5 - GRID_WIDTH, 'y': (GRID_HEIGHT*12) - GRID_HEIGHT},
    'unit_spacing': {'x': GRID_WIDTH, 'y': 0},
    'row_spacing': {'x': 0, 'y': GRID_HEIGHT}
}

HEALTH_INDICATOR_BAR_OFFSET = 32
INITIATIVE_INDICATOR_BAR_OFFSET = -32
ATTACK_ANIMATION_SPEED = 1
DEFAULT_UNIT_SCALE = 0.25