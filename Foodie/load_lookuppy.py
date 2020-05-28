from bs4 import BeautifulSoup
import requests
import pprint

def cities_func(filename):
    r  = requests.get("https://en.wikipedia.org/wiki/Classification_of_Indian_cities")
    soup = BeautifulSoup(r.text,'html.parser')
    tag=soup.find_all('td')
    tag1=tag[0].text
    tag2=tag[1].text
    tag3=tag[2].text
    tag4=tag[3].text
    cities=[i.replace('\n','').lower().strip() for i in tag4.split(',')+tag2.split(',')]

    synonyms=['bengaluru','bengalur','bangaluru','banglor','chenai','madras','chennapatnam',
              'kolkatha','culcutta','kochin','cochin','bombay','Bombay','mambai','mumby',
              'amaravati','golden city','goldencity','golden-city','holy city','holy-city',
              'holycity','bareily','baraily','nath-nagari','nathnagari','balgaum',
              'belagavi','bokaro','bokaro city','bokaro-steel city','bokaro steel-city',
              'bokaro-steel-city','jharkhand','nasik','kovai','Coyamuthur','nagpore',
              'durg bhilai','durg nagar','durg Bhilai','city of glass','suhag nagari',     
              'gurugram','hubbali','calicut','mysuru','puducherry','trivandrum',
               'trichur','Trichy','Tiruchi','vasai-virar','vasai','bazawada','vizag']
    
    cities=cities+synonyms
    with open(filename, mode="w") as outfile: 
        for i in cities:
            outfile.write("%s\n" % i)
    print('***  Look up for City Loaded ***')

def cuisines_func(filename):
    
    cuisines=['chinese','mexican','italian','american','south indians','north indian']
    
    synonyms=['chines','china','amarican','America','Amarica','americana',
    'Maxican','Mexicen','Mexico','mexicana','southindian','southindia',
    'south-indian','South-Indian','south india','indian','northindian',
    'north-indian','nothindia','North-Indian','north-india','north india',
    'north']
    
    cuisines=cuisines+synonyms
    
    with open(filename, mode="w") as outfile: 
        for i in cuisines:
            outfile.write("%s\n" % i)
    print('***  Look up for Cuisines Loaded ***')