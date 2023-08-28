# SBS-Utility

[![PyPI version](https://badge.fury.io/py/SBS-Utility.svg)](https://badge.fury.io/py/SBS-Utility)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A versatile command-line utility for text manipulation, compression, and task management.

## Features

- Text manipulation: Count words, lines, characters; convert to lowercase/uppercase; replace words; and more.
- Compression: Create ZIP or TAR archives with optional gzip compression.
- Todo List Manager: Add, remove, and list tasks in a todo list.

## Installation

You can install the utility using `pip`:

```bash
pip install SBS-Utility
``` 

## Usage

### Text Manipulation Mode

```bash
SBS-Utility text --input input.txt --words
SBS-Utility text --input input.txt --lines
SBS-Utility text --input input.txt --characters
SBS-Utility text --input input.txt --lower
SBS-Utility text --input input.txt --upper
SBS-Utility text --input input.txt --count-word target_word
SBS-Utility text --input input.txt --replace old_word new_word
```

### Compression Mode

```bash
SBS-Utility compress
```

### Todo List Manager Mode

```bash
SBS-Utility todo add "Task description"
SBS-Utility todo remove task_index
SBS-Utility todo list
```

## Example

- Count words in a text file:

```bash
SBS-Utility text --input sample.txt --words
```

- Create a compressed ZIP archive:

```bash
SBS-Utility compress
```

- Add a task to the todo list:

```bash
SBS-Utility todo add "Complete project proposal"
```


## LICENSE

This project is licensed under the MIT License - see the LICENSE file for details


