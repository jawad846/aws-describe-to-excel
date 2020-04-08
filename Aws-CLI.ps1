

aws ec2 describe-instances --profile mafro --output text --query 'Reservations[*].Instances[*].[InstanceId, InstanceType, ImageId, State.Name, LaunchTime, Placement.AvailabilityZone, Placement.Tenancy, PrivateIpAddress, PrivateDnsName, PublicDnsName, [Tags[?Key==`Name`].Value] [0][0], [Tags[?Key==`purpose`].Value] [0][0], [Tags[?Key==`environment`].Value] [0][0], [Tags[?Key==`team`].Value] [0][0] ]' > instances.csv




aws ec2 describe-volumes --profile adfaws --output text --query 'Volumes[*].Attachments[].{VolumeID:VolumeId,InstanceID:InstanceId}'



aws ec2 describe-volumes --profile mafro  --output text --query 'Volumes[*].{ID:VolumeId,InstanceId:Attachments[0].InstanceId,AZ:AvailabilityZone,Size:Size}' > instancesebs.csv






