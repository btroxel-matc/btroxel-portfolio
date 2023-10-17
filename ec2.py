#!/usr/bin/env python3
import boto3,json,argparse,random,string,botocore
parser = argparse.ArgumentParser(description='Week 6 ec2 Script.')
parser.add_argument('-n','--instancename',dest='tag_name', default='', type=str, help='Enter a tag name for your instance.')
parser.add_argument('-p','--keypair',dest='key_pair', default='', type=str, help='Enter the name of an existing Key Pair.')
args = parser.parse_args()
tag_name = args.tag_name
key_pair = args.key_pair

#Automatically creates a new Instance Tag Name.
if not tag_name:
    print(f"No name was provided for the EC2 instance. Generating a name...")
    tag_name = "Instance-" + "".join(random.choices(string.ascii_lowercase, k=8))
    print(f"Starting up instance: {tag_name}.")
else:
    print(f"Starting up instance: {tag_name}.")

def Get_Image(ec2client):
    image_response = ec2client.describe_images(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Amazon Linux 2 AMI*']
            },
            {
                'Name': 'architecture',
                'Values': ['x86_64']
            },
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            },
        ]
    )
    return image_response['Images'][0]['ImageId']

def Create_EC2(AMI, ec2client):

    DRYRUN = False

    response = ec2client.run_instances(
        ImageId=AMI,
        InstanceType='t2.micro',
        KeyName=key_pair,
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN,
        UserData='''

        #!/bin/bash -ex

        # Updated to use Amazon Linux 2

        yum -y update

        yum -y install httpd php mysql php-mysql

        /usr/bin/systemctl enable httpd

        /usr/bin/systemctl start httpd

        cd /var/www/html

        wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-100-ACCLFO-2/lab6-scaling/lab-app.zip

        unzip lab-app.zip -d /var/www/html/

        chown apache:root /var/www/html/rds.conf.php

        '''
    )   

    return response['Instances'][0]['InstanceId']

def main():
    try:
        client = boto3.client('ec2')
        AMI = Get_Image(client)
        
        Instance_Id = Create_EC2(AMI, client)
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(Instance_Id,)

        print(f"Current Status: Instance is {instance.state['Name']}")
        instance.wait_until_running()
        instance.reload()
        print(f"Status Update: Instance is {instance.state['Name']}")
        print(f"Public Ip Address of Instance is: {instance.public_ip_address}")
        instance.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': tag_name
                }
            ]
        )
        for tag in instance.tags:
            if tag ['Key'] == 'Name':
                print(f"Instance Name: {tag['Value']}")
    except botocore.exceptions.ClientError as error:
            #The region is not configured to the request.
        if error.response['Error']['Code'] == 'UnauthorizedOperation':
            print("Your region configuration is invalid for this request.")
            #Key Pair not found.
        elif error.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
            print(f"The key pair requested does not exist.")
        else:
            print(f'An error occured {error}.')

if __name__ == "__main__":
   main()