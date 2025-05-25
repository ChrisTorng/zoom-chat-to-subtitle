# About

This repo is a fork from [rasyidev/zoom-chat-to-subtitle](https://github.com/rasyidev/zoom-chat-to-subtitle), but fixes the timing issue and adds some Traditional Chinese enhancements.

# Zoom Chat to Subtitle
Convert Zoom's saved meeting chat (txt) into subtitle file (srt). Using this tool, the recorded Zoom Video can be played along with the chat as a subtitle.
![](https://raw.githubusercontent.com/ChrisTorng/zoom-chat-to-subtitle/main/demo-zoom-chat-to-subtitle.gif)

## Installation

### Clone This Repository

```
git clone https://github.com/ChrisTorng/zoom-chat-to-subtitle.git
```

### Change Directory to The Project
```
cd zoom-chat-to-subtitle
```

## Usage

**FORMAT**: `python main.py <file_path.txt> [start_time] [-o <output_path>] [-l <language>]`

### Parameters

- `<file_path.txt>`  
  Required. Path to the Zoom chat text file.

- `[start_time]`  
  Optional. Meeting start time in format `h:m:s.f` (e.g., `19:31:15`).  
  If not provided, the program will automatically extract the start time from the parent folder name (e.g., `19.30.36` format).  
  If both are unavailable, the program will display an error and exit.

- `-o, --output-path <output_path>`  
  Optional. Specify the output SRT file path. File extension must be `.srt`.  
  If not specified, defaults to the same name as the input file.

- `-l, --language <language>`  
  Optional. Language code for message translation. Supports `zh-tw` (Traditional Chinese).  
  - Default: English (no translation)
  - When `zh-tw` is specified, specific English patterns in messages will be translated to Chinese:
    - `"Replying to "` → `"回覆 "`
    - `"Reacted to "*" with ?"` → `"對 "*" 比 ?"`

### Examples

```bash
# Basic usage with automatic folder time detection
python main.py "meeting_saved_chat.txt"

# Specify meeting start time
python main.py "meeting_saved_chat.txt" 19:31:15

# Specify output file
python main.py "meeting_saved_chat.txt" -o "output.srt"

# Enable Traditional Chinese translation
python main.py "meeting_saved_chat.txt" -l zh-tw

# Combine all options
python main.py "meeting_saved_chat.txt" 19:31:15 -o "output.srt" -l zh-tw
```

## Time Processing Mechanism

- The program calculates subtitle timestamps by subtracting the meeting start time (obtained from `[start_time]` parameter or folder name) from each message timestamp.
- If the meeting start time cannot be determined automatically and is not manually specified, the program will stop and display an error message.

## Supported File Types

- Input: `.txt` chat log files only
- Output: `.srt` subtitle files only

## Customization

To modify translation rules, refer to the `translate_message` function in `module/ZoomChat2Srt.py`.


