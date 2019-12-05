import boto3
session = boto3.Session(profile_name='xxxxxxxxxxx')

rds_client = session.client('rds', region_name = 'eu-west-1')
response = rds_client.describe_db_instances()
import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_describe_elb= ('Describe_RDS_eu-west-1_xxxxxxxxxxxxx' + time + '.csv')
fieldnames = [ 'DBInstanceIdentifier' , 'DBInstanceClass' , 'Engine' ,
              'DBInstanceStatus' , 'MasterUsername' , 'Endpoint_address'
              , 'Endpoint_port','AllocatedStorage' , 'InstanceCreateTime' ,
              'EngineVersion' , 'CopyTagsToSnapshot' ,
              'LicenseModel' , 'MultiAZ' , 'StorageType','StorageEncrypted' ,
            ]
with open(filename_describe_elb, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)
    for db in response['DBInstances']:
        raw = [ db['DBInstanceIdentifier'], db['DBInstanceClass'], db['Engine'], db['DBInstanceStatus'],
         db['MasterUsername'], db['Endpoint']['Address'],db['Endpoint']['Port'],
          db['AllocatedStorage'], db['InstanceCreateTime'].date(), db['EngineVersion'], db['CopyTagsToSnapshot'],
          db['LicenseModel'],db['MultiAZ'],db['StorageType'],db['StorageEncrypted'] ]
        print(raw)
        writer.writerow(raw)
csvFile.close()
print("Completed")
