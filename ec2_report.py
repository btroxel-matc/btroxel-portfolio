#!/usr/bin/env python3

import boto3,csv,argparse

def Get_Instances(name=None, values=None):
    parser = argparse.ArgumentParser(description="Enter a Filter and Value")
    parser.add_argument('-f', '--filter', metavar='[name]', dest='varfilter', type=str, required=True, help='Enter Filter Name')
    parser.add_argument('-v', '--value', metavar='[value]', dest='varvalue', type=str, required=True, help='Enter Filter Value')
    args = parser.parse_args()
    filtername = (args.varfilter)
    filtervalue = (args.varvalue)
    ec2_client = boto3.client('ec2')
    paginator = ec2_client.get_paginator('describe_instances')
    page_list = paginator.paginate(
        Filters=[
            {
                'Name': filtername,
                'Values': [
                    filtervalue,
                ]
            },
        ],
    )
    if name and values:
        filters.append({'Name': name, 'Values': values})
    response = []
    for page in page_list:
        for reservation in page['Reservations']:
            response.append(reservation)
    return response

def CSV_Writer(header, content):
    hFile = open('export.csv','w')
    writer = csv.DictWriter(hFile,fieldnames=header)
    writer.writeheader()
    for line in content:
        writer.writerow(line)
    hFile.close()

def main():

    response = Get_Instances()
    headerRow = ['InstanceId','InstanceType','State','PublicIpAddress','InstanceMonitorings']
    content = []
    for instance in response:
        for ec2 in instance['Instances']:
            content.append(
                {
                    "InstanceId": ec2['InstanceId'],
                    "InstanceType": ec2['InstanceType'],
                    "State": ec2['State']['Name'],
                    "PublicIpAddress": ec2.get('PublicIpAddress',"N/A"),
                    "InstanceMonitorings": ec2['State']['Name']
                }
            )
    CSV_Writer(headerRow,content)
    
if __name__ == "__main__":
    main()