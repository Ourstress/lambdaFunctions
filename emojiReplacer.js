exports.handler = async event => {
  const indexPage = `
    <html>
    <head>
    <meta charset="utf-8">
    <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
    <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
    <link href="https://fonts.googleapis.com/css?family=Schoolbell&display=swap" rel="stylesheet">
  </head>
    <body>
         <h1>Emoji replacement activity</h1>
        <div id="app">
            <md-tabs>
                <md-tab v-for="question in questions" :key=question.name v-bind:md-label=question.name+question.status>
                    <emoji-activity v-bind:layout-things=question.layoutItems v-bind:question-name=question.name  @questionhandler="toggleQuestionStatus"/>
                </md-tab>
            </md-tabs>
        </div>
    </body> 
    <script src="https://unpkg.com/vue"></script>
    <script src="https://unpkg.com/vue-material@beta"></script>
    <script>
    Vue.use(VueMaterial.default)

    Vue.component('emoji-activity', {
        props: ['layoutThings', 'questionName'],
        data: function () {
            return {
            answer:{jsonFeedback:'',htmlFeedback:'',textFeedback:'',isComplete:false},
            layoutItems: this.layoutThings
        }
        },
        methods: {
            postContents: function () {
                // comment: leaving the gatewayUrl empty - API will post back to itself
                const gatewayUrl = '';
                this.$set(this, 'answer', {jsonFeedback:'',htmlFeedback:'',textFeedback:'',isComplete:false})
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
        \`<div class="md-layout  md-gutter">
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
        \`
    })
    
    new Vue({
        el: '#app',
        data: function () {
            return {
            questions:[
                {name:"question 1", layoutItems: [
                {header:"Activity variables", subHeader:'comma-separated sequence comprising a string, replaced character(s), replacement characters(s)', vModel:"hello,h,hoho"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:\`"hello".replace("h","hoho")\`}
                ], status:" 🔴"},
                {name:"question 2", layoutItems: [
                {header:"Activity variables", subHeader:'comma-separated sequence comprising a string, replaced character(s), replacement characters(s)', vModel:"who let the dogs out,dogs,cats"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:\`"who".replace()\`}
                ], status:" 🔴"},
                {name:"question 3", layoutItems: [
                {header:"Activity variables", subHeader:'comma-separated sequence comprising a string, replaced character(s), replacement characters(s)', vModel:"It was raining cats and dogs,cats and dogs,😺 & 🐶"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:\`"It was raining cats and dogs".replace()\`}
                ], status:" 🔴"},
                {name:"question 4", layoutItems: [
                {header:"Activity variables", subHeader:'comma-separated sequence comprising a string, replaced character(s), replacement characters(s)', vModel:"Python is awesome,Python,🐍"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:\`""\`}
                ], status:" 🔴"},
                {name:"question 5", layoutItems: [
                {header:"Activity variables", subHeader:'comma-separated sequence comprising a string, replaced character(s), replacement characters(s)', vModel:"I wish I had a pet pony,pony,🐎"},
                {header:"Editable Code Block", subHeader:'Your code goes below', vModel:\`""\`}
                ], status:" 🔴"}                 
            ]            
        }
        },
        methods: {
            toggleQuestionStatus (response) {
                const {data, questionName} = response
                if (data.htmlFeedback) {
                    const searchText = data.htmlFeedback
                    if (searchText.includes("You have got the answer")) this.questions.find(item => item.name === questionName).status = " ✔️";
                    else if (searchText === "You have missed the answer... check your code again?") this.questions.find(item => item.name === questionName).status = " 🤨";
                    else this.questions.find(item => item.name === questionName).status = " 🔴"
                }
            }
        }
      })
    </script>
    <style lang="scss" scoped>
    h1{
        font-family: Schoolbell !important;
        margin-top: 1rem;
        padding:20px;
        text-align: center
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
    `;

  if (event.httpMethod === "GET") {
    return {
      statusCode: 200,
      headers: {
        "Content-Type": "text/html"
      },
      body: indexPage
    };
  }

  function throwError(errorName) {
    throw new Error(errorName);
  }
  const trimAndStringify = input => input.toString().trim();

  if (event.httpMethod === "POST") {
    const parsedBodyContent = JSON.parse(event.body);
    const activityVariables = parsedBodyContent["shown"]["0"]
      .replace(/\s+/g, " ")
      .replace(/&zwnj;.*&zwnj;/, "");
    const userSolution = parsedBodyContent["editable"]["0"];
    let executeUserSolution = "";
    let activityVariables2 = "";
    let errorMessage = "";
    let results = "";
    let htmlResults = "";
    try {
      activityVariables2 = activityVariables.split(",");
      activityVariables2[0]
        ? activityVariables2[1]
          ? activityVariables2[2]
            ? null
            : throwError("no third input")
          : throwError("no second input")
        : throwError("no first input");
    } catch (error) {
      errorMessage = error.message;
    }
    try {
      executeUserSolution = eval(userSolution);
    } catch (error) {
      errorMessage = `error executing your code: ${error.message}`;
    }
    if (!errorMessage) {
      executeUserSolution ===
      trimAndStringify(activityVariables2[0]).replace(
        trimAndStringify(activityVariables2[1]),
        trimAndStringify(activityVariables2[2])
      )
        ? (results = "You got the answer!") &&
          (htmlResults = `You have got the answer: ${executeUserSolution}`)
        : (results = "You have missed the answer... check your code again?");
    }
    const textResults = results || errorMessage;
    return {
      statusCode: 200,
      headers: {
        "Content-Type": "text/html"
      },
      body: JSON.stringify({
        isComplete: results === "You got the answer!",
        jsonFeedback: JSON.stringify(textResults),
        htmlFeedback: htmlResults || textResults,
        textFeedback: textResults
      })
    };
  }
};
