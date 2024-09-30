# signal_receive

This will create a service which will listen on the websocket to catch any received signal messages.

Works on my machine ;-)
* Raspberry PI4 with Supervised HomeAssistant OS

* Precondition:
  * Installed and correctly configured Signal Messenger AddOn (https://github.com/haberda/signal-addon/tree/main)
  * Config Signal Messenger with json-rpc (which is the best performance wise but makes message receiving only available via websocket)

Only proceed when you are sure, that sending Signal messages is working.

* Configuration:
  * phone_number: The phone number which is RECEIVING the messages
  * allowed_phone_numbers: A list of phone numbers to which you want to react

What will happen:
Whenever a new message is received the event "signal_message_received" is triggered with the content.
Only data messages (=new message) will trigger an event.
If a list of allowed phone numbers is given, an event is only triggered if the sender is within this list.
