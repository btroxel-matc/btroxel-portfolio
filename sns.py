#!/usr/bin/env python3
#Author: Bryan Troxel
#Description: This simple script creates an sns topic to be sent out as an alert through email. It is meant to be used within another script in which it can be told where to send the email.
import boto3

def CreateSNSTopic(topicName):
    sns_client = boto3.client('sns')

    response = sns_client.create_topic(Name=topicName)
    return response['TopicArn']
                    
def SubscribeEmail(topicARN, emailAddress):
    sns_client = boto3.client('sns')
    response = sns_client.subscribe(TopicArn=topicARN, Protocol='email', Endpoint=emailAddress)
    return response['SubscriptionArn']
