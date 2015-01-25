import requests
from django.conf import settings
from utils import json_response, endpoint
from utils.brewerydb import BreweryDb

BreweryDb.configure(
    settings.BREWERYDB_API_KEY,
    settings.BREWERYDB_BASEURI
)


@endpoint
def search(request):
    if request.method == 'GET' and request.GET.get('q'):
        try:
            results = BreweryDb.search({
                'type': 'beer',
                'withBreweries': 'Y',
                'q': request.GET['q']
            })
            return json_response(results)
        except requests.ConnectionError:
            return json_response({
                'error': 'Cannot connect to BreweryDb'
            }, status=503)
