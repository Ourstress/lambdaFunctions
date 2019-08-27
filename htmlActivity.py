""" 
Steps to include bleach library in your own lambda function
1. create a folder to contain all the files we need
2. create a file called lambda_function.py (the name has to be lambda_function)
3. navigate to the directory in terminal / command prompt and run pip install bleach -t . (-t . installs bleach to current folder)
4. zip up the contents of the folder (don't zip up the folder itself but just the contents)
5. create a new lambda function in AWS
6. then in "code entry type" dropdown box which says "edit code inline", select "upload a .zip file"
7. upload your zip file
"""

import json
import re
import signal
    
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
         <h1>HTML Activity</h1>
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
                            <div v-html="layoutItems[0].vModel"></div>
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
                {header:"Expected Result", subHeader:'', vModel:"<h1>Today is a day for 🍨</h1>"},
                {header:"Editable HTML", subHeader:'Your code goes below', vModel:"<h1>Today is a day for</h1>"}
                ], status:" 🔴"},
                {name:"question 2", layoutItems: [
                {header:"Expected Result", subHeader:'', vModel:"<h2>Todos</h2><ol><li>Buy 🎃</li><li>Meet 🎅</li></ol>"},
                {header:"Editable HTML", subHeader:'Your code goes below', vModel:"<h2>Todos</h2><ol><li>Meet 🎅</li></ol"}
                ], status:" 🔴"},
                {name:"question 3", layoutItems: [
                {header:"Expected Result", subHeader:'', vModel:'Follow this <a href="https://blog.dnsimple.com/2016/09/how-dns-works/">link</a> to find out more about the DNS webcomic'},
                {header:"Editable HTML", subHeader:'Your code goes below', vModel:"Follow this <a https://blog.dnsimple.com/2016/09/how-dns-works/> to find out more about the DNS webcomic"}
                ], status:" 🔴"},
                {name:"question 4", layoutItems: [
                {header:"Expected Result", subHeader:'', vModel:'<form action="#" method="post"><input type="text" placeholder="name" name="user_name"/><input placeholder="email" type="email" name="user_mail"/><div class="button"><button type="submit">Send your message</button></div></form>'},
                {header:"Editable HTML", subHeader:'Your code goes below', vModel:'<form action="#" method="post"><input type="text" placeholder="name" name="user_name"/><input placeholder="" type="email" name="user_mail"/><div class="button"><button type="submit">Send your message</div></form>'}
                ], status:" 🔴"},
                {name:"question 5", layoutItems: [
                {header:"Expected Result", subHeader:'', vModel:'<table><thead><tr><th>Actual Name</th><th>Hero Name</th></tr></thead><tbody><tr><td>Peter Parker</td><td>Spiderman</td></tr><tr><td>Bruce Banner</td><td>The Hulk</td></tr></tbody></table>'},
                {header:"Editable HTML", subHeader:'Your code goes below', vModel:'<table><thead><tr><th>Actual Name</th><th>Hero Name</th></tr></thead><tbody><tr><td>Peter Parker</td><td>Spiderman</td></tr></tbody></table>'}
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
        margin: 10px;
        width:150px;
        height:40px
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
        margin:10px !important;
        width:80% !important;
        display:block
    }
    .md-field:after{
        height:0px
    }
    table{
        border-collapse:collapse
    }
    td {
        border:1px solid black
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
            for item in testCases.strip().splitlines():
                regexMatchHtmlContents = re.search(item, solution)
                expectedText = item.replace("<","&lt;").replace(">","&gt;")
                if hasattr(regexMatchHtmlContents, 'group'):
                    # escape < tag and > tag so it shows up in td cell
                    receivedText = solution.replace("<","&lt;").replace(">","&gt;")
                    if item == regexMatchHtmlContents.group(0):
                        textResults = textResults + "\nHurray! You have passed the test case. You expected {0} and provided the HTML code that contains it.\n".format(item)
                        textBackgroundColor = "#b2d8b2"
                else:
                    receivedText = solution.replace("<","&lt;").replace(">","&gt;")                 
                    textResults = textResults + "\nThe test case eludes your code so far but try again! Did not receive {0} as expected.\n".format(item)
                    textBackgroundColor = "#ff9999"
                    overallResults = "All tests passed: False"
                tableContents = tableContents + """
                    <tr bgcolor={2}>
                        <td>{0}</td>
                        <td>{1}</td>
                    </tr>
                    """.format(expectedText,receivedText,textBackgroundColor)
        except Exception as ex:
            if str(ex) == "processTooLong":
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
                        HTML code provided:
                    </p>
                    <div>
                        {2}
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
            """.format(overallResults, tableContents, solution)
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
