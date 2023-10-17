#!/usr/bin/env python3

import boto3

def CreateSNSTopic(topicName):
    sns_client = boto3.client('sns')

    response = sns_client.create_topic(Name=topicName)
    return response['TopicArn']
                    
def SubscribeEmail(topicARN, emailAddress):
    sns_client = boto3.client('sns')
    response = sns_client.subscribe(TopicArn=topicARN, Protocol='email', Endpoint=emailAddress)
    return response['SubscriptionArn']