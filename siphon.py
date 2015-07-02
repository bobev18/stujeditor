SCHEME_PREFIX = '{http://www.reflective.com}'
SIPHON_TYPES = {'T': 'Text Substring', 'R': 'Regular Expression', 'D': 'Delimiter', 'I': 'Position', 'Y': 'Replace'}

class Siphon():

    # def __init__(self, sequence, type_, start, end, match_number):
    def __init__(self, element):
        self.sequence = element.get('SEQUENCE')
        self.type = element.get('TYPE')
        self.start = element.find(SCHEME_PREFIX+'STARTTEXT').text
        if self.start == None:
            self.start = ''
        self.end = element.find(SCHEME_PREFIX+'ENDTEXT').text
        if self.end == None:
            self.end = ''
        self.match_number = element.find(SCHEME_PREFIX+'RFINDEX').text
        # self.as_dict = {'SEQUENCE': self.sequence, 'TYPE': self.type, 'STARTTEXT': self.start, 'ENDTEXT': self.end, 'RFINDEX': self.match_number}

    def __repr__(self):
        result = 'Type: ' + SIPHON_TYPES[self.type] + '\n'
        result+= 'Match: ' + self.match_number + '\n'
        result+= 'Start text: ' + self.start + '\n'
        if self.end: result+= 'End text  : ' + self.end + '\n'
        return result+'\n'

