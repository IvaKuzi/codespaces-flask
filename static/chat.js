const socket = io(); // if your front is served on the same domain as your server
const userText = document.getElementById("user-text");
const messageText = document.getElementById("message-text");
const messageHolder = document.getElementById('message-holder');
const sendButton = document.getElementById('message-send-button');

socket.on( 'connect', function() {
    console.log("Connected successfully!")
    console.log("Socket connected: " + socket.connected); // true
});

socket.on( 'disconnect', function() {
    console.log("Disconnected!")
    console.log("Socket connected: " + socket.connected); // true
});

// Add an event listener to listen for 'click' events
sendButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting

    // Get the input fields values
    const user = userText.value;
    const content = messageText.value;

    messageText.value = '';
    console.log('Message from ' + user + ' submitted: ' + content);
    
    const payload = {
		        user    : user,
		        content : content
		};
    
    // Emit message
    socket.emit('message-submit', payload);
});

function appendMessage(payload) {
    const timestamp = payload.timestamp;
    const user = payload.user;
    const content = payload.content
    const message_li = document.createElement('li');
    message_li.textContent = '(' + timestamp + ') ' + user + ': ' + content;
    messageHolder.appendChild(message_li);
};

socket.on( 'all-messages', function(data) {
    console.log("Received list of all messages.");
    messageHolder.replaceChildren(); // This removes all children
    data.forEach(payload => {
        appendMessage(payload)
    });
    messageHolder.scrollTop = messageHolder.scrollHeight;
});