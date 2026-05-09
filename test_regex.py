from regex import RegexFSM

def run_demo():
    demo_cases = {
        "a*4.+hi": ["aaaaaa4uhi", "4uhi", "4xxxhi", "meow", "4hi"],
        "c.t": ["cat", "c7t", "ct"],
        "ab+c": ["abc", "abbbc", "ac"]
    }

    for pattern, test_strings in demo_cases.items():
        print(f"\nRegular expression: '{pattern}'")
        fsm = RegexFSM(pattern)

        for text in test_strings:
            result = fsm.check_string(text)
            status = "accepted" if result else "declined"
            print(f"String: '{text:<15}' -> {status}")

def run_interactive():

    try:
        user_pattern = input("\nEnter a regular (Enter to exit): ")
        if not user_pattern:
            return

        user_fsm = RegexFSM(user_pattern)
        print(f"Authomata for '{user_pattern}' compiled.")

        while True:
            user_text = input("Enter a string (or 'exit'): ")
            if user_text.lower() == 'exit':
                break

            res = user_fsm.check_string(user_text)
            status = "accepted" if res else "declined"
            print(f"Result expression: {status}\n")

    except KeyboardInterrupt:
        print("\nexiting.")

if __name__ == "__main__":
    # run_demo()
    run_interactive()
