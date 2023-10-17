#!/usr/bin/env python3
import boto3, argparse, botocore

def main():
    parser = argparse.ArgumentParser(description='Audit security group configuration.')
    parser.add_argument('-s','--security-group',dest='sec_group', default='', type=str, help='Enter a specific security group.')
    args = parser.parse_args()
    sec_group = (args.sec_group)
    try:
        ec2client = boto3.client('ec2')
        if not sec_group:
            security_groups = ec2client.describe_security_groups()
        else:
            security_groups = ec2client.describe_security_groups(
                Filters=[
                    {
                        'Name': 'group-name',
                        'Values': [sec_group
                        ]
                    }
                ]
            )
        for security_group in security_groups['SecurityGroups']:
            for sec_rule in security_group['IpPermissions']:
                for rule in sec_rule.get('IpRanges',[]):
                    cidr = rule.get('CidrIp', '')
                    cidripv6 = rule.get('CidrIpv6', '')
                    from_port = rule.get('FromPort', '')
                    to_port = rule.get('ToPort', '')
                    for ipv4_rule in rule.get('IpRanges', []):
                        cidr = ipv4_rule.get('CidrIp', '')
                    for ipv6_rule in rule.get('Ipv6Ranges', []):
                        cidripv6 = ipv6_rule.get('CidrIpv6', '')
                    if cidr == '0.0.0.0/0' or cidripv6 =='::/0':
                        print(f"WARNING: Open to the public internet!")
                    else:
                        print(f"The following Security group has sufficient security policies.")
                    print(f"Security Group: {security_group['GroupName']}")
                    print(f"Cidr Ipv4 Ranges:{cidr}")
                    print(f"Cidr Ipv6 Ranges:{cidripv6}")
                    print(f"From Port:{from_port}")
                    print(f"To Port:{to_port}")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidGroup.NotFound':
            print("The security group requested does not exist.")
        elif error.response['Error']['Code'] == 'UnauthorizedOperation':
            print("You do not have the authorization to perform this action.")
        else:
            print("An error occurred.")

if __name__ == "__main__":
    main()