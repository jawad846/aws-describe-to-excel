import boto3
##I
#ec2 = boto3.client('ec2',
#                    aws_access_key_id='',
#                    aws_secret_access_key='+',
#                    region_name='eu-west-1')
#response = ec2.describe_instances()

session = boto3.Session(profile_name='xxxxxxxxxxxxx')
ec2 = session.client('ec2', region_name='eu-west-1')
response = ec2.describe_instances()


import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_describe_instances = ('Describe_Instances_eu-west-1_xxxxxxxxxxxx' + time + '.csv')
fieldnames = ['Instance_Name','ImageId', 'InstanceId', 'InstanceType','KeyName', 'LaunchTime',
              'Monitoring_State','Availability_Zone','GroupName', 'Tenancy', 'Platform',
              'Instance_OS','PrivateDnsName', 'PrivateIpAddress', 'PublicDnsName','PublicIpAddress',
              'State', 'SubnetId','VpcId', 'Architecture', 'EBS_List','Instance_Arn',
              'network_interface_list', 'security_group_list', 'tags_list',
              'ENVIRONMENT' , 'OS','PROJECT_NAME','EX_OWNER','ET_OWNER', 'APPLICATION_NAME',
              'APPLICATION_TYPE', 'TIER_LEVEL', 'VENDOR_NAME','REGION', 'MSP','DESCRIPTION', 'NAME']



with open(filename_describe_instances, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)
    for Reserv in response['Reservations']:
        for Insta in Reserv['Instances']:
            instance_imageid = Insta.get('ImageId', 'NULL')
            instance_InstanceId = Insta.get('InstanceId', 'NULL')
            instance_InstanceType = Insta.get('InstanceType', 'NULL')
            instance_KeyName = Insta.get('KeyName', 'NULL')
            instance_LaunchTime = Insta.get('LaunchTime', 'NULL')
            instance_Monitoring_State = Insta['Monitoring'].get('State', 'NULL')
            instance_Availability_Zone = Insta['Placement'].get('AvailabilityZone', 'NULL')
            instance_GroupName = Insta['Placement'].get('GroupName', 'NULL')
            instance_tenancy = Insta['Placement'].get('Tenancy', 'NULL')
            instance_Platform = Insta.get('Platform', 'NULL')
            instance_Private_DNS = Insta.get('PrivateDnsName', 'NULL')
            instance_Private_IP = Insta.get('PrivateIpAddress', 'NULL')
            instance_Public_DNS = Insta.get('PublicDnsName', 'NULL')
            instance_Public_IP = Insta.get('PublicIpAddress', 'NULL')
            instance_State = Insta['State'].get('Name', 'NULL')
            instance_Subnet = Insta.get('SubnetId', 'NULL')
            instance_VPCID = Insta.get('VpcId', 'NULL')
            instance_Arch = Insta.get('Architecture', 'NULL')
            #print(instance_imageid,instance_InstanceId,instance_InstanceType,instance_KeyName,instance_LaunchTime,instance_Monitoring_State,instance_Availability_Zone,instance_GroupName,instance_tenancy,instance_Platform,instance_Private_DNS,instance_Private_IP,instance_Public_DNS,instance_Public_IP,instance_State,instance_Subnet,instance_VPCID,instance_Arch)

            ebs_list = []
            for j in Insta.get('BlockDeviceMappings', 'NULL'): ##Selecting from the tags
                ebs_vol = [j.get('DeviceName', 'NULL'), 'DeleteOnTermination',
                           j['Ebs'].get('DeleteOnTermination', 'NULL'),
                           j['Ebs'].get('Status', 'NULL'),
                           j['Ebs'].get('VolumeId', 'NULL')]
                ebs_list.append(ebs_vol)

            try:
                instance_Arn = Insta['IamInstanceProfile'].get('Arn','NULL')
            except KeyError:
                instance_Arn = 'Null'
                pass


            network_interface_list = []
            for k in Insta['NetworkInterfaces']: ##Selecting from the NetworkInterfaces
                for l in k.get('PrivateIpAddresses', 'NULL'):
                    if l.get('Association', 'NULL') != 'NULL':
                        network_interface = [l['Association'].get('PublicDnsName', 'NULL'),
                                             l['Association'].get('PublicIp', 'NULL'),
                                             l.get('PrivateDnsName', 'NULL'),
                                             l.get('PrivateIpAddress', 'NULL')]
                        network_interface_list.append(network_interface)

            security_group_list = []
            for m in Insta.get('SecurityGroups', 'NULL'): ##Selecting from the NetworkInterfaces
                security_group = [m.get('GroupName', 'NULL'), m.get('GroupId', 'NULL')]
                security_group_list.append(security_group)

            tags_list = []
            for n in Insta.get('Tags', 'NULL'): ##Selecting from the tags
                #print(n)
                #print("-----")
                #print(n.get('Value', 'NULL'))
                if n.get('Key', 'NULL') == 'ENVIRONMENT':
                    instance_ENVIRONMENT = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'OS':
                    instance_OS = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'PROJECT_NAME':
                    instance_PROJECT_NAME = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'EX_OWNER':
                    instance_EX_OWNER = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'ET_OWNER':
                    instance_ET_OWNER = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'APPLICATION_NAME':
                    instance_APPLICATION_NAME = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'APPLICATION_TYPE':
                    instance_APPLICATION_TYPE = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'TIER_LEVEL':
                    instance_TIER_LEVEL = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'VENDOR_NAME':
                    instance_VENDOR_NAME = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'REGION':
                    instance_REGION = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'MSP':
                    instance_MSP = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'DESCRIPTION':
                    instance_DESCRIPTION = n.get('Value', 'NULL')
                if n.get('Key', 'NULL') == 'NAME':
                    instance_NAME = n.get('Value', 'NULL')
                if n == 'N':
                    instance_Name = "NULL"
                    break
                else:
                    tag = [n.get('Key', 'NULL'), n.get('Value', 'NULL')]
                    tags_list.append(tag)
                    if n.get('Key', 'NULL') == 'Name':
                        instance_Name = n.get('Value', 'NULL')
                    if n.get('Key', 'NULL') == 'OS':
                        instance_OS = n.get('Value','NULL')




#            raw = [instance_Name,instance_imageid,instance_InstanceId,instance_InstanceType,instance_KeyName,instance_LaunchTime,instance_Monitoring_State,instance_Availability_Zone,instance_GroupName,instance_tenancy,instance_Platform,instance_OS,instance_Private_DNS,instance_Private_IP,instance_Public_DNS,instance_Public_IP,instance_State,instance_Subnet,instance_VPCID,instance_Arch,ebs_list,instance_Arn,network_interface_list,security_group_list,tags_list]
            raw = [instance_Name,
                   instance_imageid,
                   instance_InstanceId,
                   instance_InstanceType,
                   instance_KeyName,
                   instance_LaunchTime,
                   instance_Monitoring_State,
                   instance_Availability_Zone,
                   instance_GroupName,
                   instance_tenancy,
                   instance_Platform,
                   instance_OS,
                   instance_Private_DNS,
                   instance_Private_IP,
                   instance_Public_DNS,
                   instance_Public_IP,
                   instance_State,
                   instance_Subnet,
                   instance_VPCID,
                   instance_Arch,
                   ebs_list,
                   instance_Arn,
                   network_interface_list,
                   security_group_list,
                   tags_list,
                   instance_ENVIRONMENT,
                   instance_OS,
                   instance_PROJECT_NAME,
                   instance_EX_OWNER,
                   instance_ET_OWNER,
                   instance_APPLICATION_NAME,
                   instance_APPLICATION_TYPE,
                   instance_TIER_LEVEL,
                   instance_VENDOR_NAME,
                   instance_REGION,
                   instance_MSP,
                   instance_DESCRIPTION,
                   instance_NAME]



            writer.writerow(raw)
            for o in raw:
                o = 'NULL'
            raw = []
            #print("===")

csvFile.close()
