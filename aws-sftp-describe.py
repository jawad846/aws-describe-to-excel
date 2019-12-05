import boto3
session = boto3.Session(profile_name='XXXXXXXXXX')

sftp_client = session.client('transfer')
import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_describe_instances = ('Describe_sftp_XXXXXXXXXX' + time + '.csv')
fieldnames = ['ServerId','Arn', 'IdentityProviderType', 'EndpointType','LoggingRole', 'State', 'UserCount']
with open(filename_describe_instances, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)
    for sftp in sftp_response['Servers']:
        raw =  [ sftp['ServerId'], sftp['Arn'], sftp['IdentityProviderType'], sftp['EndpointType'], sftp['LoggingRole'],
          sftp['State'],sftp['UserCount'] ]
        writer.writerow(raw)
        for o in raw:
            o = 'NULL'
            raw = []


csvFile.close()
