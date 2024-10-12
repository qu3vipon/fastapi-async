from shared.config import SERVER_PORT

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <style>
        #messages {
            list-style-type: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
        }

        li {
            margin: 5px 0;
            max-width: 80%;
            border-radius: 10px;
            padding: 10px;
            color: #fff;
        }

        .my-message {
            align-self: flex-end;
            background-color: #007bff;
        }

        .other-message {
            align-self: flex-start;
            background-color: #6c757d;
        }
    </style>
    </head>
    <body>
        <div class="container">
          <h1 class="mt-5">💬 오픈 채팅 [PORT] </h1>
          <hr>
        <h5 class="mt-3">My ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
        <div class="input-group mb-3">
            <input class="form-control" type="text" id="messageText" autocomplete="off"/ placeholder="메시지를 입력하세요..">
            <button class="btn btn-dark">보내기</button>
        </div>

        </form>
        <ul id='messages'>
        </ul>
        </div>

        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id
            var ws = new WebSocket(`ws://localhost:PORT/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');

                if (event.data.startsWith("<Me>")) {
                    var content = document.createTextNode(event.data.replace("<Me>", ""));
                    message.classList.add('my-message');
                } else {
                    var content = document.createTextNode(event.data.replace("<Them>", ""));
                    message.classList.add('other-message');
                }

                message.appendChild(content);
                messages.appendChild(message);
        };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
""".replace("PORT", SERVER_PORT)
