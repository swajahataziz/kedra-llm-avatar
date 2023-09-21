1. Navigate the [Lex console](https://console.aws.amazon.com/lexv2/home#)
2. Select "Bots" in the left menu
3. Click "Action" -> Import
   4. Name: AmariBot
   5. Input file: [AmariBot-DRAFT-O1G7VNR3NV-LexJson.zip](./AmariBot-DRAFT-O1G7VNR3NV-LexJson.zip)
   5. IAM permission: Use an existing role -> AWSServiceRoleForLexV2Bots_Bedrock (follow the instructions in the [README](../01-iam/README.md))
6. Select the created bot
   7. In the left menu, select English (US) under "All languages"
   8. Click Build