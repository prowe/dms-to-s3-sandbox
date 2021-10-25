#!/bin/bash

set -e

export AWS_REGION=us-east-2

for logicalId in DataBucket QueryResultsBucket;
do
    echo "$logicalId"
    bucket_name=$(aws cloudformation describe-stack-resource \
        --stack-name=prowe-dms-sandbox \
        --logical-resource-id=$logicalId \
        --query='StackResourceDetail.PhysicalResourceId' --output=text)
    aws s3 rm "s3://$bucket_name" --recursive
done

aws cloudformation delete-stack --stack-name=prowe-dms-sandbox
aws cloudformation wait stack-delete-complete --stack-name=prowe-dms-sandbox