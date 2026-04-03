<h1 align="center">Easy Grok Chat Exporter 📝</h1>

![Easy Grok Chat Exporter Logo](Grok%20Easy%20Chat%20Exporter%20Image.png)

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg)](https://github.com/Owlock/easy-grok-chat-exporter)
> **The only Grok exporter that extracts AI thinking traces.** Convert your Grok conversations into clean Markdown, Text, or JSONL files — with optional step-by-step AI reasoning included. Zero dependencies, interactive CLI.
---
## Why this tool is different
Every other Grok exporter only saves the final response. **Easy Grok Chat Exporter is the only tool that can also extract Grok's internal thinking process** — the hidden step-by-step reasoning the AI used before answering you.
| Feature | Easy Grok Chat Exporter | Others |
|---|---|---|
| **Extracts AI thinking traces** | ✅ Yes | ❌ No |
| Processes `prod-grok-backend.json` directly | ✅ Yes | ❌ No |
| Interactive terminal menu | ✅ Yes | ❌ No |
| Multi-format (Markdown, Text, JSONL) | ✅ Yes | ⚠️ Partial |
| No browser extension needed | ✅ Yes | ❌ No |
| Bilingual docs (EN/ES) | ✅ Yes | ❌ No |
---
## What are AI Thinking Traces?
When Grok answers a question, it first goes through an internal reasoning process — analyzing the question, considering approaches, and planning its response. This process is called **thinking traces** and is stored inside the `prod-grok-backend.json` file that Grok sends you.
**Most exporters ignore this data. We don't.**
### Why include thinking traces?
- **Understand Grok's reasoning** — See exactly how the AI arrived at each answer
- **Import full context into other AIs** — Give another AI model not just the conversation, but also the reasoning behind each response
- **Study AI thought patterns** — Analyze how AI models think through complex problems
- **Keep a complete archive** — Preserve every layer of your AI interactions
- **Debug AI behavior** — Identify where reasoning went wrong in incorrect answers
---
## Quick Overview
This tool takes the JSON file that Grok sends you when you request your data export and converts each conversation into clean, readable files. You can choose to include or exclude Grok's **internal thinking process** — the step-by-step reasoning the AI used before answering you.
---
## Step-by-Step Guide
### Step 1: Request Your Data from Grok
1. Go to [grok.com](https://grok.com) or [x.com/i/grok](https://x.com/i/grok)
2. Open your **Account Settings** or **Data & Privacy** section
3. Look for the option to **Request your data** or **Export conversations**
4. Submit the request. Grok will process it and send you an email with a download link.
> This may take a few minutes to a few hours depending on how many conversations you have.
---
### Step 2: Download and Extract the ZIP File
1. Check your email for a message from Grok/xAI with the subject containing
   something like "Your data export is ready"
2. Click the download link in the email
3. You will receive a **.zip file** containing several files
4. **Extract/unzip** the file to a folder on your computer
> **Windows:** Right-click the .zip file → "Extract All..." → Choose a folder → Click "Extract"
>
> **macOS:** Double-click the .zip file → It extracts automatically
>
> **Linux:** Run `unzip filename.zip` in the terminal
---
### Step 3: Locate the `prod-grok-backend.json` File
After extracting the ZIP, you will see several files inside. Look for the file named:
prod-grok-backend.json
This is the file that contains **all your Grok conversations** in JSON format.
It's the most important file for this tool.
> **Note:** The ZIP may contain other files like images, attachments, or other JSON
> files. You only need `prod-grok-backend.json` for this tool.
---
### Step 4: Download This Tool
1. **Download** the `grok_exporter.py` file from this repository
2. Create a new folder on your computer (for example:
   `C:\Users\YourName\Grok-Export` on Windows or `~/Grok-Export` on macOS/Linux)
3. Place **both** files in that folder:
   - `grok_exporter.py` (this tool)
   - `prod-grok-backend.json` (your Grok data)
Your folder should look like this:
Grok-Export/
├── grok_exporter.py
└── prod-grok-backend.json
---
### Step 5: Run the Tool
#### Option A: Interactive Mode (Recommended for beginners)
Open your terminal/command prompt, navigate to the folder, and run:
```bash
python grok_exporter.py -i
The tool will guide you through a series of questions:
1. Path to JSON file — Press Enter if prod-grok-backend.json is in the same
   folder, or type the full path
2. Output format — Choose:
   - 1 = Markdown (.md) — Best for reading and documentation
   - 2 = Plain Text (.txt) — Universal, works everywhere
   - 3 = JSON Lines (.jsonl) — Best for importing into other AI models
   - 4 = All formats — Get everything
3. Include AI thinking traces? — Choose:
   - 1 = No (only final responses)
   - 2 = Yes (include Grok's step-by-step reasoning)
That's it! Your exported files will appear in the same folder.
---
Option B: Command Line (For advanced users)
# Export to Markdown (default)
python grok_exporter.py prod-grok-backend.json -md
# Export to Markdown WITH thinking traces
python grok_exporter.py prod-grok-backend.json -md -t
# Export to Plain Text
python grok_exporter.py prod-grok-backend.json -txt
# Export to JSON Lines (best for AI import)
python grok_exporter.py prod-grok-backend.json -jsonl
# Export ALL formats WITH thinking traces
python grok_exporter.py prod-grok-backend.json -all -t
# Specify a custom output directory
python grok_exporter.py prod-grok-backend.json -all -t -o ./my-exported-chats
---
Command Reference
Flag	Description
-i, --interactive	Interactive mode with step-by-step questions
-md, --markdown	Export to Markdown format
-txt, --text	Export to Plain Text format
-jsonl, --jsonlines	Export to JSON Lines format
-all, --all-formats	Export to all formats at once
-t, --thinking	Include AI thinking traces in the output
-o, --output-dir	Specify output directory
---
Output Examples
Markdown (with thinking traces enabled)
When you use the -t flag, each Grok response includes a collapsible thinking section:
# My Conversation Title
**Chat ID:** abc-123-xyz
---
<details>
<summary>🧠 AI Thinking Process</summary>
Thinking about your request...
- Step 1: Analyze the user's question
- Step 2: Consider possible approaches
- Step 3: Select the best solution
</details>
**Grok:**
Here is my answer based on the reasoning above...
---
JSON Lines (for AI import)
Each line is a complete message with optional thinking:
{"sender": "user", "message": "How do I sort a list in Python?", "create_time": "2025-01-15T10:30:00Z", "model": "grok-3", "thinking": ""}
{"sender": "assistant", "message": "You can use the sorted() function...", "create_time": "2025-01-15T10:30:05Z", "model": "grok-3", "thinking": "User is asking about Python list sorting. Common approaches: sorted(), .sort(), list comprehension..."}
---
## Importing into Other AI Models
The **JSON Lines (.jsonl)** format is specifically designed to be easily imported
into other AI models or chat systems. Each line contains:
- `sender` — Who sent the message (user or assistant)
- `message` — The message content
- `create_time` — When the message was sent
- `model` — Which Grok model was used
- `thinking` — Grok's internal reasoning (if `-t` was used)
This structured format makes it easy to:
- Feed conversations into other AI models for context
- Build a personal knowledge base
- Analyze conversation patterns
- Migrate to other platforms
---
Requirements
- Python 3.6 or higher — No additional packages needed!
- Works on Windows, macOS, and Linux
- Zero dependencies — Just Python and the standard library
---
Troubleshooting
"File not found" error
Make sure prod-grok-backend.json is in the same folder as grok_exporter.py,
or provide the full path to the file.
"Invalid JSON format" error
Make sure you are using the correct file. It must be named exactly
prod-grok-backend.json and come from the Grok data export ZIP.
Output files are empty
Some conversations may have empty titles or no messages. These are automatically
skipped. Check the export report at the end to see how many were processed.
Non-ASCII characters in filenames
The tool automatically removes emojis and non-ASCII characters from filenames to
prevent errors on all operating systems.
---
License
MIT License — Free to use, modify, and distribute. See LICENSE (LICENSE) for details.
---
Contributing
Found a bug? Have a feature request? Open an
issue (https://github.com/Owlock/easy-grok-chat-exporter/issues) or submit a
pull request (https://github.com/Owlock/easy-grok-chat-exporter/pulls).
---
Made with ❤️ for the Grok community
4. Baja al final y dale **"Commit changes..."** → **"Commit changes"**
