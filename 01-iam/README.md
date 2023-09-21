## IAM Role - Lex

1. Navigate the [IAM console](https://console.aws.amazon.com/iamv2)
2. Click "Roles" in the left menu
3. Click "Create role"
   4. Trusted entity type: AWS service
   5. Use case: 
      6. Lex
      7. Lex V2 - Bots
   8. Name: Bedrock

## IAM Role - Lambda

1. Navigate the [IAM console](https://console.aws.amazon.com/iamv2)
2. Click "Roles" in the left menu
3. Click "Create role"
   4. Trusted entity type: AWS service
   5. Use case: 
      6. Lambda
   8. Select the following managed policies:
      9. AmazonKendraFullAccess
      10. AmazonSageMakerFullAccess
      10. AmazonS3FullAccess
      11. ComprehendFullAccess
      11. CloudWatchFullAccess
      12. CloudWatchLogsFullAccess
   13. Name: LambdaBedrockRole
14. In the created role, click "Add permissions" -> create inline policy
    15. JSON
    16. Copy and paste the content from [bedrock-policy.json](./LambdaBedrockRole/bedrock-policy.json)
    17. Name: bedrock-policy
18. In the created role, click "Trust relationship"
19. Click "Edit trust policy"
    20. Copy and paste the content from [trusted-relationship.json](./LambdaBedrockRole/trusted-relationship.json)