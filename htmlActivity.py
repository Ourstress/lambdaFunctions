import json

import re

import signal
import time

    
def lambda_handler(event, context):
    
    method = event.get('httpMethod',{}) 
        
    indexPage="""
    <html>
    <head>
    <meta charset="utf-8">
    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
  </head>
    <body>
         <h1>HTML Custom Activity</h1>
        <div id="app" class="md-layout  md-gutter">
            <div id="cardGroupCreator" class="md-layout-item md-size-50">
            <md-card>
                <md-card-header>
                    <md-card-header-text>
                        <div class="md-title">Test case</div>
                        <div class="md-subhead">Enter HTML snippets below to test against the code in the HTML code block.</div>
                    </md-card-header-text>
                </md-card-header>
                <md-card-content>
                    <md-field>
                        <md-input v-for="item in testCases" v-model="item.value"></md-input>
                    </md-field>
                </md-card-content>
                <md-card-actions class="md-alignment-left">
                  <md-button class="md-raised" @click="addTestCase">add</md-button>
                </md-card-actions>
            </md-card>
            <md-card>
                <md-card-header>
                    <md-card-header-text>
                        <div class="md-title">Solution Code Block</div>
                        <div class="md-subhead">Enter the "model answer" below.</div>
                    </md-card-header-text>
                </md-card-header>
                <md-card-content>
                    <md-field>
                        <md-textarea v-model="hidden"></md-textarea>
                     </md-field>
                </md-card-content>
            </md-card>
            <md-card>
                <md-card-header>
                    <md-card-header-text>
                        <div class="md-title">HTML Code Block</div>
                        <div class="md-subhead">Enter your HTML code below</div>
                    </md-card-header-text>
                </md-card-header>
                <md-card-content>
                    <md-field>
                        <md-textarea v-model="solution"></md-textarea>
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
        data: {
            testCases: [{
            value: '<p>Hello World</p>'
            }],
            solution:"<!--https://www.w3schools.com/code/tryit.asp?filename=G3TUA7U40NG9--><h3>Add a third list item with the text 'Three'.</h3><input><button>Click me</button><ul><li>One</li><li>Two</li><ul>",
            answer:"",
            hidden: "<h3>Add a third list item with the text 'Three'.</h3><input><button>Click me</button><ul><li>One</li><li>Two</li><ul>"
        },
        methods: {
            staygo: function () {
            // comment: leaving the gatewayUrl empty - API will post back to itself
            const gatewayUrl = '';
            fetch(gatewayUrl, {
        method: "POST",
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({shown:{0:this.testCases},editable:{0:this.solution}, hidden:{0:this.hidden}})
        }).then(response => {
            return response.json()
        }).then(data => {
            this.answer = JSON.parse(JSON.stringify(data))
            })
         },
         addTestCase() {
      this.testCases.push({
        value: ''
      });
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
        min-height:300px;
        height: 100% !important
    }
    .md-tabs-container .md-tab textarea{
        height:100%
    }
    .md-field{
        flex-direction:column;
    }
    .md-field.md-theme-default:after{
        background-color:transparent !important;
    }
    .md-field.md-theme-default:before{
        background-color:transparent !important;
    }    
    input{
        margin-bottom:1rem;
        width:100%;
        height:1.5rem;
        font-size: 1rem !important;
        border-bottom: 1px dotted black !important;
    }
    .md-button{
        margin-bottom:0.5rem;
    }
    #tab-textResults{
        height:300px;
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
        bodyContent = event.get('body',{}) 
        parsedBodyContent = json.loads(bodyContent)
        testCases = parsedBodyContent["shown"]["0"] 
        solution = parsedBodyContent["editable"]["0"] 
        hidden = "\n" + parsedBodyContent["hidden"]["0"]
        
        # sanitise HTML input
        import bleach
        otherTags = ['h1','h2','h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
        'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
        'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td','p', 'span', 'button' ,'input']
        attrs = {
            '*': ['class'],
            'a': ['href', 'rel'],
            'img': ['alt'],
        }
        # for item in testCases:
        #     item["value"] = bleach.clean(item["value"], tags = bleach.sanitizer.ALLOWED_TAGS+otherTags, attributes=attrs)
        # solution = bleach.clean(solution, tags = bleach.sanitizer.ALLOWED_TAGS+otherTags, attributes=attrs)
        # hidden = bleach.clean(hidden, tags = bleach.sanitizer.ALLOWED_TAGS+otherTags, attributes=attrs)

        import re
        
        
        # Setup variables for printing results on the UI
        tableContents = ""
        textBackgroundColor = "#ffffff"
        expectedText = ""
        receivedText = ""
        textResults = ""
        overallResults = "All tests passed: True"
        
        timeout = False
        # handler function that tell the signal module to execute
        # our own function when SIGALRM signal received.
        def timeout_handler(num, stack):
            print("Received SIGALRM")
            raise Exception("processTooLong")

        # register this with the SIGALRM signal    
        signal.signal(signal.SIGALRM, timeout_handler)
        
        # signal.alarm(10) tells the OS to send a SIGALRM after 10 seconds from this point onwards.
        signal.alarm(10)

        # After setting the alarm clock we invoke the long running function.
        try:
            for item in testCases:
                regexMatchHtmlContents = re.search(item["value"], solution)
                if hasattr(regexMatchHtmlContents, 'group'):
                    # escape < tag and > tag so it shows up in td cell
                    expectedText = item["value"].replace("<","&lt;")
                    expectedText = expectedText.replace(">","&gt;")
                    
                    receivedText = "True"
                    if item["value"] == regexMatchHtmlContents.group(0):
                        textResults = textResults + "\nHurray! You have passed the test case. You expected {0} and the provided HTML code contains it.\n".format(item["value"])
                        textBackgroundColor = "#b2d8b2"
                else:
                    expectedText = item["value"].replace("<","&lt;")
                    expectedText = expectedText.replace(">","&gt;")
                    textResults = textResults + "\nThe test case eludes your code so far but try again! Did not receive {0} as expected.\n".format(item["value"])
                    textBackgroundColor = "#ff9999"
                    receivedText = "False"                    
                    overallResults = "All tests passed: False"
                tableContents = tableContents + """
                    <tr bgcolor={2}>
                        <td>{0}</td>
                        <td>{1}</td>
                    </tr>
                    """.format(expectedText,receivedText,textBackgroundColor)
        except Exception as ex:
            if "processTooLong" in ex:
                timeout = True
                print("processTooLong triggered")
        # set the alarm to 0 seconds after all is done
        finally:
            signal.alarm(0)
        
        htmlResults="""
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
                </head>
                <body>
                    <div>
                        <p class="class="md-subheading">{0}</p>
                        <br/>
                        <p class="md-subheading tableTitle">Test cases</p>
                        <table>
                            <thead>
                                <tr>
                                    <th style="width:75%">Expected</th>
                                    <th style="width:25%">Received</th>
                                </tr>
                            </thead>
                            <tbody>
                                {1}
                            </tbody>
                        </table>
                    </div>
                </body>         
                <style>
                br {{
                    display:block;
                    content:"";
                    margin:1rem
                }}
                table{{
                    text-align:center
                }}
                .tableTitle{{
                    text-decoration:underline
                }}
                </style>
                    </div>
                    <br/>
                    <p class="md-subheading">
                        HTML code expected:
                    </p>
                    <div>
                        {2}
                    </div> 
                     <br/>
                    <p class="md-subheading">
                        HTML code provided:
                    </p>
                    <div>
                        {3}
                    </div>
                </body>
                <style>
                br {{
                    display:block;
                    content:"";
                    margin:1rem
                }}
                table{{
                    text-align:center
                }}
                .tableTitle{{
                    text-decoration:underline
                }}
                .md-subheading{{
                    text-decoration:underline
                }}
                </style>
            </html>
            """.format(overallResults, tableContents, hidden, solution)
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":True,
                "jsonFeedback": json.dumps(overallResults),
                "htmlFeedback": htmlResults,
                "textFeedback": overallResults + "\n" + textResults
            })
            }
