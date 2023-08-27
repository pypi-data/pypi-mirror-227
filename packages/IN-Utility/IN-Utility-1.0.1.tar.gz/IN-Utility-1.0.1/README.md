# Your Utility Name

[![PyPI version](https://badge.fury.io/py/IN-utility.svg)](https://badge.fury.io/py/your-utility)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A versatile command-line utility for text manipulation, compression, and task management.

## Features

- Text manipulation: Count words, lines, characters; convert to lowercase/uppercase; replace words; and more.
- Compression: Create ZIP or TAR archives with optional gzip compression.
- Todo List Manager: Add, remove, and list tasks in a todo list.

## Installation

You can install the utility using `pip`:

```bash
pip install your-utility
``` 

## Usage

### Text Manipulation Mode

```bash
your-utility text --input input.txt --words
your-utility text --input input.txt --lines
your-utility text --input input.txt --characters
your-utility text --input input.txt --lower
your-utility text --input input.txt --upper
your-utility text --input input.txt --count-word target_word
your-utility text --input input.txt --replace old_word new_word
```

### Compression Mode

```bash
your-utility compress
```

### Todo List Manager Mode

```bash
your-utility todo add "Task description"
your-utility todo remove task_index
your-utility todo list
```

## Example

- Count words in a text file:

```bash
your-utility text --input sample.txt --words
```

- Create a compressed ZIP archive:

```bash
your-utility compress
```

- Add a task to the todo list:

```bash
your-utility todo add "Complete project proposal"
```


## LICENSE

This project is licensed under the MIT License - see the LICENSE file for details


