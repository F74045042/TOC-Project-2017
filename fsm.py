from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    count = 0

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def user_to_play(self, update):
        text = update.message.text
        return text.lower() == '/play'

    def play_to_ask(self, update):
        text = update.message.text
        return text.lower() == 'ask'

    def ask_to_John(self, update):
        text = update.message.text
        return text == 'John'


    def ask_to_Sam(self, update):
        text = update.message.text
        return text == 'Sam'
    

    def ask_to_Mary(self, update):
        text = update.message.text
        return text == 'Mary'
    
    def play_to_arrest(self, update):
        text = update.message.text
        return text == 'arrest'
    
    def arrest_to_John(self, update):
        text = update.message.text
        if text == "John":
            update.message.reply_text("John: Yes, I'm the one.")
            update.message.reply_text("John: Now you know the truth, and I'm GONNA TO KILL YOU!!!")
            update.message.reply_photo("https://orig00.deviantart.net/0b2c/f/2014/034/a/a/jeffthekiller_by_leepicrainbow-d74zjxh.jpg")
            update.message.reply_text("GameOver... You're Dead....")
        if text == "Sam": 
            update.message.reply_text("Sam: No, I'm not the killer...")
            update.message.reply_text("Sam: That Killer is Running away because of you!!!")
            update.message.reply_photo("http://cdn.clm02.com/ezvivi.com/211682/211682_1.jpg")
            update.message.reply_text("GameOver...")
        if text == "Mary":
            update.message.reply_text("Mary: You let me down...")
            update.message.reply_photo("https://cdn.pixabay.com/photo/2017/07/17/22/00/furious-2514031_960_720.jpg")
            update.message.reply_text("GameOver...")
        return 1

    def on_enter_play(self, update):
        update.message.reply_text("There's a billionaire has been murdered last night. We found 3 suspects, and we know one of them is lying...")
        update.message.reply_text("But the killer is Telling the truth...")
        update.message.reply_text("Who is the Killer? maybe we should ask them...")
        update.message.reply_text("1.ask")
        update.message.reply_text("2.arrest")
    
    def on_enter_ask(self, update):
        update.message.reply_text("Let's ask someone...")
        update.message.reply_text("1.John")
        update.message.reply_text("2.Sam")
        update.message.reply_text("3.Mary")
    
    def on_enter_arrest(self, update):
        update.message.reply_text("Who is the Killer?")
        update.message.reply_text("We got only one chance")
        update.message.reply_text("1.John")
        update.message.reply_text("2.Sam")
        update.message.reply_text("3.Mary")

    def on_enter_John(self, update):
        update.message.reply_text("John: Sam didn't kill anyone.")
        self.go_back(update)

    def on_enter_Sam(self, update):
        update.message.reply_text("Sam: John is telling the truth.")
        self.go_back(update)
    
    def on_enter_Mary(self, update):
        update.message.reply_text("Mary: John is lying.")
        self.go_back(update)
