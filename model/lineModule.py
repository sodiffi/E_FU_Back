import json
# from model import politicianModel
from coder import MyEncoder
import json
from linebot.models import (
    TextSendMessage, ImageSendMessage, StickerSendMessage)


class lineModule:

    @staticmethod
    def handle_messenge(event):
        msg = event.message.text
        return TextSendMessage(text='網址')
            