import boto3
session = boto3.Session(profile_name='xxxxxxxxx')

efs_client = session.client('efs', region_name = 'eu-west-1')
efs_response = efs_client.describe_file_systems()

import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_describe_EFS = ('EFS_xxxxxxxxx' + time + '.csv')
fieldnames = ['Name' , 'FileSystemId','CreationTime', 'LifeCycleState',
          'NumberOfMountTargets' , 'PerformanceMode' , 'Encrypted' , 'ThroughputMode' ,
          'PerformanceMode' ]


with open(filename_describe_EFS, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)
    raw = []
    for efs_id in efs_response['FileSystems']:
        efs_filesystemid = efs_id['FileSystemId']
        efs_creationtime = efs_id['CreationTime'].date()
        efs_Lifecyclestate = efs_id['LifeCycleState']
        try:
            efs_Name = efs_id['Name']
        except Exception as e:
            efs_Name = "NOT_APPLICABLE"
            print(e)
        efs_MountTarget = efs_id['NumberOfMountTargets']
        efs_performancemode = efs_id['PerformanceMode']
        efs_encrypt_status = efs_id['Encrypted']
        efs_throughputmode = efs_id['ThroughputMode']
        efs_performancemode = efs_id['PerformanceMode']

        raw = [efs_Name,efs_filesystemid,efs_creationtime,efs_Lifecyclestate,efs_MountTarget, efs_performancemode,
               efs_encrypt_status, efs_throughputmode, efs_performancemode ]

        print (raw   )
        writer.writerow(raw)
        for o in raw:
            o = 'NULL'
        raw = []
csvFile.close()
