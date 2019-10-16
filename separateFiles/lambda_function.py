import json

def lambda_handler(event, context):

    # Python 3.7 runtime
    # This example demos AWS Lambda with a simple HTTP proxy
    # By default, the lambda function returns index.html with content-type in header set to text/html
    
    with open("index.html") as file:
        bodyContent = file.read()
    contentType = 'text/html'
    
    # In the case of style.css, change contentType to text/css and bodyContent to contents of style.css 
    
    path = event.get('path')
    if path == "/style.css":
        contentType = "text/css"
        with open("style.css") as file:
            bodyContent = file.read()

    # same for main.js as above

    if path == "/main.js":
        contentType = "text/javascript"
        with open("main.js") as file:
            bodyContent = file.read()

    return {
        'statusCode': 200,
         "headers": {
            'Content-Type': contentType,
            },
        'body': bodyContent
    }