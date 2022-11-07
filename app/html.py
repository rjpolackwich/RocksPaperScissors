
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>RPS</title>
    </head>
    <body>
        <h1>Rock Paper Scissors</h1>
        <form action="">
            <label>Username: <input type="text" id="userName" autocomplete="off"/></label>
            <button onclick="connect(event)">Connect</button>
        </form>
        <hr>
        <form action="">
            <fieldset>
                <legend>Select your Throw:</legend>
                    <div>
                        <input type="radio" id="rockChoice" name="throwSelection" value="rock" checked/>
                        <label for="rockChoice">Rock</label>
                        <input type="radio" id="paperChoice" name="throwSelection" value="paper" />
                        <label for="paperChoice">Paper</label>
                        <input type="radio" id="scissorsChoice" name="throwSelection" value="scissors" />
                        <label for="scissorsChoice">Scissors</label>
                    </div>
                <div>
                    <button onclick="playSelection(event)">Play Throw!</button>
                </div>
            </fieldset>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var userName = document.getElementById("userName")
                ws = new WebSocket("ws://localhost:8001/ws/" + userName.value);
                console.log(ws)
                ws.onmessage = function(event) {
                    console.log("got on message")
                    console.log(event.data)
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function playSelection(event) {
                console.log(event.data)
                console.log("in playselection")
                var throws = document.getElementsByName("throwSelection")
                console.log(throws)
                for (const t of throws) {
                    console.log(t)
                    if (t.checked == true) {
                        ws.send(t.value)
                    }
                }
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""



