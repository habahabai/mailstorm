\# Mailstorm API Documentation



\## Overview



Mailstorm API is a service that provides email management functionality through a Tor hidden service. The API allows you to check access key usage, verify service health, and perform email subscription operations.



Base URL: http://ypwri6hshlwgxltrzorrcptslirxk7qkrvrzdi6i5fvrm36kkgw764yd.onion



Important Note: This API is only accessible through the Tor network. You must use a Tor browser or configure your application to route requests through the Tor proxy.



\## Authentication



The API uses access keys for authentication. Include your access key in the request body for relevant endpoints.

**To get an access key, join our Discord server: https://discord.gg/TNeDd7jsuh**



json

{

&nbsp; "access": "your\_access\_key\_here"

}





\## Endpoints



\### 1. Health Check



Check if the API service is running and healthy.



Endpoint: GET /health



Response:

\- 200 OK - Service is healthy

&nbsp; plaintext

&nbsp; true

&nbsp; 



Example Request:

bash

curl -X GET http://ypwri6hshlwgxltrzorrcptslirxk7qkrvrzdi6i5fvrm36kkgw764yd.onion/health





\### 2. Check Access Key Usage



Verify the usage statistics for your access key.



Endpoint: POST /access\_usage



Request Body:

json

{

&nbsp; "access": "your\_access\_key"

}





Responses:

\- 200 OK - Usage information returned

&nbsp; plaintext

&nbsp; Access key usage: 2/5 used

&nbsp; 

\- 400 Bad Request - Missing or invalid access key

&nbsp; plaintext

&nbsp; Missing required field: access

&nbsp; 

\- 500 Internal Server Error - Server error

&nbsp; plaintext

&nbsp; Server error

&nbsp; 



Example Request:

bash

curl -X POST http://ypwri6hshlwgxltrzorrcptslirxk7qkrvrzdi6i5fvrm36kkgw764yd.onion/access\_usage \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d '{"access": "your\_access\_key"}'





\### 3. Bomb Mail Operation



Subscribe an email address to mailing lists using the provided access key.



Endpoint: POST /bombmail



Request Body:

json

{

&nbsp; "first\_name": "John",

&nbsp; "last\_name": "Doe",

&nbsp; "email": "john.doe@example.com",

&nbsp; "access": "your\_access\_key"

}





Parameters:

\- first\_name (string, required): The target's first name

\- last\_name (string, required): The target's last name

\- email (string, required, email format): The target's email address

\- access (string, required): Your access key for authentication



Responses:

\- 200 OK - Operation completed successfully

&nbsp; plaintext

&nbsp; sent

&nbsp; 

\- 400 Bad Request - Missing fields, invalid email, or invalid access key

&nbsp; json

&nbsp; {

&nbsp;   "error": "Missing required fields: first\_name, last\_name, email, and access"

&nbsp; }

&nbsp; 

\- 500 Internal Server Error - Server error during processing

&nbsp; json

&nbsp; {

&nbsp;   "error": "An error occurred while processing the request."

&nbsp; }

&nbsp; 



Example Request:

bash

curl -X POST http://ypwri6hshlwgxltrzorrcptslirxk7qkrvrzdi6i5fvrm36kkgw764yd.onion/bombmail \\

&nbsp; -H "Content-Type: application/json" \\

&nbsp; -d '{

&nbsp;   "first\_name": "John",

&nbsp;   "last\_name": "Doe", 

&nbsp;   "email": "john.doe@example.com",

&nbsp;   "access": "your\_access\_key"

&nbsp; }'





\## Access Instructions



\### Using curl with Tor Proxy

bash

curl --socks5-hostname 127.0.0.1:9050 \\

&nbsp; -X GET http://ypwri6hshlwgxltrzorrcptslirxk7qkrvrzdi6i5fvrm36kkgw764yd.onion/health





\### Programmatic Access

Configure your HTTP client to use the Tor SOCKS proxy (default: 127.0.0.1:9050) when making requests to the .onion address.



\## Error Handling



All endpoints return appropriate HTTP status codes with descriptive error messages. Common errors include:



\- 400 Bad Request: Missing or invalid parameters

\- 500 Internal Server Error: Server-side issues

\- Connection errors: Usually indicate Tor connectivity problems



\## Rate Limiting



Usage is controlled through access keys, which have predefined usage limits. Check your remaining usage with the /access\_usage endpoint.



\## Security Notes



\- This service is only accessible via Tor

\- Keep your access keys secure and do not share them

\- The service does not require API key headers; include keys in request bodies

\- All communications are encrypted through Tor's onion routing



\## Support



For issues with the API, verify:

1\. You are connected to the Tor network

2\. Your access key is valid and has remaining usage

3\. All required parameters are provided in the correct format

4\. The service health check returns true









it will also return many errors like mail not sent, csrf error or link non existent, those errors are supposed to be ignored and you are required to retry the request, those errors will not count towards usage, only successful mail sent will be counted

