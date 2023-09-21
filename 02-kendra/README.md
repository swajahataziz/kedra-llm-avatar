## Kendra Index

1. Navigate the [Kendra console](https://console.aws.amazon.com/kendra/home#)
2. Click "Create index"
   3. Name: stellantis-index
   4. IAM Role: Create a new Role
   5. Provisioning editions: Developer edition

## Data Sources

### IAM Role

1. Navigate the [IAM console](https://console.aws.amazon.com/iamv2)
2. Click "Roles" in the left menu 
3. Search the Kendra Role 
4. Click "Add permissions"
   5. Search for AmazonS3FullAccess
   6. Search for AmazonKendraFullAccess

### S3 documents

1. Upload the cleaned documents in an Amazon S3 bucket

1. Navigate the [Kendra console](https://console.aws.amazon.com/kendra/home#)
2. Select the created index 
3. Click "Data sources" in the left menu
4. Click "Add data source"
   5. Search S3
   6. Click Amazon S3 connector -> Add connector
   7. IAM Role: The created Kendra Role
   8. Bucket: The S3 bucket where the documents are stored
   9. Metadata files prefix folder: The S3 prefix where your document are stored
   10. Sync run schedule: Run on demand