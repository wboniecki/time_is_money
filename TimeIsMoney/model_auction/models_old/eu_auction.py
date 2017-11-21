from .auction import Auction
from django.db import models

class AuctionEu(Auction):
    class Meta:
        app_label = 'model_auction'
        db_table = 'auctionEU'
        indexes = [
            models.Index(fields=['ownerRealm', 'auc']),
            models.Index(fields=['ownerRealm', 'owner']),
            models.Index(fields=['ownerRealm'])
        ]

