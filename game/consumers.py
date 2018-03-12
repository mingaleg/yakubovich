from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
    if message.user.player.game:
        Group(message.user.player.game.uuid.__str__()).add(message.reply_channel)
    Group("global").add(message.reply_channel)
    message.reply_channel.send({
        'accept': True,
    })


@channel_session_user
def ws_disconnect(message):
    if message.user.player.game:
        Group(message.user.player.game.uuid.__str__()).discard(message.reply_channel)
    Group("global").discard(message.reply_channel)


@channel_session_user
def ws_recieve(message):
    pass
