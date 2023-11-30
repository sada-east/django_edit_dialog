import json

from django.db import models


class Spot(models.Model):
    '''地図上のスポットのデータ
    '''
    name = models.CharField('名前', max_length=100)
    coords = models.JSONField('座標', default=dict)

    def __str__(self):
        return self.name

    def coords_str(self):
        '''座標を JSON 文字列で返す
        '''
        return json.dumps(self.coords, indent=4)

    def gmap_url(self):
        '''Google Maps のその座標の URL を返す
        '''
        coords = f'{self.coords["latitude"]}%2C{self.coords["longitude"]}'
        return 'https://www.google.com/maps/search/?api=1&query=' + coords
