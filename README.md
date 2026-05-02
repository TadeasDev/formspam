# Google Form Spammer Tool

A Python terminal tool for sending repeated submissions to a Google Form for testing, demos, and educational use.

## Created by TadeasDev

This tool lets you enter the URL of a public Google Form and configure how the answers should be filled before sending repeated submissions. You can manually choose answers for each question, or use preset random text from `texts.txt` so the tool can submit different premade words or phrases automatically.

It is designed to be simple enough for anyone to run from the terminal: paste a form URL, choose how each question should be answered, set how many submissions you want, choose the speed, and let the script run.

## Features

- Automatic Google Form parsing for supported public forms
- Supports short text, long text, multiple choice, dropdowns, checkboxes, and linear scale questions
- Preset random text loading from `texts.txt`
- Manual static answers for controlled testing
- Random option selection for choice-based fields
- Configurable submission count
- Power setting to control submission speed
- Randomized browser user agents and request headers
- Colored terminal status output
- Success and failure counters after completion

## Requirements

- Python 3.6 or higher
- `pip`
- A public Google Form URL that does not require sign-in

Required Python packages are listed in `requirements.txt`:

```txt
requests
beautifulsoup4
colorama
```

## Installation & Usage

### One-Command Setup

If this project is hosted on GitHub, clone it and install the requirements:

#### Windows

```bash
git clone https://github.com/TadeasDev/formspam.git && cd formspam && pip install -r requirements.txt && python main.py
```

#### macOS/Linux

```bash
git clone https://github.com/TadeasDev/formspam.git && cd formspam && pip3 install -r requirements.txt && python3 main.py
```

If your repository name is different, replace the GitHub URL and folder name with the correct ones.

### Manual Setup

1. Download or copy the project files.
2. Make sure these files are in the same folder:
   - `main.py`
   - `requirements.txt`
   - `texts.txt`
3. Open a terminal or command prompt in the project folder.
4. Install the requirements and run the tool:

#### Windows

```bash
pip install -r requirements.txt
python main.py
```

#### macOS/Linux

```bash
pip3 install -r requirements.txt
python3 main.py
```

## How to Run Again

After the first setup, you do not need to reinstall the requirements every time.

#### Windows

```bash
cd formspam
python main.py
```

#### macOS/Linux

```bash
cd formspam
python3 main.py
```

## How to Use

1. Run `main.py`.
2. Enter the public Google Form URL you want to test.
3. Wait for the tool to fetch and detect the form questions.
4. For each text question, choose one of these options:
   - Random preset text from `texts.txt`
   - Manual static text
5. For each multiple choice, dropdown, or scale question, choose one of these options:
   - Random choice
   - Manual choice
6. For each checkbox question, choose one of these options:
   - Random single checkbox option
   - Manual checkbox selection by index
7. Enter how many times the form should be submitted.
8. Choose a power level from 1 to 10:
   - 1: Slowest, longer delay between submissions
   - 10: Fastest, shortest delay between submissions
9. Press `Ctrl+C` if you need to stop the tool while it is running.

## Preset Random Spam Text

The `texts.txt` file is used as the preset random answer pool for text fields. When you choose the random text option, the tool selects one value from this file for every text answer.

You can separate values with commas:

```txt
Answer one,Answer two,Answer three
```

Or with new lines:

```txt
Answer one
Answer two
Answer three
```

The tool automatically reads both formats.

## Supported Question Types

- Short answer
- Paragraph answer
- Multiple choice
- Dropdown
- Checkboxes
- Linear scale

Some special Google Form fields or restricted forms may not work, especially forms that require login, have advanced validation, or block public access.

## Disclaimer

This project is for educational and authorized testing purposes only. Use it responsibly and only on forms you own or have explicit permission to test.

Do not use this tool to ruin someone else's form, manipulate real survey results, harass people, submit unwanted responses, or cause disruption. Use common sense and do not be irresponsible with it.

The owner and author are not responsible for any misuse, damage, lost data, blocked accounts, or other consequences caused by this program. By using this tool, you accept full responsibility for your own actions.

## Attribution Requirements

You are allowed to edit this code and distribute your modified version. However, if you use any part of this code in your own projects, you must provide credit to the original author by including a reference to TadeasDev:

https://github.com/TadeasDev

## License

This project is licensed under the MIT License. Add a `LICENSE` file to the repository if you want to distribute it with the full license text.
