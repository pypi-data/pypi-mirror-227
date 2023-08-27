import os
from chatterbot import ChatBot


class StartTheBot:
    data_child = []
    speak_bot = ChatBot("speak_bot",
                        # response_selection_method=get_random_response,
                        logic_adapters=[
                            {
                                'import_path': 'speak_shyna_intro_adapter.ShynaIntro',
                                'default_response': 'False',
                                'maximum_similarity_threshold': 1
                            },
                        ]
                        )

    def get_ans_by_apt(self, user_input):
        try:
            bot_response_text = self.speak_bot.get_response(user_input)
            if str(bot_response_text).__eq__('False'):
                return False
            else:
                return bot_response_text
        except AttributeError:
            return False

    def get_ans(self, user_input_ans):
        # print("getting ans")
        bot_response_sent = ""
        try:
            print("seeking answer for ", user_input_ans)
            bot_response_sent = self.get_ans_by_apt(user_input=str(user_input_ans).lower())
            print("Final response is ", bot_response_sent)
        except Exception as e:
            bot_response_sent = "Dammit! exception. I have sent you the details"
        finally:
            return bot_response_sent


# test = StartTheBot()
# test.get_ans(user_input_ans="introduction")
