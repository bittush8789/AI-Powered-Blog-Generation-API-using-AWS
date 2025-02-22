import boto3
import botocore.config
import json

from datetime import datetime

def blog_generate_using_bedrock(blogtopic: str) -> str:
    # Create a prompt for the blog generation based on the blog topic
    prompt = f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """

    # Define the body of the request with parameters for generation
    body = {
        "prompt": prompt,
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }

    try:
        # Create a Bedrock client for invoking the model
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        # Invoke the model with the request body and get the response
        response = bedrock.invoke_model(body=json.dumps(body), modelId="meta.llama2-13b-chat-v1")

        # Read and parse the response content
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        print(response_data)
        # Extract the generated blog details from the response
        blog_details = response_data['generation']
        return blog_details
    except Exception as e:
        # Handle any exceptions that occur during the blog generation
        print(f"Error generating the blog: {e}")
        return ""

def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    # Create an S3 client for saving the blog content
    s3 = boto3.client('s3')

    try:
        # Upload the generated blog content to the specified S3 bucket and key
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Code saved to s3")
    except Exception as e:
        # Handle any exceptions that occur during the saving to S3
        print("Error when saving the code to s3")

def lambda_handler(event, context):
    # Parse the event body to get the blog topic
    event = json.loads(event['body'])
    blogtopic = event['blog_topic']

    # Generate the blog content using Bedrock
    generate_blog = blog_generate_using_bedrock(blogtopic=blogtopic)

    if generate_blog:
        # Generate a unique S3 key based on the current time
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = 'aws_bedrock_course1'
        # Save the generated blog content to the specified S3 bucket
        save_blog_details_s3(s3_key, s3_bucket, generate_blog)
    else:
        print("No blog was generated")

    return {
        'statusCode': 200,
        'body': json.dumps('Blog Generation is completed')
    }
