# This activity requires Python 2.7 runtime
# -*- coding: utf-8 -*-
import json
import traceback
import logging
import doctest

import re

import signal
import time

    
def lambda_handler(event, context):
    
    def run_local(requestDict):
        #namespace = UsedNamespace()
    
        #Add a try here to catch errors and return a better response
        solution = requestDict['solution']
        tests = requestDict['tests']
    
        import StringIO
        import sys
        # Store App Engine's modified stdout so we can restore it later
        gae_stdout = sys.stdout
        # Redirect stdout to a StringIO object
        new_stdout = StringIO.StringIO()
        sys.stdout = new_stdout

        try:
            namespace = {}
            compiled = compile('import json', 'submitted code', 'exec')
            exec compiled in namespace
            compiled = compile(solution, 'submitted code', 'exec')
            exec compiled in namespace
            namespace['YOUR_SOLUTION'] = solution.strip()
            namespace['LINES_IN_YOUR_SOLUTION'] = len(solution.strip().splitlines())

            test_cases = doctest.DocTestParser().get_examples(tests)
            results, solved = execute_test_cases(test_cases, namespace)
        
            # Get whatever was printed to stdout using the `print` statement (if necessary)
            printed = new_stdout.getvalue()
            # Restore App Engine's original stdout
            sys.stdout = gae_stdout
        
            responseDict = {"solved": solved , "results": results, "printed":printed}
        
            #Add a try here can catch errors. 
            responseJSON = json.dumps(responseDict)
            logging.info("Python verifier returning %s",responseJSON)
            return responseJSON
        except:
            sys.stdout = gae_stdout
            errors = traceback.format_exc()
            logging.info("Python verifier returning errors =%s", errors)
            if len(errors) > 500:
                lines = errors.splitlines()
                i = len(lines) - 1
                errors = lines[i]
                i -= 1
                while i >= 0:
                    line = lines[i]
                    s = '%s\n%s' % (line, errors)
                    if len(s) > 490:
                        break
                    errors = s
                    i -= 1
                errors = '...\n%s' % errors

            responseDict = {'errors': '%s' % errors}
            responseJSON = json.dumps(responseDict)
            #logging.info("######## Returning json encoded errors %s", responseJSON)
            return responseJSON

    #Refactor for better readability.
    def execute_test_cases(testCases, namespace):
        resultList = []
        solved = True
        for e in testCases:
            if not e.want:
                exec e.source in namespace
                continue
            call = e.source.strip()
            logging.warning('call: %s', (call,))
            got = eval(call, namespace)
            expected = eval(e.want, namespace)
        
            correct = True
            if got == expected:
                correct = True
            else:
                correct = False
                solved = False
            resultDict = {'call': call, 'expected': expected, 'received': "%(got)s" % {'got': got}, 'correct': correct}
            resultList.append(resultDict)
        return resultList, solved
    
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
         <h1>Doctest Activity for Learning Python</h1>
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
        body: JSON.stringify({shown:{0:this.layoutItems[0].vModel},editable:{0:this.layoutItems[1].vModel}})
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
                {header:"Tests", subHeader:'', vModel:">>> sum(1,2)\\n3 \\n>>> sum(2,2)\\n4"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"def sum(a,b):\\n return b+1"}
                ], status:" 🔴"},
                {name:"question 2", layoutItems: [
                {header:"Tests", subHeader:'', vModel:">>> multiply(1,2)\\n2 \\n>>> multiply(2,3)\\n6"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"def multiply(a,b):\\n return b"}
                ], status:" 🔴"},
                {name:"question 3", layoutItems: [
                {header:"Tests", subHeader:'', vModel:">>> floorDivide(10,2)\\n5 \\n>>> floorDivide(2,3)\\n0"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"def floorDivide(a,b):\\n return b"}
                ], status:" 🔴"},
                {name:"question 4", layoutItems: [
                {header:"Tests", subHeader:'', vModel:">>> logicAndOperation(True,True)\\nTrue \\n>>> logicAndOperation(False,True)\\nFalse"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"def logicAndOperation(a,b):\\n return b"}
                ], status:" 🔴"},
                {name:"question 5", layoutItems: [
                {header:"Tests", subHeader:'', vModel:">>> doubleEqualOperation(12,12)\\nTrue \\n>>> doubleEqualOperation(12,13)\\nFalse"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:"def doubleEqualOperation(a,b):\\n return b"}
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
            jsonResponse = run_local({"solution": solution, "tests": testCases})
        except Exception as ex:
            if "processTooLong" in ex:
                timeout = True
                print("processTooLong triggered")
        # set the alarm to 0 seconds after all is done
        finally:
            signal.alarm(0)

        jsonResponseData = json.loads(jsonResponse)
        
        solvedStatusText = expectedText = receivedText = callText = textResults = tableContents = ""
        overallResults = """<span class="md-subheading">All tests passed: {0}</span><br/>""".format(str(jsonResponseData.get("solved")))
        numTestCases = len(re.findall('>>>', testCases))
        resultContent = jsonResponseData.get('results') 
        textBackgroundColor = "#ffffff"
        
        if resultContent:
            for i in range(len(resultContent)):
                expectedText = resultContent[i]["expected"]
                receivedText = resultContent[i]["received"]
                correctText = resultContent[i]["correct"]
                callText = resultContent[i]["call"]
                if str(expectedText) == str(receivedText):
                    textResults = textResults + "\nHurray! You have passed the test case. You called {0} and received {1} against the expected value of {2}.\n".format(callText, receivedText, expectedText)
                    textBackgroundColor = "#b2d8b2"
                else:
                    textResults = textResults + "\nThe test case eludes your code so far but try again! You called {0} and received {1} against the expected value of {2}.\n".format(callText, receivedText, expectedText)
                    textBackgroundColor = "#ff9999"
                tableContents = tableContents + """
                <tr bgcolor={4}>
                    <td>{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                    <td>{3}</td>
                </tr>
                """.format(callText,expectedText,receivedText,correctText,textBackgroundColor)
        solvedStatusText = str(jsonResponseData.get("solved")) or "error"
        textResults = """All tests passed: {0}\n""".format(solvedStatusText) + textResults
        if not resultContent:
            textResults = "Your test is passing but something is incorrect..."
            
        if timeout or jsonResponseData.get("errors"):
            textResults = "An error - probably related to code syntax - has occured. Do look through the JSON results to understand the cause."
            tableContents = """
                <tr>
                    <td></td>
                    <td></td>
                    <td>error</td>
                    <td></td>
                </tr>
                """
        htmlResults="""
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
                </head>
                <body>
                    <div>
                        {0}
                        <span class="md-subheading tableTitle">Tests</span>
                        <table>
                             <thead>
                                <tr>
                                    <th>Called</th>
                                    <th>Expected</th>
                                    <th>Received</th>
                                    <th>Correct</th>
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
            </html>
            """.format(overallResults,tableContents)
        return {
            "statusCode": 200,
            "headers": {
            "Content-Type": "application/json",
                },
            "body":  json.dumps({
                "isComplete":jsonResponseData.get("solved"),
                "jsonFeedback": jsonResponse,
                "htmlFeedback": htmlResults,
                "textFeedback": textResults
            })
            }
