1. Upload [additional-layer/lambda_layer.zip](./additional-layer/lambda_layer.zip) in an Amazon S3 Bucket in the demo account
2. Select the uploaded file and click Copy URL 
2. Navigate the [Layer console](https://console.aws.amazon.com/lambda/home#/layers)
3. Click "Create layer"
   4. Name: additional-layer
   5. Upload a file from an Amazon S3: the S3 URL copied in the point 2
   6. Runtimes: Python 3.8 
7. Upload [bedrock-sdk/lambda_layer.zip](./additional-layer/lambda_layer.zip) in an Amazon S3 Bucket in the demo account
8. Select the uploaded file and click Copy URL 
9. Navigate the [Layer console](https://console.aws.amazon.com/lambda/home#/layers)
10. Click "Create layer"
   4. Name: bedrock-sdk
   5. Upload a file from an Amazon S3: the S3 URL copied in the point 8
   6. Runtimes: Python 3.8