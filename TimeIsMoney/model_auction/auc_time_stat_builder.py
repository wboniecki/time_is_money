import datetime
from .models import AuctionUpdateTimeStat
from model_realm.services import RealmService

class AuctionUpdateTimeStatBuilder:


    def __init__(self, time_start, crud_count, realm_name):
        self.time_start = time_start
        self.crud_count = crud_count
        self.connected_realm = RealmService().getRealmConnectedRealmId(realm_name)

    def save(self):
        stat = AuctionUpdateTimeStat()
        stat.date = datetime.date.today()
        stat.time_start = self.time_start
        stat.time_stop = datetime.datetime.now().time()
        stat.crud_count = self.crud_count
        stat.connected_realm = self.connected_realm

        stat.save()
