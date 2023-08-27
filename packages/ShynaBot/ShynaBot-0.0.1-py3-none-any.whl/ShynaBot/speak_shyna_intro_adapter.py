from chatterbot.logic import LogicAdapter


class ShynaIntro(LogicAdapter):
    conf = []

    def __init__(self, chatbot, **kwargs):
        super(ShynaIntro, self).__init__(chatbot, **kwargs)

    def can_process(self, statement):
        try:
            cmd_list = ["tell me something about your self",
                        "who are you",
                        "introduce yourself",
                        "give me your introduction",
                        "introduction",
                        "tell me about yourself",
                        "tell her about yourself",
                        "tell him about yourself",
                        "tell them about yourself",
                        "introduction please"]
            if str(statement).lower().startswith(tuple(cmd_list)):
                return True
            else:
                return False
        except AttributeError:
            return False
        except Exception as e:
            print("Exception at Intro adapter in Chatter Bot", e)
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        from chatterbot.conversation import Statement
        import requests
        url = "https://shyna623.com/sdb/shynacontact/get_shyna_intro.php"
        payload = {'host': '216.10.252.35',
                   'username': 'shyna2t5_shyna',
                   'passwd': 'MajorShyna@623'}
        response = requests.request("POST", url, data=payload)
        if response.status_code == 200:
            confidence = 1
            response_statement = Statement(text=str(response.json()[0]['intro_sent']))
            response_statement.confidence = confidence
        else:
            confidence = 1
            response_statement = Statement(text="Internal Server Error")
            response_statement.confidence = confidence
        return response_statement
