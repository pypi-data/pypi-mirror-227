from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokenType(Enum):

    HEAD = 0
    DIRT = 1
    GOLD = 2


@dataclass
class Token:

    end_index: int = -1
    pattern: str = ""
    next_token: Token = None
    previous_token: Token = None
    token_type: TokenType = None


class Patex:

    def __init__(self, pattern: str) -> None:

        self.p_string = pattern
        self._head = Token(0, token_type=TokenType.HEAD)
        self._get_tokens()

    def run(self, target: str) -> dict[str, Any]:

        current_token = self._head.next_token
        current_str = target
        mined = {}

        while current_token:
            
            if current_token.token_type == TokenType.DIRT:
                
                if current_str.find(current_token.pattern):

                    raise ValueError(f"The target doesn't match the pattern: pattern end-index=\"{current_token.end_index}\"")
                
                current_str = current_str[len(current_token.pattern):]
            
            else:
                
                #right now we just handle dirt-gold-dirt
                if current_token.next_token:
                    pattern = current_token.next_token.pattern
                    if current_str.find(pattern) == -1:
                        raise ValueError("There is an error, it should change later")
                    
                    mined_text = current_str[:current_str.find(pattern)]
                    current_str = current_str[current_str.find(pattern):]
                else:
                    mined_text = current_str

                mined[current_token.pattern] = mined_text
            
            current_token = current_token.next_token

        return mined

    def _get_tokens(self):

        tokens = []
        gold_count = 0
        current_token = ""
        previous_token = self._head

        for idx, c in enumerate(self.p_string):

            current_token += c

            if c == "{":
                if gold_count == 0:
                    if current_token[:-1]:
                        previous_token.next_token = Token(
                            idx - 1, current_token[:-1], token_type=TokenType.DIRT, previous_token=previous_token)
                        previous_token = previous_token.next_token

                    current_token = ""
                gold_count += 1

            elif c == "}":
                gold_count -= 1
                if gold_count == 0:
                    previous_token.next_token = Token(
                        idx, current_token[:-1], token_type=TokenType.GOLD, previous_token=previous_token)
                    previous_token = previous_token.next_token
                    current_token = ""
