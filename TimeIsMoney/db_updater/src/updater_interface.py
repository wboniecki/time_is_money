'''
wboniecki 2017-11-12
Interface class for updater contains most common reusable methods.
Includes settings file with apiKey, valid regions and locale.
'''
from db_updater.src import settings
import urllib.request, json, http.client

class UpdaterInterface():

    # Class contstructor, must contains region
    def __init__(self, region):
        self.region = region

    # Returns blizz API key defined in settings file
    def getApiKey(self):
        return settings.APIKEY

    # Returns JSON data from url defined in parameter
    def getApiLinkData(self, url):
        try:
            request = urllib.request.urlopen(url).read()
            return json.loads(request.decode('utf-8'))
        except http.client.IncompleteRead as e:
            request = e.partial

    # Returns locale defined in settings
    def getLocale(self):
        if self.region in settings.REGIONS_LOCALES:
            return settings.REGIONS_LOCALES[self.region]
        else:
            return None

    # Return true if region param exist in settings file
    def isRegionValid(self):
        return self.region in settings.REGIONS

