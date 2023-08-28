import argparse
import zipfile
import tarfile
import os

# Text Manipulation Functions
def load_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def count_word_occurrences(text, target_word):
    return text.lower().count(target_word.lower())

def replace_word(text, old_word, new_word):
    return text.replace(old_word, new_word)

def count_words(text):
    words = text.split()
    return len(words)

def count_lines(text):
    lines = text.split("\n")
    return len(lines)

def count_characters(text):
    return len(text)

def convert_to_lower(text):
    return text.lower()

def convert_to_upper(text):
    return text.upper()

# Compression Functions
def compress_zip(input_filename):
    with zipfile.ZipFile(input_filename + '.zip', 'w') as zipf:
        zipf.write(input_filename)

def compress_tar(input_filename, use_gzip):
    compression_mode = 'w:gz' if use_gzip else 'w'
    with tarfile.open(input_filename + '.tar' + ('.gz' if use_gzip else ''), compression_mode) as tarf:
        tarf.add(input_filename)

# Todo List Functions
def add_task(task_list, task):
    task_list.append(task)
    save_tasks(task_list)
    print(f"Added task: {task}")

def remove_task(task_list, task_index):
    if 0 <= task_index < len(task_list):
        removed_task = task_list.pop(task_index)
        print(f"Removed task: {removed_task}")
        save_tasks(task_list)
    else:
        print("Invalid task index")

def list_tasks(task_list):
    if not task_list:
        print("No tasks in the list.")
    else:
        print("Tasks:")
        for idx, task in enumerate(task_list):
            print(f"{idx}: {task}")

def save_tasks(task_list):
    with open("tasks.txt", "w") as file:
        file.write("\n".join(task_list))

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

def main():
    parser = argparse.ArgumentParser(description="Python CLI Utility")
    parser.add_argument("mode", choices=["text", "compress", "todo"], help="Choose mode: text, compress, or todo")
    args, remaining_args = parser.parse_known_args()

    if args.mode == "text":
        # Text Manipulation Mode
        print("Text Manipulation Mode")
        text_parser = argparse.ArgumentParser(description="Text Manipulation Utility", prog='script.py text')
        text_parser.add_argument("--input", help="Input text file for manipulation")

        group = text_parser.add_mutually_exclusive_group()
        group.add_argument("-w", "--words", action="store_true", help="Count words")
        group.add_argument("-l", "--lines", action="store_true", help="Count lines")
        group.add_argument("-c", "--characters", action="store_true", help="Count characters")
        group.add_argument("--lower", action="store_true", help="Convert text to lowercase")
        group.add_argument("--upper", action="store_true", help="Convert text to uppercase")
        group.add_argument("--count-word", help="Count occurrences of a specific word")
        group.add_argument("--replace", nargs=2, help="Replace occurrences of a word with another word")

        text_args = text_parser.parse_args(remaining_args)

        if text_args.input:
            try:
                text = load_file(text_args.input)
            except FileNotFoundError:
                print("Error: File not found.")
                return
        else:
            text = input("Enter the text: ")

        if text_args.words:
            count = count_words(text)
            print("Word Count:", count)
        elif text_args.lines:
            count = count_lines(text)
            print("Line Count:", count)
        elif text_args.characters:
            count = count_characters(text)
            print("Character Count:", count)
        elif text_args.lower:
            converted_text = convert_to_lower(text)
            print("Converted Text (Lowercase):\n", converted_text)
        elif text_args.upper:
            converted_text = convert_to_upper(text)
            print("Converted Text (Uppercase):\n", converted_text)
        elif text_args.count_word:
            word = text_args.count_word
            count = count_word_occurrences(text, word)
            print(f"'{word}' appears {count} times in the text.")
        elif text_args.replace:
            old_word, new_word = text_args.replace
            replaced_text = replace_word(text, old_word, new_word)
            print("Replaced Text:\n", replaced_text)
        else:
            print("Please specify an option: -w, -l, -c, --lower, --upper, --count-word, or --replace")

    elif args.mode == "compress":
        # Compression Mode
        print("Compression Mode")
        input_file = input("Enter the path of the file to compress: ")
        if not os.path.exists(input_file):
            print("Error: The specified input file does not exist.")
            return
        compression_format = input("Enter compression format (zip or tar): ")
        if compression_format == "zip":
            compress_zip(input_file)
            print(f"{input_file} has been compressed to {input_file}.zip")
        elif compression_format == "tar":
            use_gzip = input("Use gzip compression for TAR format (yes or no): ").lower() == "yes"
            compress_tar(input_file, use_gzip)
            if use_gzip:
                print(f"{input_file} has been compressed to {input_file}.tar.gz")
            else:
                print(f"{input_file} has been compressed to {input_file}.tar")
        else:
            print("Error: Invalid compression format. Please choose 'zip' or 'tar'.")


    elif args.mode == "todo":
        # Todo List Manager Mode
        print("Todo List Manager Mode")

        todo_parser = argparse.ArgumentParser(description="Todo List Manager", prog='script.py todo')
        todo_parser.add_argument("action", choices=["add", "remove", "list"], help="Action to perform on the todo list")
        todo_args, todo_remaining_args = todo_parser.parse_known_args(remaining_args)

        task_list = load_tasks()

        if todo_args.action == "add":
            task = input("Enter the task description: ")
            add_task(task_list, task)
        elif todo_args.action == "remove":
            list_tasks(task_list)
            try:
                index = int(input("Enter the index of the task to remove: "))
                remove_task(task_list, index)
            except ValueError:
                print("Invalid index")
        elif todo_args.action == "list":
            list_tasks(task_list)
        else:
            print("Invalid action")


    else:
        print("Invalid mode. Please choose 'text', 'compress', or 'todo'.")

if __name__ == "__main__":
    main()
