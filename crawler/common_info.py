import numpy as np

LOG_PREFIX = "[pLOG]"

DB_SYS_INFO = {
  'URL' : '192.168.0.112',
#  'URL' : 'localhost',
  'PORT' : 1521,
  'SID' : 'xe'
}

DB_USER_INFO = {
  'ID' : 'njs_master',
  'PASSWORD' : '1234',
}

class NEWS_CLASS():
    SPORTS = 'sports'
    ENTERTAINMENT = 'entertainment'
    SOCIETY = 'society'
    POLITICS = 'politics'
    ECONOMIC = 'economic'
    INTERNATIONAL = 'foreign'
    CULTURE = 'culture'
    SCIENCE = 'digital'

CLASS_ENTERTAIN = np.array(['star', 'drama', 'variety', \
                            'music', 'movie'])

CLASS_SPORTS = np.array(['soccer', 'worldsoccer', \
                         'baseball', 'worldbaseball', \
                          'golf', 'basketball', 'volleyball', \
                            'esports', 'general'])
 
ENTERTAIN_URL = 'https://entertain.daum.net/'
SPORTS_URL = 'https://sports.daum.net/'

BASE_URL = 'https://news.daum.net/'
# SOCIETY_URL = BASE_URL + NEWS_CLASS.SOCIETY
# POLITICS_URL = BASE_URL + NEWS_CLASS.POLITICS
# ECONOMIC_URL = BASE_URL + NEWS_CLASS.ECONOMIC
# INTERNAIONAL_URL = BASE_URL + NEWS_CLASS.INTERNATIONAL
# CULTURE_URL = BASE_URL + NEWS_CLASS.CULTURE
# SCIENCE_URL = BASE_URL + NEWS_CLASS.SCIENCE