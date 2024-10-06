const socket = io.connect('https://' + document.domain + ':' + location.port);
const messageForm = document.getElementById("message-form");
const userText = document.getElementById("user-text");
const messageText = document.getElementById("message-text");
const sendButton = document.getElementById('message-send-button');
const messageHolder = document.getElementById('message-holder');

function appendMessage(payload) {
    const timestamp = payload.timestamp;
    const user = payload.user;
    const content = payload.content
    console.log('(' + timestamp + ') New message from ' + user + ' received: ' + content );
    const message_li = document.createElement('li');
    message_li.textContent = '(' + timestamp + ') ' + user + ': ' + content;
    messageHolder.appendChild(message_li);
}

socket.on( 'connect', function() {
    console.log("Connected successfully!")
})

socket.on( 'all-messages', function(data) {
    messageHolder.replaceChildren(); // This removes all children
    console.log(data);
    data.forEach(payload => {
        appendMessage(payload)
    });
    messageHolder.scrollTop = messageHolder.scrollHeight;
})

// Add an event listener to listen for 'click' events
sendButton.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the form from submitting (if needed)

    // Get the input fields values
    const user = userText.value;
    const content = messageText.value;
    messageText.value = '';

    // Perform an action with the value
    console.log('Message from ' + user + ' submitted: ' + content);
    
    socket.emit( 'message-submit', {
        user    : user,
        content : content
    }, );
});
