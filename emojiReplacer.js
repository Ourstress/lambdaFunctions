exports.handler = async (event) => {
    
    const indexPage=`
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
            Hello enter your activity variables
            <input v-model="userVariables"/>
            Enter answer
            <input v-model="userAnswer" />
            <button v-on:click="postContents">Submit</button>
        </div>
    </body> 
    <script src="https://unpkg.com/vue"></script>
    <script src="https://unpkg.com/vue-material@beta"></script>
    <script>
    Vue.use(VueMaterial.default)
    
    new Vue({
        el: '#app',
        data: function () {
            return {
            userAnswer:"",
            userVariables:"",
            serverResponse:"" 
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
        body: JSON.stringify({editable:{0:this.userAnswer}, shown:{0:this.userVariables}})
        }).then(response => {
            return response.json()
        }).then(data => {
            this.serverResponse = JSON.parse(JSON.stringify(data))
            console.log(this.serverResponse)
            })
         }
        }        
      })
    </script>
    <style lang="scss" scoped>
        html{
            text-align:center;
        }
        h1{
            font-family: Schoolbell !important;
            margin-top: 1rem
        }
    </style>
    </html>
    `
    
    if (event.httpMethod === 'GET'){
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": indexPage
        }
    }
    
    function throwError(errorName){throw new Error(errorName)}
    
    if (event.httpMethod === 'POST'){
        const parsedBodyContent = JSON.parse(event.body)
        const activityVariables = parsedBodyContent["shown"]["0"] 
        const userSolution = parsedBodyContent["editable"]["0"]
        let executeUserSolution = ""
        let activityVariables2 = ""
        let errorMessage = ""
        let results = ""
        try {
            activityVariables2 = activityVariables.split(",")
            activityVariables2[0] ?
                activityVariables2[1] ? 
                    activityVariables2[2] ? null
                    : throwError("no third input")
                : throwError("no second input")
            : throwError("no first input")
        }
        catch(error){
            activityVariables2 = error.message
        }
        try {
            executeUserSolution = eval(userSolution)
        }
        catch(error) {
            errorMessage = `error executing your code: ${error.message}`
        }
        if (!errorMessage) {
            results = executeUserSolution === activityVariables2[0].toString().replace(activityVariables2[1].toString(),activityVariables2[2].toString())
        }
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": JSON.stringify(results || errorMessage) //{activityVariables2, executeUserSolution, errorMessage})
        }
    }
};
