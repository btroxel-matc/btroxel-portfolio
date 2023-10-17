#!/usr/bin/env python3
#Author: Bryan Troxel
#Description: This script will bring back all roles and the policies that belong to them. This includes both managed and unmanaged policies.
import boto3
import botocore
import datetime

def main():
    try:
        iamclient = boto3.client('iam')

        role_list = iamclient.list_roles()
        for role in role_list['Roles']:    
            rolename = role['RoleName']
            rolecreation = role['CreateDate']
            unmanaged_resp = iamclient.list_role_policies(RoleName=rolename)
            managed_resp = iamclient.list_attached_role_policies(RoleName=rolename)
            print(f"Role: {rolename} -- Created:{rolecreation}")
            if 'PolicyNames' in unmanaged_resp:
                for policyname in unmanaged_resp['PolicyNames']:
                    print(f"...has unmanaged policy name:{policy['PolicyName']}")
            if 'AttachedPolicies' in managed_resp:
                for policy in managed_resp['AttachedPolicies']:
                    m_policy = policy['PolicyName']
                    print(f"...has managed policy name: {m_policy}")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            print("You are not authorized to perform this task on this resource.")
        else:
            print('An error occurred.')

if __name__ == "__main__":
    main()
