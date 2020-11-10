var ws = new WebSocket("ws://[::1]:15674/ws")
var client = Stomp.over(ws);
var on_connect = function() {
    console.log('connected');
//    client.subscribe('spots', function(d) {
//        console.log('spot');
//        var debug = '';
//    });
}
var on_error = function() {
    console.log('error');
}
client.connect('guest', 'guest', on_connect, on_error, '/');
