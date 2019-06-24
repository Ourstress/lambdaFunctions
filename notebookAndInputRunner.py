import json
import base64
    
try:
    import requests
except ImportError:
    from botocore.vendored import requests
import os

def get_notebook_from_colab_url(url):
    docId = url.split("drive/")[1]
    url = "https://drive.google.com/uc?export=download&id=" + docId
    content = requests.get(url).json()
    return content

def lambda_handler(event, context):
    
    method = event.get('httpMethod',{}) 
    
    # process input notebook contents  
    notebookContents = ""
    
    indexPage="""
    <html>
    <head>
    <meta charset="utf-8">
    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
    <link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon"> 
  </head>
    <body>
         <h1>iPynb Runner</h1>
        <div id="app" class="md-layout  md-gutter">
            <div id="cardGroupCreator" class="md-layout-item md-size-50">
            <md-card>
                <md-card-header>
                    <md-card-header-text>
                        <div class="md-title">Input</div>
                        <div class="md-subhead">Enter colab url or upload Jupyter Notebook below</div>
                    </md-card-header-text>
                </md-card-header>
                <md-card-content>
                    <label for="notebook">Choose notebook to upload:</label>
                    <input type="file" id="notebook" accept=".ipynb,.py" @change="previewFiles" >
                    <md-field>
                        <md-input v-model="notebookSource" placeholder="colab url here"></md-input>
                     </md-field>
                </md-card-content>
            </md-card>
            <md-card>
                <md-card-header>
                    <md-card-header-text>
                        <div class="md-title">Enter input</div>
                        <div class="md-subhead">Input for your notebook</div>
                    </md-card-header-text>
                </md-card-header>
                <md-card-content>
                    <md-field>
                        <md-textarea v-model="input"></md-textarea>
                     </md-field>
                </md-card-content>
            </md-card>
                    <button v-on:click="staygo">Submit</button>
            </div>
            <div id="cardGroupPreview" class="md-layout-item md-size-50">
                <md-card>
                    <md-card-header>
                    <md-card-header-text>
                        <div class="md-title">Output</div>
                        <div class="md-subhead">Test results</div>
                    </md-card-header-text>
                </md-card-header>
                <md-card-content>
                    <md-field>
                        <md-tabs>
                            <md-tab id="tab-htmlResults" md-label="HTML results">
                                <div v-html="answer.htmlFeedback"></div>
                            </md-tab>
                            <md-tab id="tab-jsonResults" md-label="JSON results">
                                <md-textarea v-model="answer.jsonFeedback" readonly></md-textarea>
                            </md-tab>
                            <md-tab id="tab-textResults" md-label="Text results">
                                <md-textarea v-model="answer.textFeedback" readonly></md-textarea>
                            </md-tab>                            
                        </md-tabs>
                     </md-field>
                </md-card-content>
            </md-card>
            </div>
        </div>
    </body> 
    <script src="https://unpkg.com/vue"></script>
    <script src="https://unpkg.com/vue-material@beta"></script>
    <script>
    Vue.use(VueMaterial.default)

    new Vue({
        el: '#app',
        data() {
        return {
            notebookSource: "",
            input:"",
            answer:"",
            notebook:"",
            uploadedNotebookData: ""
            }
        },
        methods: {
            previewFiles: function(event) {
                let reader = new FileReader()
                reader.onload = e => { 
                this.uploadedNotebookData = JSON.parse(e.target.result)
                }
                this.notebook = event.target.files
                const file = this.notebook[0]
                reader.readAsText(file)
            },
            staygo: function () {
            // comment: leaving the gatewayUrl empty - API will post back to itself
                const gatewayUrl = '';
                fetch(gatewayUrl, {
                method: "POST",
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({uploadedNotebookData:this.uploadedNotebookData,notebookUrl:this.notebookSource,input:this.input})
                }).then(response => {
                return response.json()
                 }).then(data => {
                   this.answer = JSON.parse(JSON.stringify(data))
               })
         }
        }
      })
    </script>
    <style lang="scss" scoped>
    .md-card {
        width: 90%;
        margin: 20px;
        display: inline-block;
        vertical-align: top;
        min-height:300px
    }
    .md-card-content {
        padding-bottom: 16px !important;
    }
    button {
        display:block;
        margin: 20px 60px 20px 60px;
        width:200px !important;
    }
    #cardGroupCreator {
        display:flex;
        flex-direction:column
    }
    #cardGroupPreview .md-card {
        width: 500px;
    }
    textarea {
        font-size: 1rem !important;
    }
    .md-tabs{
        width:100%;
    }
    html {
        width:95%;
    }
    h1{
        padding:20px;
        margin:auto
    }
    .md-content{
        min-height:300px
    }
    .md-tabs-container .md-tab textarea{
        height:100%
    }
    </style>
    </html>
    """
    
    if method == 'GET':
        response = {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html'
            },
            "body": indexPage
        }
        return response
        
    if method == 'POST':
        response = ""
        bodyContent = event.get('body',{}) 
        parsedBodyContent = json.loads(bodyContent)
        try:
            notebookContents = parsedBodyContent["uploadedNotebookData"] or get_notebook_from_colab_url(parsedBodyContent['notebookUrl'])
            payload = json.loads(json.dumps({
                "notebook": notebookContents,
                "files": {"hello.txt":str(base64.b64encode(bytes(json.dumps(parsedBodyContent['input']), "utf-8")))[2: -1]}
            }))
            # post to jupyternotebook lambda function
            jupyterNbExecuter = os.environ['jupyterNbExecuter']
            modelResponse = requests.post(jupyterNbExecuter, json=payload)
            if(modelResponse.status_code == 200):
                if(modelResponse.json()["result"]):
                    results = modelResponse.json()["result"]
                    response = {
                        "statusCode": 200,
                        "headers": {
                            "Content-Type": "application/json",
                        },
                        "body":  json.dumps({
                            "isComplete":True,
                            "jsonFeedback": results,
                            "htmlFeedback": results,
                            "textFeedback": results                        
                        })
                    }
                    return response
            else:
                response = {
                    "statusCode": 500,
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "body":  json.dumps({
                        "results": "no results returned from notebook"
                    })
                }
                return response
        except Exception as ex:
           print(ex)
