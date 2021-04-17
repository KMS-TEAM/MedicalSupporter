class Words:
    def __init__(self):
        self.text = ''
        self.tagging = ''

class Chunk:
    def __init__(self):
        self.text = ''
        self.root_text = ''
        self.root_dep = ''
        self.root_head_text = ''

class Entities:
    def __init__(self):
        self.text = ''
        self.label = ''

class Transcription:
    def __init__(self, id, des, medical_specialty, sample_name, trans, keywords):
        self.id = id
        self.transcription = trans
        self.description = des
        self.medicalspecialty = medical_specialty
        self.sample_name = sample_name
        self.keywords = keywords