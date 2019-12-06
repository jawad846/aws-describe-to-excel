import boto3
session = boto3.Session(profile_name='XXXXXXX')

s3_client = session.client('s3', region_name = 'us-east-1')
s3_resource = session.resource('s3')

response = s3_client.list_buckets()

import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_describe_instances = ('s3_xxxxxxxx' + time + '.csv')
fieldnames = ['Bucket_Name','Bucket_Createddate', 'Policy' , 'ACL',
              's3_vendor_name', 's3_evironment', 's3_application_name', 's3_project_name']

with open(filename_describe_instances, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)
    raw = []
    for bucket in response['Buckets']:
        #print (bucket)
        bucket_name = bucket['Name']
        bucket_cdate = str(bucket['CreationDate'].date())

        print( bucket_name , bucket_cdate )
        bucket_policy = "Not_Configured"
        try:
            result = s3_client.get_bucket_policy(Bucket=bucket_name)
            #print(result['Policy'])
            bucket_policy = result['Policy']
        except Exception as e:
            if str(e).find("AccessDenied") != -1:
                print(e)
            else:
                bucket_policy = "Not_Configured"

        bucket_acl = "Not_Configured"
        try:
            result = s3_client.get_bucket_acl(Bucket=bucket_name)
            #print(result)
            bucket_acl = result['Grants']
        except Exception as e:
            if str(e).find("AccessDenied") != -1:
                print(e)
            else:
                bucket_acl = "Not_Configured"


        s3_vendor_name = "Not_Configured"
        s3_evironment = "Not_Configured"
        s3_application_name = "Not_Configured"
        s3_project_name = "Not_Configured"

        try:
            result = s3_client.get_bucket_tagging(Bucket=bucket_name)
            for tagkey in result['TagSet']:
                if tagkey['Key'] == 'VENDOR_NAME':
                    s3_vendor_name = tagkey['Value']
                if tagkey['Key'] == 'ENVIRONMENT':
                    s3_evironment = tagkey['Value']
                if tagkey['Key'] == 'APPLICATION_NAME':
                    s3_application_name = tagkey['Value']
                if tagkey['Key'] == 'PROJECT_NAME':
                    s3_project_name = tagkey['Value']
        except Exception as e:
            s3_vendor_name = "Not_Configured"
            s3_evironment = "Not_Configured"
            s3_application_name = "Not_Configured"
            s3_project_name = "Not_Configured"
            #print (e)


        raw= [bucket_name, bucket_cdate, bucket_policy, bucket_acl,
                s3_vendor_name,  s3_evironment,s3_application_name, s3_project_name ]
        writer.writerow(raw)
        #print(raw)
        for o in raw:
            o = 'NULL'
        raw = []

csvFile.close()
