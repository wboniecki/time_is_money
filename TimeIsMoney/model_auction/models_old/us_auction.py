from .auction import Auction
from django.db import models

class AuctionUs(Auction):
    class Meta:
        app_label = 'model_auction'
        db_table = 'auctionUS'
        indexes = [
            models.Index(fields=['ownerRealm', 'owner']),
            models.Index(fields=['ownerRealm'])
        ]

