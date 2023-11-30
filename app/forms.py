from django import forms


class CoordsForm(forms.Form):
    latitude = forms.FloatField(label='緯度', min_value=-90.0, max_value=90.0)
    longitude = forms.FloatField(label='経度', min_value=-180.0, max_value=180.0)
