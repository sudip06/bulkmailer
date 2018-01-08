from operator import itemgetter
import random
with open("cred.csv") as file:
    for eachLine in file:
        loginid, website=itemgetter(0,2)(eachLine.split(':'))
        i=random.random()
        print loginid,website
