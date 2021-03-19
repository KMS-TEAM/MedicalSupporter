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