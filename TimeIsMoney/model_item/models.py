from django.db import models
from pathlib import Path
import urllib.request, urllib.error
from django.conf import settings

class Item(models.Model):
    itemId = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, default='Unknown')
    sellPrice = models.CharField(max_length=255, null=True, default="0")
    icon = models.CharField(max_length=255, default='unknown')
    quality = models.IntegerField(default=0)
    itemClass = models.IntegerField(default=0)
    itemSubClass = models.IntegerField(default=0)
    inventoryType = models.IntegerField(default=0)

    class Meta:
        db_table = 'item'
        indexes = [
            models.Index(fields=['itemId'])
        ]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Check if exist icon if not download and do super

        if self.icon:
            # Blizzard icon media url patterns
            url = 'http://media.blizzard.com/wow/icons/'
            icon_str = str(self.icon)
            # Example link http://media.blizzard.com/wow/icons/56/inv_misc_gem_x4_rare_uncut_blue.jpg

            if not Path(settings.MEDIA_ROOT+'icons/18/'+icon_str+'.jpg').is_file():
                # Download 18x18 icon file
                try:
                    urllib.request.urlretrieve(url+'18/'+icon_str+'.jpg', settings.MEDIA_ROOT+'icons/18/'+icon_str+'.jpg')
                except urllib.error.URLError as e:
                    print(e)
            if not Path(settings.MEDIA_ROOT+'icons/36/'+icon_str+'.jpg').is_file():
                # Download 36x36 icon file
                try:
                    urllib.request.urlretrieve(url+'36/'+icon_str+'.jpg', settings.MEDIA_ROOT+'icons/36/'+icon_str+'.jpg')
                except urllib.error.URLError as e:
                    print(e)
            if not Path(settings.MEDIA_ROOT+'icons/56/'+icon_str+'.jpg').is_file():
                # Download 56x56 icon file
                try:
                    urllib.request.urlretrieve(url+'56/'+icon_str+'.jpg', settings.MEDIA_ROOT+'icons/56/'+icon_str+'.jpg')
                except urllib.error.URLError as e:
                    print(e)

        super(Item, self).save()

        return
