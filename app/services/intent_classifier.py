class IntentClassifier:

    def __init__(self):

        self.greetings = {
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        }

        self.thanks = {
            "thanks",
            "thank you",
            "thankyou",
            "thx"
        }

        self.farewells = {
            "bye",
            "goodbye",
            "see you",
            "see ya"
        }

        self.help_requests = {
            "help",
            "what can you do",
            "who are you"
        }

    def classify(self, query):

        query = query.lower().strip()

        if query in self.greetings:
            return "greeting"

        if query in self.thanks:
            return "thanks"

        if query in self.farewells:
            return "farewell"

        if query in self.help_requests:
            return "help"

        return "pdf"