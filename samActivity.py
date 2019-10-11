# This activity requires Python 3.7 runtime
# -*- coding: utf-8 -*-
import json
def lambda_handler(event, context):
    
    method = event.get('httpMethod',{}) 
        
    indexPage="""
    <html>
    <head>
    <meta charset="utf-8">
    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.32.0/codemirror.min.css" />
  </head>
    <body>
         <h1>SAM Activity</h1>
        <div id="app">
            <md-tabs id="header">
                <md-tab v-for="question in questions" :key=question.name v-bind:md-label=question.name+question.status>
                    <doctest-activity v-bind:layout-things=question.layoutItems v-bind:question-name=question.name  @questionhandler="toggleQuestionStatus"/>
                </md-tab>
            </md-tabs>
            </div>
        </div>
    </body> 
    <script src="https://unpkg.com/vue"></script>
    <script src="https://unpkg.com/vue-material@beta"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.32.0/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/yaml/yaml.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue-codemirror@4.0.6/dist/vue-codemirror.min.js"></script>
    <script>
    Vue.use(VueMaterial.default)
    Vue.use(window.VueCodemirror)
    
    Vue.component('doctest-activity', {
        props: ['layoutThings', 'questionName'],
        data: function () {
            return {
            answer:{jsonFeedback:'',htmlFeedback:'',textFeedback:'',isComplete:false},
            layoutItems: this.layoutThings,
            cmOptions: {
              mode: 'yaml',
              lineNumbers: true
            },
            cmReadOnly: {
              lineNumbers: true,
              mode:  "python",
              readOnly: true
            }
        }
        },
        methods: {
            postContents: function () {
            // comment: leaving the gatewayUrl empty - API will post back to itself
            const gatewayUrl = '';
            this.$set(this, 'answer', {jsonFeedback:'',htmlFeedback:'',textFeedback:'',isComplete:false});
            fetch(gatewayUrl, {
        method: "POST",
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({shown:{0:this.layoutItems[0].vModel},editable:{0:this.layoutItems[1].vModel}})
        }).then(response => {
            return response.json()
        }).then(data => {
            this.answer = JSON.parse(JSON.stringify(data))
            this.answer.jsonFeedback = JSON.stringify(this.answer.jsonFeedback)
            return this.$emit('questionhandler',{data, questionName:this.questionName})
            })
         }
        },
        template: 
        `<div class="md-layout  md-gutter">
            <div id="cardGroupPreview" class="md-layout-item">
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
                                <md-tab :md-label="layoutItems[2].header">
                            <div class="md-subhead">{{layoutItems[2].subHeader}}</div>
                            <md-textarea v-model="layoutItems[2].vModel" readonly></md-textarea>
                </md-tab>            
            <md-tab  :md-label="layoutItems[0].header">
                            <div class="md-subhead">{{layoutItems[0].subHeader}}</div>
                             <codemirror class="editableTextarea" v-model="layoutItems[0].vModel" :options="cmReadOnly"></codemirror>
                </md-tab>
                <md-tab v-for="item in layoutItems.slice([3,])" :md-label="item.header">
                            <div class="md-subhead">{{item.subHeader}}</div>
                             <codemirror class="editableTextarea" v-model="item.vModel" :options="{lineNumbers: true,mode:item.mode,readOnly: true}"></codemirror>
                </md-tab>
                </md-tabs>
                        </md-field>
                    </md-card-content>
                </md-card>
                
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
            <div id="cardGroupCreator" class="md-layout-item">
                <md-card>
                    <md-card-header>
                        <md-card-header-text>
                            <div class="md-title">{{layoutItems[1].header}}</div>
                            <div class="md-subhead">{{layoutItems[1].subHeader}}</div>
                        </md-card-header-text>
                            <md-card-media>
                                <md-button class="md-raised md-primary" v-on:click="postContents">Submit</md-button>
                            </md-card-media>
                    </md-card-header>
                    <md-card-content>
                        <md-field>
                            <codemirror class="editableTextarea" v-model="layoutItems[1].vModel" :options="cmOptions"></codemirror>
                        </md-field>
                    </md-card-content>
                </md-card>
            </div>            
        </div>
        `
    })
    
    new Vue({
        el: '#app',
        data: function () {
            return {
            questions:[
                {name:"question 1", layoutItems: [
                {header:"Tests", subHeader:'', vModel:'GET, text=madam, response.type, shouldEqual, text/text\\nGET, text=banana, response.body, shouldContain, banana'},
                {header:"Editable Code Block", subHeader:'Your code goes below. Avoid double quotes.', vModel:'AWSTemplateFormatVersion: "2010-09-09"\\nTransform: AWS::Serverless-2016-10-31\\n\\nResources:\\n    LambdaFunc:\\n        Type: AWS::Serverless::Function\\n        Properties:\\n            CodeUri: hello_world/\\n            Handler: "app.lambda_handler"\\n            Runtime: "python2.7"\\n            Events: \\n                ExecuteFunc:\\n                    Type: Api\\n                    Properties:\\n                        Path: /\\n                        Method: any\\n    FunctionRole:\\n        Properties: \\n            AssumeRolePolicyDocument:\\n                Statement:\\n                - Action:\\n                    - sts: AssumeRole\\n                  Effect: Allow\\n                  Principal:\\n                    Service:\\n                        - lambda.amazonaws.com\\n            ManagedPolicyArns:\\n            - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole\\n            - arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess\\n            Path: /\\n            Type: AWS::IAM::Role'},
                {header:"Introduction", subHeader:'', vModel:"Map a route from API path x to function handler A"},
                {header:"app.py", mode:"python", subHeader:'', vModel:'import json\\nimport requests\\ndef lambda_handler(event, context):\\n    return {\\n        "statusCode": 200,\\n        "body": json.dumps(\\n            {"message": "hello world"}\\n        ),\\n    }'}
                ], status:" 🔴"}
            ]
        }
        },
         methods: {
            toggleQuestionStatus (response) {
                const {data, questionName} = response
                if (data.htmlFeedback) {
                    const searchText = data.htmlFeedback
                    searchText.search(/b2d8b2/) !== -1 ?
                        searchText.search(/#ff9999/) == -1 ?
                        this.questions.find(item => item.name === questionName).status = " ✔️"
                        :
                        this.questions.find(item => item.name === questionName).status = " 🤨"
                    :
                    this.questions.find(item => item.name === questionName).status = " 🔴"
                }
            }
        }
      })
    </script>
    <style lang="scss" scoped>
    h1{
        background-color:gainsboro
    }
    #header > .md-tabs-navigation {
        background-color:gainsboro;
    }
    .md-tabs-navigation .md-button{
         flex:1 100px
     }
    .md-card {
        width: 90%;
        margin: 20px;
        display: inline-block;
        vertical-align: top;
        min-height:200px
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
        flex-direction:column;
        padding: 0px;
        flex: 1 300px;
        min-width: 0
    }
    #cardGroupPreview .md-card {
        width: 90%;
    }
    #cardGroupPreview{
        padding: 0px;
        flex: 1 300px;
        min-width: 0
    }
    #cardGroupPreview .md-tab{
        height:100%
    }
    textarea {
        font-size: 1rem !important;
        min-height: 175px !important
    }
    .md-tabs{
        width:100%;
    }
    .md-tab{
        overflow-x: auto;
    }
    .md-tab::-webkit-scrollbar {
    width: 0px;
    }
    html {
        mix-blend-mode: darken
    }
    h1{
        padding:20px;
        margin:auto;
        text-align: center;
    }
    .md-content{
        min-height:300px
    }
    .md-tabs-container, .md-tabs-container .md-tab textarea, .md-tabs-content{
        height:100% !important
    }
    .md-field{
        margin:0px;
        padding:0px
    }
    .md-tabs-navigation{
        justify-content:center !important;
        flex-wrap:wrap
    }
    .md-card-media{
        width:400px !important
    }
    .md-button{
        margin:10px !important
    }
    .cm-s-default{
        height:100%
    }
    .md-card-header{
        padding:0 16px 16px 16px
    }
    </style>
    </html>
    """
    
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": indexPage
        }
        
    if method == 'POST':
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":True,
                "jsonFeedback": "hello",
                "htmlFeedback": "<h2>Hello</h2>",
                "textFeedback": "hello"
            })
            }