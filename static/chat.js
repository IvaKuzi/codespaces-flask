const socket = io(); // if your front is served on the same domain as your server
const messageForm = document.getElementById("message-form");
const userText = document.getElementById("user-text");
const messageText = document.getElementById("message-text");
const sendButton = document.getElementById('message-send-button');
const messageHolder = document.getElementById('message-holder');
const usersHolder = document.getElementById('active-users-holder');

function appendMessage(payload) {
    const timestamp = payload.timestamp;
    const user = payload.user;
    const content = payload.content
    const message_li = document.createElement('li');
    message_li.textContent = '(' + timestamp + ') ' + user + ': ' + content;
    messageHolder.appendChild(message_li);
};

function appendUser(user) {
    const user_li = document.createElement('li');
    user_li.textContent = user;
    usersHolder.appendChild(user_li);
};

socket.on( 'connect', function() {
    console.log("Connected successfully!")
    console.log("Socket connected: " + socket.connected); // true

    const engine = socket.io.engine;
    console.log("Transport: " + engine.transport.name); // in most cases, prints "polling"

    engine.once("upgrade", () => {
        // called when the transport is upgraded (i.e. from HTTP long-polling to WebSocket)
        console.log('Upgraded transport to: ' + engine.transport.name); // in most cases, prints "websocket"
    });

    engine.on("packet", ({ type, data }) => {
        // called for each packet received
        console.log("Packet received!")
    });
    
    engine.on("packetCreate", ({ type, data }) => {
        // called for each packet sent
        console.log("Packet sent!")
    });
    
    engine.on("drain", () => {
        // called when the write buffer is drained
        console.log("Write buffer is drained!")
    });
    
    engine.on("close", (reason) => {
        // called when the underlying connection is closed
        console.log("Connection closed!")
    });
});

socket.on( 'disconnect', function() {
    console.log("Disconnected!")
    console.log("Socket connected: " + socket.connected); // true
});

socket.on("connect_error", (error) => {
    if (socket.active) {
      // temporary failure, the socket will automatically try to reconnect
      console.log("Connection error! Temporary failure, the socket will automatically try to reconnect.")
    } else {
      // the connection was denied by the server
      // in that case, `socket.connect()` must be manually called in order to reconnect
      console.log("Connection error!" + error.message);
      console.log("Trying to reconnect ... ");
      socket.connect();
    }
});

socket.on( 'all-messages', function(data) {
    console.log("Received list of all messages.");
    messageHolder.replaceChildren(); // This removes all children
    //console.log(data);
    data.forEach(payload => {
        appendMessage(payload)
    });
    messageHolder.scrollTop = messageHolder.scrollHeight;
});

socket.on( 'update-users', function(usernames) {
    console.log("Updating list of active users.");
    console.log(usernames)
    usersHolder.replaceChildren(); // This removes all children
    appendUser("Users online: ")
    usernames.forEach(user => {
        appendUser(user)
    });
});

// Add an event listener to listen for 'click' events
sendButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting (if needed)

    // Get the input fields values
    const user = userText.value;
    const content = messageText.value;
    if( content != '' ) {
        messageText.value = '';

        // Perform an action with the value
        console.log('Message from ' + user + ' submitted: ' + content);
    
        socket.emit( 'message-submit', {
            user    : user,
            content : content
        }, );
    };
});