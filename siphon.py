SCHEME_PREFIX = '{http://www.reflective.com}'
SIPHON_TYPES = {'T': 'Text Substring', 'R': 'Regular Expression',}

class Siphon():

    # def __init__(self, sequence, type_, start, end, match_number):
    def __init__(self, element):
        self.sequence = element.get('SEQUENCE')
        self.type = element.get('TYPE')
        self.start = element.find(SCHEME_PREFIX+'STARTTEXT').text
        self.end = element.find(SCHEME_PREFIX+'ENDTEXT').text
        self.match_number = element.find(SCHEME_PREFIX+'RFINDEX').text

    def __repr__(self):
        result = 'Type: ' + SIPHON_TYPES[self.type] + '\n'
        result+= 'Match: ' + self.match_number + '\n'
        result+= 'Start text: ' + self.start + '\n'
        if self.end: result+= 'End text  : ' + self.end + '\n'
        return result+'\n'
