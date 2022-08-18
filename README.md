# lambda_async
An example of asynchronous call of lambda. 
Resource configured with AWS CDK

## Architecture

### Lambdas function: 
1. `main_handler` - Main process function working in synchronous/asynchronous manner.
2. `function_on_success` - Triggered by `main_handler` on success. It stores response from main function in S3 bucket.
3. `polling_handler` - Polling function which fetch status of the job from S3 bucket.

### API Gateway
API GW is integrated with two above lambdas: `main_handler` and `polling_handler`.

HTTP Methods: 
- **POST** associated with `main_handler`
- **GET** associated with `polling_handler`

## Usage

1. Call main process function in asynchronous manner by adding header `InvocationType: Event`: 
`curl -i -XPOST "<api_gateway_url>" -H "InvocationType:Event"`
2. Call the same endpoint with method **GET** to check the status of the job running: `curl -i -XGET "<api_gateway_url>"`

Job once will show message *Job is finished*.