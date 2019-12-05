import boto3
session = boto3.Session(profile_name='xxxxxxxx')

elb_client = session.client('elbv2', region_name = 'eu-west-1')
response = elb_client.describe_load_balancers()
import datetime
import csv
time = datetime.datetime.now().strftime ('%Y-%m-%d-%H-%M-%S')
filename_describe_elb= ('Describe_ELB_eu-west-1_xxxxxxxxx' + time + '.csv')

fieldnames = [ 'Elb_ARN' , 'Elb_Name' , 'Elb_Type' , 'Elb_Scheme' , 'Elb_Dns' , 'Elb_VPCID' , 'Elb_LaunchTime' ,
            'Elb_IPType' , 'Elb_state' , 'Elbv2az_list' , 'Elb_Sg' , 'listner_ARN' , 'listner_port' , 'listner_proto' ,
            'Rules_ARN' , 'Rules_Priority' , 'Rules_Condition' , 'Rules_Action_Type' , 'Rules_Targetgrp_Arn' ,
            'Rules_Targetgrp_Name' ,'Targetgrp_Type' ,  'Targetgrp_Protocole' , 'Targetgrp_Port' , 'Targetgrp_Vpcid' ,
            'Targetgrp_Health_Protocole' , 'Targetgrp_Healthport' , 'Targetgrp_Healthenable' ,
            'Rules_targetgrp_health' ]

with open(filename_describe_elb, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(fieldnames)
    for elbv2 in response['LoadBalancers']:
        #print("===================")
        Elb_ARN = elbv2.get("LoadBalancerArn","NOT_APPLICABLE")
        Elb_Name = elbv2.get("LoadBalancerName","NOT_APPLICABLE")
        Elb_Type = elbv2.get("Type","NOT_APPLICABLE")
        Elb_Scheme = elbv2.get("Scheme","NOT_APPLICABLE")
        Elb_Dns = elbv2.get("DNSName","NOT_APPLICABLE")
        Elb_VPCID = elbv2.get("VpcId","NOT_APPLICABLE")
        Elb_LaunchTime = elbv2.get("CreatedTime","NOT_APPLICABLE").date()
        Elb_IPType = elbv2.get("IpAddressType","NOT_APPLICABLE")
        Elb_state = elbv2['State'].get("Code","NOT_APPLICABLE")
        Elbv2az_list = []
        for elbv2az in elbv2['AvailabilityZones']:
                elbv2azs = [elbv2az["ZoneName"],elbv2az["SubnetId"]]
                Elbv2az_list.append(elbv2azs)

        elbv2sg = []
        try:
            elbv2sg = elbv2['SecurityGroups']
        except:
            elbv2sg = "NOT_APPLICABLE"
            pass
        Elb_Sg = elbv2sg

        response_listners = elb_client.describe_listeners( LoadBalancerArn= Elb_ARN )

        for listner in response_listners['Listeners']:

            listner_ARN = listner.get("ListenerArn", "NOT_APPLICABLE")
            listner_port = listner.get("Port", "NOT_APPLICABLE")
            listner_proto = listner.get("Protocol", "NOT_APPLICABLE")

            response_listner_rules = elb_client.describe_rules( ListenerArn = listner_ARN )

            for rules in response_listner_rules['Rules']:

                rules_ARN = rules.get("RuleArn", "NOT_APPLICABLE")
                rules_PRI = rules.get("Priority", "NOT_APPLICABLE")
                rules_Con = rules.get("Conditions", "NOT_APPLICABLE")

                for rules_actions in rules['Actions']:
                    rules_action_type = rules_actions.get("Type", "NOT_APPLICABLE")
                    rules_targetgrp_arn = rules_actions.get("TargetGroupArn", "NOT_APPLICABLE")
                    try :
                        rules_targetgrp_name = rules_actions["TargetGroupArn"].split('/')[1]
                        response_targetgrp = elb_client.describe_target_groups( Names = [ rules_targetgrp_name ] )
                        for targetgroup in response_targetgrp['TargetGroups']:
                            targetgrp_proto = targetgroup['Protocol']
                            targetgrp_port = targetgroup['Port']
                            targetgrp_Vpcid = targetgroup['VpcId']
                            targetgrp_healthproto = targetgroup['HealthCheckProtocol']
                            targetgrp_healthport = targetgroup['HealthCheckPort']
                            targetgrp_healthenable = targetgroup['HealthCheckEnabled']
                            targetgrp_type = targetgroup['TargetType']

                        response_targetgrp_health = elb_client.describe_target_health( TargetGroupArn = rules_targetgrp_arn  )
                        rules_targetgrp_health = response_targetgrp_health['TargetHealthDescriptions']
                        #print(targetgrp_health)

                    except Exception as e:
                        targetgrp_name = "NOT_APPLICABLE"
                        targetgrp_proto = "NOT_APPLICABLE"
                        targetgrp_port = "NOT_APPLICABLE"
                        targetgrp_Vpcid = "NOT_APPLICABLE"
                        targetgrp_healthproto = "NOT_APPLICABLE"
                        targetgrp_healthport = "NOT_APPLICABLE"
                        targetgrp_healthenable = "NOT_APPLICABLE"
                        targetgrp_type = "NOT_APPLICABLE"
                        targetgrp_health = "NOT_APPLICABLE"
                        print(e)
                        #break
                    raw = [ Elb_ARN , Elb_Name , Elb_Type , Elb_Scheme , Elb_Dns , Elb_VPCID , Elb_LaunchTime ,
                          Elb_IPType , Elb_state , Elbv2az_list , Elb_Sg , listner_ARN , listner_port , listner_proto ,
                          rules_ARN , rules_PRI , rules_Con , rules_action_type , rules_targetgrp_arn ,
                          rules_targetgrp_name ,targetgrp_type ,  targetgrp_proto , targetgrp_port , targetgrp_Vpcid ,
                          targetgrp_healthproto , targetgrp_healthport , targetgrp_healthenable ,
                          rules_targetgrp_health ]

                    #print(raw)
                    writer.writerow(raw)

            #Elb_ARN = Elb_Name = Elb_Type = Elb_Scheme = Elb_Dns = Elb_VPCID = Elb_LaunchTime = "NULL"
            #Elb_IPType = Elb_state = Elbv2az_list = Elb_Sg = listner_ARN = listner_port = listner_proto = 'NULL'
                rules_ARN = rules_PRI = rules_Con = rules_action_type = rules_targetgrp_arn = 'NULL'
                rules_targetgrp_name  = targetgrp_type =  targetgrp_proto = targetgrp_port = targetgrp_Vpcid = 'NULL'
                targetgrp_healthproto = targetgrp_healthport = targetgrp_healthenable = 'NULL'
                rules_targetgrp_health = 'NULL'

            #print(Elb_ARN , Elb_Name , Elb_Type , Elb_Scheme , Elb_Dns , Elb_VPCID , Elb_LaunchTime ,
            #              Elb_IPType , Elb_state , Elbv2az_list , Elb_Sg , listner_ARN , listner_port , listner_proto ,
            #              rules_ARN , rules_PRI , rules_Con , rules_action_type , rules_targetgrp_arn ,
            #              rules_targetgrp_name ,targetgrp_type ,  targetgrp_proto , targetgrp_port , targetgrp_Vpcid ,
            #              targetgrp_healthproto , targetgrp_healthport , targetgrp_healthenable ,
            #              rules_targetgrp_health)

csvFile.close()
print("Completed")
