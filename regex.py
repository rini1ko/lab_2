from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    def __init__(self) -> None:
        self.next_states: list[State] = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class StartState(State):
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return True


class TerminationState(State):
    def __init__(self):
        super().__init__()

    def check_self(self, char: str) -> bool:
        return False


class DotState(State):
    """
    state for . character (any character accepted)
    """
    def __init__(self):
        super().__init__()

    def check_self(self, char: str):
        return True


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.curr_sym = symbol

    def check_self(self, curr_char: str) -> bool:
        return curr_char == self.curr_sym


class StarState(State):
    def __init__(self, checking_state: State):
        super().__init__()
        self.checking_state = checking_state

    def check_self(self, char):
        if self.checking_state.check_self(char):
            return True
        for state in self.next_states:
            if state.check_self(char):
                return True
        return False


class PlusState(State):
    def __init__(self, checking_state: State):
        super().__init__()
        self.checking_state = checking_state

    def check_self(self, char):
        return self.checking_state.check_self(char)


class RegexFSM:
    def __init__(self, regex_expr: str) -> None:
        self.curr_state = StartState()
        prev_state = self.curr_state
        tmp_next_state = self.curr_state

        for char in regex_expr:
            new_state = self.__init_next_state(char, prev_state, tmp_next_state)

            if char in ("*", "+"):
                prev_state.next_states.pop()
                prev_state.next_states.append(new_state)
                tmp_next_state = new_state
            else:
                if tmp_next_state != self.curr_state:
                    prev_state = tmp_next_state
                prev_state.next_states.append(new_state)
                tmp_next_state = new_state
        tmp_next_state.next_states.append(TerminationState())

    def __init_next_state(
        self, next_token: str, prev_state: State, tmp_next_state: State
    ) -> State:
        new_state = None

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()
            case next_token if next_token == "*":
                new_state = StarState(tmp_next_state)
            case next_token if next_token == "+":
                new_state = PlusState(tmp_next_state)
            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)
            case _:
                raise AttributeError("Character is not supported")

        return new_state

    def check_string(self, string: str) -> bool:
        def match(state: State, text: str) -> bool:
            if isinstance(state, TerminationState):
                return len(text) == 0

            if isinstance(state, StartState):
                return any(match(nxt, text) for nxt in state.next_states)

            if isinstance(state, StarState):
                if any(match(nxt, text) for nxt in state.next_states):
                    return True
                if text and state.checking_state.check_self(text[0]):
                    if match(state, text[1:]):
                        return True
                return False

            if not text:
                return False

            if isinstance(state, PlusState):
                if state.checking_state.check_self(text[0]):
                    if match(state, text[1:]):
                        return True
                    if any(match(nxt, text[1:]) for nxt in state.next_states):
                        return True
                return False

            if state.check_self(text[0]):
                return any(match(nxt, text[1:]) for nxt in state.next_states)

            return False

        return match(self.curr_state, string)


if __name__ == "__main__":
    regex_pattern = "a*4.+hi"
    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))
    print(regex_compiled.check_string("4uhi"))
    print(regex_compiled.check_string("meow"))
