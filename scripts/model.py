class Sentence:
    def __init__(self, user_id, pub_count, sent_count, sentence):
        self.id = f's_{user_id}_{pub_count}_{sent_count}'
        self.text = sentence

    def toTREC(self):
        return f'\
        <DOC>\n\
            \t<DOCNO>{self.id}</DOCNO>\n\
            \t<TEXT>{self.text}</TEXT>\n\
        </DOC>\n'
    