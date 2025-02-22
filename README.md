# AI-Powered Blog Generation using AWS Bedrock

## Overview

This project implements an **AI-powered blog generation API** using **AWS Lambda, Amazon Bedrock, and Amazon S3**. The Lambda function generates blog content based on a given topic using **Meta's LLaMA 2 model** via Amazon Bedrock and stores the generated blog in an **Amazon S3 bucket**.

## Architecture

1. The API receives a request containing a blog topic.
2. The AWS Lambda function processes the request and interacts with **Amazon Bedrock** to generate AI-based content.
3. The generated blog is saved in **Amazon S3** for storage and retrieval.
4. The API responds with a success message once the blog is stored.

## Prerequisites

To run this project, you need:

- **AWS Account** with access to **Amazon Bedrock, Lambda, API Gateway, and S3**.
- **Python 3.x** installed.
- **Boto3 SDK** for AWS services.
- **IAM Permissions** for accessing Bedrock and S3.

## Setup & Deployment

### 1. Install Dependencies

Ensure you have the AWS SDK installed:

```sh
pip install boto3 botocore
```

### 2. Configure AWS Credentials

Set up your AWS CLI credentials:

```sh
aws configure
```

### 3. Deploying the Lambda Function

1. Create an **AWS Lambda** function in the **us-east-1** region.
2. Upload the provided `lambda_handler` Python script.
3. Attach necessary IAM roles for accessing Bedrock and S3.

### 4. API Gateway Setup

- Configure **Amazon API Gateway** to trigger the Lambda function upon receiving requests.
- Deploy the API and obtain the endpoint URL.

## Usage

Send a POST request using **Postman** or **cURL**:

```sh
curl -X POST https://your-api-gateway-url \
     -H "Content-Type: application/json" \
     -d '{"blog_topic": "Artificial Intelligence in 2025"}'
```

## Code Breakdown

### **blog\_generate\_using\_bedrock(blogtopic: str) -> str**

- Constructs a prompt for blog generation.
- Calls **Amazon Bedrock** to generate content using LLaMA 2.
- Returns the generated blog text.

### **save\_blog\_details\_s3(s3\_key, s3\_bucket, generate\_blog)**

- Saves the generated blog in an **S3 bucket** under a timestamped filename.

### **lambda\_handler(event, context)**

- Handles incoming API requests.
- Calls `blog_generate_using_bedrock()` to generate content.
- Saves the output in S3 and returns a success response.

## Error Handling

- Exception handling for **Bedrock API failures** and **S3 upload errors**.
- Logs errors and provides a default response in case of failures.

## Future Enhancements

- Add support for **different AI models** in Bedrock.
- Implement **database storage** for structured blog management.
- Enhance **API response format** with metadata.
