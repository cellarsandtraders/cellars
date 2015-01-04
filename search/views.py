from django.conf import settings
from brewerydb import BreweryDb
from utils import json_response, endpoint

BreweryDb.configure(
    settings.BREWERYDB_API_KEY,
    settings.BREWERYDB_BASEURI
)


@endpoint
def search(request):
    if request.method == 'GET' and request.GET.get('q'):
        results = BreweryDb.search({'type': 'beer', 'q': request.GET['q']})
        return json_response(results)
