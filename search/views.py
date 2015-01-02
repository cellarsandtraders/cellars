from django.conf import settings
from brewerydb import BreweryDb
from utils import json_response

BreweryDb.configure(
    settings.BREWERYDB_API_KEY,
    settings.BREWERYDB_BASEURI
)


def search(request):
    if request.method == 'GET' and request.GET.get('q'):
        results = BreweryDb.search({'type': 'beer', 'q': request.GET['q']})
        return json_response(results)

    elif request.method == 'OPTIONS':
        return json_response({})

    else:
        return json_response({'error': "Bad Request"}, status=400)
