from django.shortcuts import render
from json import dumps
  
  
def send_dictionary(request):
    # create data dictionary
    while True:
        n = 0
        x = 0
        for n in range(1, 10):
            print(n)
            x+=1

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
        dataJSON = dumps(n)
        return render(request, 'landing.html', {'data': dataJSON})
    

    # RUN python manage.py runserver
