from django.shortcuts import render
from json import dumps
  
  
def send_dictionary(request):
    # create data dictionary

    n = 0
    for n in range(1, 10):
        print(n)

    dataDictionary = {
        'hello': 'World',
        'geeks': 'forgeeks',
        'ABC': 123,
        456: 'abc',
        14000605: 1,
        'list': ['zeeeeks', n, 'geeks'],
        'dictionary': {'you': 'can', 'send': 'anything', 3: 1}
    }
    # dump data
    dataJSON = dumps(dataDictionary)
    return render(request, 'landing.html', {'data': dataJSON})
