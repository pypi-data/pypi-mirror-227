from personal_assistant.sort import sorter_starter
from personal_assistant.addressbook import addressbook_starter
from personal_assistant.notes import notes_main as notes_starter
from new_ABC import RichCommands
from abc import ABC, abstractmethod


class Telegram:
    def __init__(self, token):
        self.token = token
    
    def send_message(self, text):
        print(f"Send {text} to Telegram")

class ConsoleOutputAbstract(ABC):
    @abstractmethod
    def output(self, text: str) -> None:
        pass

class TerminalOutput(ConsoleOutputAbstract):
    def output(self, text: str) -> None:
        print(text)

class TelegramOutput(ConsoleOutputAbstract):
    def __init__(self, token) -> None:
        self.telegram_client = Telegram(token)
    
    def output(self, text: str) -> None:
        self.telegram_client.send_message(text)

class Commands_Handler:
    def __init__(self, command_output: ConsoleOutputAbstract):
        self.__output_processor = command_output
        
    def send_message(self, message) -> None:
        self.__output_processor.output(message)
    
    def execute_function(self, function_number):
        if function_number == 1:
            print("ADDress book")
            addressbook_starter()
        elif function_number == 2:
            print("Note book")
            notes_starter()
        elif function_number == 3:
            print("Sorter")
            sorter_starter()
        else:
            self.send_message("Invalid function number")

def menu():

    output_choice = input("Choose output type (1 - Console, 2 - Telegram): ")
        
    if output_choice == "1":
        output_processor = TerminalOutput()
    elif output_choice == "2":
        telegram_token = input("Enter your Telegram token: ")
        output_processor = TelegramOutput(telegram_token)
    else:
        print("Invalid choice")
        return

    commands_handler = Commands_Handler(output_processor)

    while True:
        
        main = RichCommands()
        main.main_menu()
        

        user_input = input(">>> ")
        if user_input in ["1", "2", "3"]:
            function_number = int(user_input)
            commands_handler.execute_function(function_number)
        elif user_input == '0' or user_input.lower() == "exit":
            print('\nGoodbye!\n')
            break
        else:
            commands_handler.send_message("\nWrong number... Try again...\n")

        # if user_input == '1':
        #     print("\n✨ AddressBook Started! ✨\n")

        #     addressbook_starter()
        # elif user_input == '2':
        #     print("\n✨ NoteBook Started! ✨\n")

        #     notes_starter()
        # elif user_input == '3':
        #     print("\n✨ Files Sorter Started! ✨\n")

        #     result = sorter_starter()
        #     print(result)
        # elif user_input == '0' or user_input.lower() == "exit":
        #     print('\nGoodbye!\n')
        #     break
        # else:
        #     imput_console = Console()
        #     text = "  Wrong number... Try again..."
        #     panel = Panel(text,width=35)
        #     imput_console.print(panel)


if __name__ == '__main__':
    menu()
