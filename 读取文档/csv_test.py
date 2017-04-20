import csv
import urllib.request
from io import StringIO


# file = urllib.request.urlopen('http://pythonscraping.com/files/MontyPythonAlbums.csv').read().decode('ascii','ignore')
# dataFile = StringIO(file)

file = open('./MontyPythonAlbums.csv')

csvReader = csv.reader(file)
for row in csvReader:
    print(row[0], row[1])
# print(csvReader)
'''
csv.reader(file)
csv.DictReader()

AttributeError: module 'csv' has no attribute 'DictReader'     文件命名为csv.py导致报错

Name Year
Monty Python's Flying Circus 1970
Another Monty Python Record 1971
Monty Python's Previous Record 1972
The Monty Python Matching Tie and Handkerchief 1973
Monty Python Live at Drury Lane 1974
An Album of the Soundtrack of the Trailer of the Film of Monty Python and the Holy Grail 1975
Monty Python Live at City Center 1977
The Monty Python Instant Record Collection 1977
Monty Python's Life of Brian 1979
Monty Python's Cotractual Obligation Album 1980
Monty Python's The Meaning of Life 1983
The Final Rip Off 1987
Monty Python Sings 1989
The Ultimate Monty Python Rip Off 1994
Monty Python Sings Again 2014
'''