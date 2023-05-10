import sys
import re

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment_line(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()
    
    def skip_comment_block(self):
        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()
                self.advance()
                break
            else:
                self.advance()
    
    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None
    
    def get_number(self):
        number = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char.lower() in 'abcdefx'):
            number += self.current_char
            self.advance()
        if number.startswith('0x'):
            return int(number, 16)
        else:
            return int(number)
    
    def get_operator(self):
        operator = ''
        while self.current_char is not None and self.current_char in '+-*/%^':
            operator += self.current_char
            self.advance()
        return operator
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '/':
                if self.peek() == '/':
                    self.skip_comment_line()
                    continue
                elif self.peek() == '*':
                    self.advance()
                    self.advance()
                    self.skip_comment_block()
                    continue
            
            if self.current_char.isdigit() or self.current_char.lower() in 'abcdefx':
                return Token('TokNumber', self.get_number())
            
            if self.current_char in '+-*/%^':
                return Token('TokOp', self.get_operator())
            
            raise Exception(f'Unexpected character: {self.current_char}')
        
        return Token('TokEOF', None)
    

if __name__ == '__main__':
    text = sys.stdin.read()
    lexer = Lexer(text)
    
    while True:
        token = lexer.get_next_token()
        if token.type == 'TokEOF':
            break
        print(token.type, token.value)
