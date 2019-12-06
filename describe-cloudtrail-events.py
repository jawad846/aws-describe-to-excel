import boto3
from datetime import date, timedelta
import datetime
import collections
from collections import OrderedDict

print(datetime.datetime.now())

session = boto3.Session(profile_name='xxxxxxxx')
cloudt_cli = session.client('cloudtrail', region_name = 'eu-west-1')
cldevent = cloudt_cli.lookup_events( StartTime=str(date.today() - timedelta(days=1)), EndTime= str(date.today()) )



evnt = []
evnt_dict = {}
cldevent = cloudt_cli.lookup_events( StartTime=str(date.today() - timedelta(days=1)), EndTime= str(date.today()))

while True:

    print("+++++++++++++++++++")
    for i in cldevent['Events']:
        evnt.append(str(i['EventName']))

    try :
        if cldevent.get('NextToken','NULL') != 'NULL':
            cldevent = cloudt_cli.lookup_events( StartTime=str(date.today() - timedelta(days=1)), EndTime= str(date.today()), NextToken = cldevent.get('NextToken','NULL'))
        else:
            print("Bye")
            break
    except Exception as e:
        print(e)
        break


evnt_dict = {}
evnt_uniq = list(set(evnt))
for i  in evnt_uniq:
    edict = {}
    edict = {i : evnt.count(i)}
    evnt_dict.update(edict)



OrderedDict(evnt_dict.items())
OrderedDict(sorted(evnt_dict.items(), key = lambda t: t[1]))
D1 = dict(OrderedDict(sorted(evnt_dict.items(), key = lambda t: t[1])))
reverse_order_dict = dict(collections.OrderedDict(reversed(list(D1.items()))))

for i in reverse_order_dict.keys():
    print ('{:<40} {:<20}'.format(i, reverse_order_dict[i]))

print(datetime.datetime.now())
