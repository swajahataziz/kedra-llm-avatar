1. Navigate the [Function console](https://console.aws.amazon.com/lambda/home#/functions)
2. Click "Create function"
   3. Function name: DigitalAssistantLambda
   4. Runtime: Python 3.8
   5. Execution Role: LambdaBedrockRole (follow the instructions in the [README](../01-iam/README.md))
6. Select the created function `DigitalAssistantLambda`
   7. Select Code 
   8. Copy and paste the content of [lambda_function.py](./DigitalAssistantLambda/lambda_function.py)
   9. Paste the URL copied in the point 2 
10. Select the created function `DigitalAssistantLambda`
11. Click "Add layer"
    12. Custom Layer 
    13. Select additional-layer (follow the instructions in the [README](../03-lambda_layer/README.md))
    14. Select the latest version 
15. Click "Add layer"
    16. Custom Layer 
    17. Select bedrock-sdk (follow the instructions in the [README](../03-lambda_layer/README.md))
    18. Select the latest version 
19. Click "Configurations"
    20. In "General configuration" click "Edit"
    21. Set Lambda timeout to 15 min