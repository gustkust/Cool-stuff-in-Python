import fbchat


print("This program writes song to a friend on facebook word by word.\n")
song = input("type songs lyrics in one line:")
song = song.split()
username = input("type your username:\n")
password = input("type your password:\n")
client = fbchat.Client(username, password)
friend = client.searchForUsers(input("type friends name:\n"))[0]
for word in song:
    client.send(fbchat.models.Message(word), friend.uid)
