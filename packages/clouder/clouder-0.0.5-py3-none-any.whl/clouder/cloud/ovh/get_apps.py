import ovh

from tabulate import tabulate


client = ovh.Client()
applications = client.get('/me/api/application')

table = []

for application in applications:
    print(application)