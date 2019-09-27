from twilio.rest import Client



# Your Account SID from twilio.com/console
account_sid = "AC342847da381754ad0085aaffb40cf46a"
# Your Auth Token from twilio.com/console
auth_token  = "b6b91d29101d35f641a17bc7ae5413bc"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+919877452151",
    from_="+14159697091",
    body="Hello from Sewak!")

print(message.sid)
