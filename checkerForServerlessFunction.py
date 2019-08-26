try:
    import requests
except ImportError:
    from botocore.vendored import requests
import json

def getIndexPage():
    indexPage="""
    <html>
    <head>
    <meta charset="utf-8">
    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
  </head>
    <body>
         <h1>Checker for Serverless Functions</h1>
        <div id="app">
            <md-tabs>
                <md-tab v-for="question in questions" :key=question.name v-bind:md-label=question.name+question.status>
                    <doctest-activity v-bind:layout-things=question.layoutItems v-bind:question-name=question.name  @questionhandler="toggleQuestionStatus"/>
                </md-tab>
            </md-tabs>
            </div>
        </div>
    </body> 
    <script src="https://unpkg.com/vue"></script>
    <script src="https://unpkg.com/vue-material@beta"></script>
    <script>
    Vue.use(VueMaterial.default)
    
    Vue.component('doctest-activity', {
        props: ['layoutThings', 'questionName'],
        data: function () {
            return {
            answer:"",
            layoutItems: this.layoutThings
        }
        },
        methods: {
            postContents: function () {
            // comment: leaving the gatewayUrl empty - API will post back to itself
            const gatewayUrl = '';
            fetch(gatewayUrl, {
        method: "POST",
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({userToken:"ABCDE",shown:{0:this.layoutItems[0].vModel},editable:{0:this.layoutItems[1].vModel}})
        }).then(response => {
            return response.json()
        }).then(data => {
            this.answer = JSON.parse(JSON.stringify(data))
            return this.$emit('questionhandler',{data, questionName:this.questionName})
            })
         }
        },
        template: 
        `<div class="md-layout  md-gutter">
            <div id="cardGroupCreator" class="md-layout-item md-size-50">
                <md-card>
                    <md-card-header>
                        <md-card-header-text>
                            <div class="md-title">{{layoutItems[0].header}}</div>
                            <div class="md-subhead">{{layoutItems[0].subHeader}}</div>
                        </md-card-header-text>
                    </md-card-header>
                    <md-card-content>
                        <md-field>
                            <md-textarea v-model="layoutItems[0].vModel" readonly></md-textarea>
                        </md-field>
                    </md-card-content>
                </md-card>
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
                            <md-textarea v-model="layoutItems[1].vModel"></md-textarea>
                        </md-field>
                    </md-card-content>
                </md-card>
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
        `
    })
    
    new Vue({
        el: '#app',
        data: function () {
            return {
            questions:[
                {name:"question 1", layoutItems: [
                {header:"Tests", subHeader:'Key in the following below: HTTP method, parameters(if any), responseTarget (eg. response.type, response.body), testMethod (shouldContain or shouldEqual), testValue', vModel:"GET,, response.type, shouldEqual, text/html\\nGET, text=banana, response.body, shouldContain, banana"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"https://us-south.functions.cloud.ibm.com/api/v1/web/fddc9646-3687-4c6e-a36c-96754d415126/default/dragon"}
                ], status:" 🔴"},
                {name:"question 2", layoutItems: [
                {header:"Tests", subHeader:'Key in the following below: HTTP method, parameters(if any), responseTarget (eg. response.type, response.body), testMethod (shouldContain or shouldEqual), testValue', vModel:"POST,, response.type, shouldEqual, application/json\\nPOST,, response.body, shouldContain, banana"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"https://us-south.functions.cloud.ibm.com/api/v1/web/fddc9646-3687-4c6e-a36c-96754d415126/default/dragon"}
                ], status:" 🔴"},
                {name:"question 3", layoutItems: [
                {header:"Tests", subHeader:'Key in the following below: HTTP method, parameters(if any), responseTarget (eg. response.type, response.body), testMethod (shouldContain or shouldEqual), testValue', vModel:"POST, name=boohoo, response.type, shouldEqual, application/json\\nPOST, name=boohoo, response.body, shouldContain, boohoo"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"https://us-south.functions.cloud.ibm.com/api/v1/web/fddc9646-3687-4c6e-a36c-96754d415126/default/dragon"}
                ], status:" 🔴"},
                {name:"question 4", layoutItems: [
                {header:"Tests", subHeader:'Key in the following below: HTTP method, parameters(if any), responseTarget (eg. response.type, response.body), testMethod (shouldContain or shouldEqual), testValue', vModel:"GET,name=alset, response.type, shouldEqual, text/html\\nGET, name=alset, response.body, shouldContain, alset"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"https://us-south.functions.cloud.ibm.com/api/v1/web/fddc9646-3687-4c6e-a36c-96754d415126/default/dragon"}
                ], status:" 🔴"},
                {name:"question 5", layoutItems: [
                {header:"Tests", subHeader:'Key in the following below: HTTP method, parameters(if any), responseTarget (eg. response.type, response.body), testMethod (shouldContain or shouldEqual), testValue', vModel:"POST, name=alset, response.type, shouldEqual, application/json\\nPOST, organisation=alset, response.body, shouldContain, alset"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"https://us-south.functions.cloud.ibm.com/api/v1/web/fddc9646-3687-4c6e-a36c-96754d415126/default/dragon"}
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
        padding-right: 0px
    }
    #cardGroupPreview .md-card {
        width: 90%;
    }
    #cardGroupPreview{
        padding-left: 0px
    }
    #cardGroupPreview .md-tab{
        height:100%
    }
    textarea {
        font-size: 1rem !important;
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
        width:95%;
        margin:auto;
        mix-blend-mode: darken
    }
    h1{
        padding:20px;
        margin:auto;
        text-align: center
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
        justify-content:center !important
    }
    .md-card-media{
        width:400px !important
    }
    .md-button{
        margin:10px !important
    }
    </style>
    </html>
    """
    return indexPage

def exec_tests(testUrl,test,userToken):
    jsonResponse = {"results": []}
    for oneTest in test:
        partsOfTest = oneTest.split(",")
        partsOfTest = list(map(str.strip, partsOfTest))
        if(partsOfTest[0].lower() == "url"):
            # -------------------------------------#
            # [0]     [1]         [2]
            # method, testMethod, testValue
            # URL, shouldContain, abc
            # -------------------------------------#
            if(partsOfTest[1].lower() == "shouldcontain" and testUrl):
                opStr = "\"{received}\".find('{testValue}') != -1".format(
                            received = testUrl,
                            testValue = partsOfTest[2])
            else:
                opStr = "False"
        else: 
            execUrlStr = """requests.{method}(url="{url}?{parameter}")""".format(
            method = partsOfTest[0].lower(),
            url = testUrl,
            parameter = partsOfTest[1])
            urlResponse = eval(execUrlStr)
            resStatusCode = urlResponse.status_code  
            # -------------------------------------#
            # [0]     [1]         [2]             [3]         [4]
            # method, parameters, responseTarget, testMethod, testValue
            # GET, name=abc, response.type, shouldEqual, text/text
            # GET, text=banana, response.json.anotherResult, shouldEqual, Hey there
            # Define responseTarget
            # -------------------------------------#
            if(partsOfTest[2].lower() == "response.type"):
                targetStr = "headers['Content-Type']"
            elif(partsOfTest[2].lower() == "response.body"):
                targetStr = "text"
            elif(partsOfTest[2] and partsOfTest[2].lower().find("response.json") !=1 ):
                targetStr = "json()"
            else: # Default target text
                targetStr = "text"
            execReq = str(eval("urlResponse."+targetStr))
            # format json correctly, replace ' with " and " with \\"
            finalRes = execReq.replace("'",'"').replace('"', '\\"')
            # -------------------------------------#
            # For json() target
            # -------------------------------------#
            if(targetStr == "json()" and resStatusCode == 200):
                keys = ""
                # response.json.key1.key2 -> get all the keys
                for key in partsOfTest[2].split(".")[2:]:
                    keys +="[\"{key}\"]".format(key=key)
                temp = "json.loads(\"{received}\"){keys}".format(
                            received = finalRes, 
                            keys = keys)
                finalRes = eval(temp)
            # -------------------------------------#
            # Define testMethod/operation
            # -------------------------------------#
            if execReq:
                if(partsOfTest[3].lower() == "shouldequal"):
                    opStr = "\"{testvalue}\" in \"{received}\"".format(
                            received = finalRes, 
                            testvalue = partsOfTest[4])
                elif(partsOfTest[3].lower() == "shouldcontain"):
                    if(partsOfTest[4] == "YOUR_USER_TOKEN" and finalRes):
                        opStr = "\"{received}\".find('{testValue}') != -1".format(
                            received = finalRes,
                            testValue = userToken)
                    else:
                        opStr = "\"{testValue}\" in \"\"\"{received}\"\"\"".format(
                            received = finalRes,
                            testValue = partsOfTest[4])
                else:
                    opStr = "False"
            else:
                opStr = "False"
        execOpStr = """{operation}""".format(operation=opStr)
        execOp = str(eval(execOpStr))
        result = {}
        if(partsOfTest[0].lower() == "url"):
            result = {"method": partsOfTest[0], 
                "parameters": "--", 
                "responseTarget": "--",
                "testMethod": partsOfTest[1], 
                "testValue": partsOfTest[2], 
                "receivedValue": "--", 
                "statusCode":"--", 
                "correct": execOp}
        else:
            result = {"method": partsOfTest[0], 
                    "parameters": partsOfTest[1], 
                    "responseTarget": partsOfTest[2],
                    "testMethod": partsOfTest[3], 
                    "testValue": partsOfTest[4], 
                    "receivedValue": execReq, 
                    "statusCode":resStatusCode, 
                    "correct": execOp}
        jsonResponse["results"].append(result)
    return jsonResponse

def calcFeedback(jsonResponse,userToken):
    jsonResponseData = json.loads(json.dumps(jsonResponse))
    resultContent = jsonResponseData.get('results')
    textResults = ""
    tableContents = ""
    textBackgroundColor = "#ffffff"
    allTestCaseResult = True
    if resultContent:
        for i in range(len(resultContent)):
            methodText = resultContent[i]["method"]
            parameterText = resultContent[i]["parameters"]
            responseTargetText = resultContent[i]["responseTarget"]
            testMethodText = resultContent[i]["testMethod"]
            # test value YOUR_USER_TOKEN = ABCD or testvalue
            testValueText = "YOUR_USER_TOKEN = " + userToken if (resultContent[i]["testValue"] == "YOUR_USER_TOKEN") else resultContent[i]["testValue"]
            receivedValueText = resultContent[i]["receivedValue"]
            statusCode = resultContent[i]["statusCode"]
            correctText = resultContent[i]["correct"]
            # Collective Pass or Fail
            allTestCaseResult = (allTestCaseResult and (correctText == "True"))
            textResults += ("\n Public Test - ")
            if correctText == "True":
                textResults += ("Passed.\n")
                textBackgroundColor = "#b2d8b2" #Green
            else:
                textResults += ("Failed.\n") 
                textBackgroundColor = "#ff9999" #Red
            textResults += ("INFO: Status code {statusCode}. {method} call with "
                            "{parameter} and received {responseTarget} as " 
                            "{receivedValue} against the expected value " 
                            "of {testValue}.\n").format(
                                statusCode=statusCode,
                                method=methodText, 
                                parameter=parameterText, 
                                responseTarget=responseTargetText, 
                                receivedValue=receivedValueText,
                                testValue=testValueText)
            tableContents = tableContents + """
            <tr bgcolor={color}>
                <td>{method}</td>
                <td>{parameter}</td>
                <td>{responseTarget}</td>
                <td>{testMethod}</td>
                <td>{testValue}</td>
                <td>{receivedValue}</td>
                <td>{statusCode}</td>
                <td>{correct}</td>
            </tr>
            """.format(method=methodText, parameter=parameterText, 
                    responseTarget=responseTargetText, testMethod=testMethodText, 
                    testValue=testValueText, receivedValue=receivedValueText, 
                    statusCode=statusCode, correct=correctText, 
                    color=textBackgroundColor)
    tableContents = ("<span class=\"md-subheading\">"
                    "All tests passed:" 
                    "{allPassed}</span><br/>").format(
                            allPassed=str(allTestCaseResult)) + tableContents
    textResults = ("All tests passed: {allPassed}\n").format(
                    allPassed=str(allTestCaseResult)) + textResults
    if not resultContent:
        textResults = "Your test is passing but something is incorrect..."
    htmlResults = """
        <html>
            <head>
                <meta charset="utf-8">
                <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
            </head>
            <body>
                <div>
                    <table>
                         <thead>
                            <tr>
                                <th>Method</th>
                                <th>Parameters</th>
                                <th>Response Target</th>
                                <th>Test Method</th>
                                <th>Test Value</th>
                                <th>Received Value</th>
                                <th>Status Code</th>
                                <th>Correct</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tableContents}
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
            </style>
        </html>
        """.format(tableContents=tableContents)
    allFeedback = {"isCorrect": allTestCaseResult,
                    "htmlFeedback": htmlResults, 
                    "textFeedback": textResults, 
                    "jsonFeedback": json.dumps(jsonResponseData, indent=4, sort_keys=True)}
    return allFeedback

def lambda_handler(event, context):
    method = event.get('httpMethod', {})
    indexPage = getIndexPage()
    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": indexPage
        }

    if method == 'POST':
        recResp = json.loads(event.get('body', {}))
        print("Received request")
        print(recResp)
        testUrl = recResp["editable"]["0"].strip()
        shownTest = recResp["shown"]["0"].strip().splitlines()
        userToken = recResp["userToken"].strip()
        #Execute tests
        shownJsonResp = exec_tests(testUrl,shownTest,userToken)
        result = shownJsonResp["results"]
        jsonResp = {"results": result}
        print(jsonResp)
        #Form feedback
        allFeedback = calcFeedback(jsonResp,userToken)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body":  json.dumps({
                "isComplete": allFeedback["isCorrect"],
                "jsonFeedback": allFeedback["jsonFeedback"],
                "htmlFeedback": allFeedback["htmlFeedback"],
                "textFeedback": allFeedback["textFeedback"]
            })
        }
