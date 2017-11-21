import datetime
from .models import AuctionDailyStats
from .serializer import AuctionDailyStatsSerializer

from model_realm.services.realm_service import RealmService


class AuctionDailyStatsService:

    def _create(self, connected_realm_id):
        stats = AuctionDailyStats()
        stats.connected_realm = connected_realm_id
        stats.save()

    def update(self, created, updated, deprecated, realm_name):
        realm_service = RealmService()
        connected_realm_id = realm_service.getRealmConnectedRealmId(realm_name)
        if connected_realm_id is not None:
            today = datetime.date.today()
            stats = AuctionDailyStats.objects.filter(date=today, connected_realm=connected_realm_id).first()
            if stats:
                # UPDATE
                stats.created += created
                stats.updated += updated
                stats.deprecated += deprecated
                stats.total += created + updated + deprecated
                stats.save()
            else:
                # CREATE
                self._create(connected_realm_id)
                self.update(created, updated, deprecated, realm_name)

