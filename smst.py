def sendsms(token,action):
    from twilio.rest import Client
    number='+917507483508'
    account_sid = 'AC9ca57309561dff05e457f51f0d40370a'
    auth_token = 'd5a27293ea20119e6a61f540983efb30'
    client = Client(account_sid, auth_token)
    if action=='E':
        body1="Your token number  already exists and token number is: '{0}'"
    elif action =='N':
        body1="Your token number generated successfully  and token number is: '{0}'"
    body2=body1.format(token)
    message = client.messages.create(
                body=body2,
                from_='+17065100684',
                to=number,
                )