import boto3

#session = boto3.session.Session()

session = boto3.Session(profile_name='xxxxxxxxxxx')
ec2 = session.client('ec2', region_name='eu-west-1')
responsesg = ec2.describe_security_groups()


import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_security_group = ('Describe_SG_eu-west-1_xxxxxxxxxx' + time + '.csv') ##Edit the Name
fieldnames = ['SG_NAME','SG_ID', 'SG_OwnerId', 'SG_Description','SG_VPCID', 'SG_TAGS', 'Traffic_Type','Protocol','Port', 'CIDR/SG']

with open(filename_security_group, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)

    for SGS in responsesg['SecurityGroups']:
        SG_NAME = SGS.get('GroupName','NULL')
        SG_ID = SGS.get('GroupId','NULL')
        SG_OwnerId = SGS.get('OwnerId','NULL')
        SG_Description = SGS.get('Description','NULL')
        SG_VPCID = SGS.get('VpcId','NULL')

        tags_list = []
        for n in SGS.get('Tags', 'NULL'): ##Selecting from the tags
            #print(n)
            if n == 'N':
                #instance_Name = "NULL"
                break
            else:
                tag = [n.get('Key', 'NULL'), n.get('Value', 'NULL')]
                tags_list.append(tag)
                #To extract custom Key and Value
                #if n.get('Key', 'NULL') == 'Name':
                #    instance_Name = n.get('Value', 'NULL')
                #if n.get('Key', 'NULL') == 'OS':
                #    instance_OS = n.get('Value','NULL')
        #print(tags_list)
        SG_TAGS = tags_list


        for inbound in SGS.get('IpPermissions','NULL'):
            #print(inbound)
            #print(SGS.get('IpPermissions','NULL'))
            if inbound['IpProtocol'] == "-1":
                traffic_type="All Trafic"
                ip_protpcol="All"
                to_port="All"
            else:
                ip_protpcol = inbound['IpProtocol']
                from_port=inbound['FromPort']
                to_port=inbound['ToPort']
                #If ICMP, report "N/A" for port #
                if to_port == -1:
                    to_port = "N/A"

            #If source/target is an IP v4
            if len(inbound['IpRanges']) > 0:
                for ip_range in inbound['IpRanges']:
                    cidr_block_sg = ip_range['CidrIp']
                    raw = []
                    raw = [SG_NAME, SG_ID, SG_OwnerId, SG_Description, SG_VPCID, SG_TAGS, "Inbound",ip_protpcol,to_port, cidr_block_sg]
                    writer.writerow(raw)
            #If source/target is an IP v6
            if len(inbound['Ipv6Ranges']) > 0:
                for ip_range in inbound['Ipv6Ranges']:
                    cidr_block_sg = ip_range['CidrIpv6']
                    raw = []
                    raw = [SG_NAME, SG_ID, SG_OwnerId, SG_Description, SG_VPCID, SG_TAGS, "Inbound",ip_protpcol,to_port, cidr_block_sg]
                    writer.writerow(raw)
            #If source/target is a security group
            if len(inbound['UserIdGroupPairs']) > 0:
                for source in inbound['UserIdGroupPairs']:
                    cidr_block_sg = source['GroupId']
                    raw = []
                    raw = [SG_NAME, SG_ID, SG_OwnerId, SG_Description, SG_VPCID, SG_TAGS, "Inbound",ip_protpcol,to_port, cidr_block_sg]
                    writer.writerow(raw)
            for o in raw:
                o = 'NULL'
            raw = []
            #print("Inbound",ip_protpcol, to_port, cidr_block_sg)

        for outbound in SGS.get('IpPermissionsEgress','NULL'):
            #print(outbound)
            if outbound['IpProtocol'] == "-1":
                traffic_type="All Trafic"
                ip_protpcol="All"
                to_port="All"
            else:
                ip_protpcol = outbound['IpProtocol']
                from_port=outbound['FromPort']
                to_port=outbound['ToPort']
                #If ICMP, report "N/A" for port #
                if to_port == -1:
                    to_port = "N/A"

            #If source/target an IP v4
            if len(outbound['IpRanges']) > 0:
                for ip_range in outbound['IpRanges']:
                    cidr_block_sg = ip_range['CidrIp']
                    raw = []
                    raw = [SG_NAME, SG_ID, SG_OwnerId, SG_Description, SG_VPCID, SG_TAGS, "Outbound",ip_protpcol,to_port, cidr_block_sg]
                    writer.writerow(raw)
            #If source/target is an IP v6
            if len(outbound['Ipv6Ranges']) > 0:
                for ip_range in outbound['Ipv6Ranges']:#
                    cidr_block_sg = ip_range['CidrIpv6']
                    raw = []
                    raw = [SG_NAME, SG_ID, SG_OwnerId, SG_Description, SG_VPCID, SG_TAGS, "Outbound",ip_protpcol,to_port, cidr_block_sg]
                    writer.writerow(raw)
            #If source/target is a security group
            if len(outbound['UserIdGroupPairs']) > 0:#
                for source in outbound['UserIdGroupPairs']:
                    cidr_block_sg = source['GroupId']
                    raw = []
                    raw = [SG_NAME, SG_ID, SG_OwnerId, SG_Description, SG_VPCID, SG_TAGS, "Outbound",ip_protpcol,to_port, cidr_block_sg]
                    writer.writerow(raw)
            for o in raw:
                o = 'NULL'
            raw = []
            #print("Outbound",ip_protpcol, to_port, cidr_block_sg)

csvFile.close()
