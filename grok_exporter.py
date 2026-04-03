import os
import json
import re
import sys
import argparse
from datetime import datetime

def safe_filename(title):
    """
    Return a sanitized version of 'title' for filenames.
    Removes non-ASCII characters (including emojis),
    then replaces typical forbidden characters with '_'.
    """
    title = re.sub(r'[^\x00-\x7F]+', '', title)
    return re.sub(r'[\\/*?:"<>|]', '_', title).strip()

def extract_thinking_text(traces):
    """Extract and format thinking traces from Grok responses."""
    if not traces:
        return ""
    
    thinking_parts = []
    
    if isinstance(traces, list):
        for trace in traces:
            if isinstance(trace, dict):
                text = trace.get('thinking_trace', '')
                if text:
                    thinking_parts.append(text)
            elif isinstance(trace, str):
                thinking_parts.append(trace)
    elif isinstance(traces, dict):
        text = traces.get('thinking_trace', '')
        if text:
            thinking_parts.append(text)
    elif isinstance(traces, str):
        thinking_parts.append(traces)
    
    return '\n\n'.join(thinking_parts) if thinking_parts else ""

def format_thinking_for_markdown(thinking_text):
    """Format thinking text for markdown output."""
    if not thinking_text:
        return ""
    
    lines = []
    lines.append("<details>")
    lines.append("<summary>🧠 AI Thinking Process</summary>")
    lines.append("")
    lines.append("```")
    lines.append(thinking_text)
    lines.append("```")
    lines.append("")
    lines.append("</details>")
    lines.append("")
    
    return '\n'.join(lines)

def format_thinking_for_text(thinking_text):
    """Format thinking text for plain text output."""
    if not thinking_text:
        return ""
    
    lines = []
    lines.append("=" * 60)
    lines.append("AI THINKING PROCESS:")
    lines.append("=" * 60)
    lines.append(thinking_text)
    lines.append("=" * 60)
    lines.append("")
    
    return '\n'.join(lines)

def process_conversation(conv, include_thinking=False):
    """Process a single Grok conversation and return formatted content."""
    if not isinstance(conv, dict) or 'conversation' not in conv or 'responses' not in conv:
        return None
    
    conv_data = conv['conversation']
    chat_id = conv_data.get('id', 'unknown')
    title = conv_data.get('title', '') or ''
    create_time = conv_data.get('create_time', '')
    responses = conv['responses']
    
    if not title or not responses:
        return None
    
    title_sanitized = safe_filename(title)
    if not title_sanitized:
        return None
    
    return {
        'chat_id': chat_id,
        'title': title,
        'title_sanitized': title_sanitized,
        'create_time': create_time,
        'responses': responses,
        'include_thinking': include_thinking
    }

def convert_to_markdown(processed_conv, output_dir):
    """Convert processed conversation to markdown file."""
    if not processed_conv:
        return False
    
    title_sanitized = processed_conv['title_sanitized']
    chat_id = processed_conv['chat_id']
    create_time = processed_conv['create_time']
    include_thinking = processed_conv['include_thinking']
    responses = processed_conv['responses']
    
    filename = os.path.join(output_dir, f"{title_sanitized}.md")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {processed_conv['title']}\n\n")
            f.write(f"**Chat ID:** {chat_id}\n\n")
            if create_time:
                f.write(f"**Created:** {create_time}\n\n")
            f.write("---\n\n")
            
            for resp_wrapper in responses:
                resp = resp_wrapper.get('response', {})
                if not isinstance(resp, dict) or 'sender' not in resp:
                    continue
                
                sender = resp.get('sender', 'unknown')
                message = resp.get('message', '')
                
                if include_thinking:
                    thinking_traces = resp.get('agent_thinking_traces', [])
                    thinking_text = extract_thinking_text(thinking_traces)
                    if thinking_text:
                        f.write(format_thinking_for_markdown(thinking_text))
                
                if message:
                    f.write(f"**{sender}:**\n\n{message}\n\n")
                
                f.write("---\n\n")
        
        return True
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        return False

def convert_to_text(processed_conv, output_dir):
    """Convert processed conversation to plain text file."""
    if not processed_conv:
        return False
    
    title_sanitized = processed_conv['title_sanitized']
    chat_id = processed_conv['chat_id']
    create_time = processed_conv['create_time']
    include_thinking = processed_conv['include_thinking']
    responses = processed_conv['responses']
    
    filename = os.path.join(output_dir, f"{title_sanitized}.txt")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {processed_conv['title']}\n")
            f.write(f"Chat ID: {chat_id}\n")
            if create_time:
                f.write(f"Created: {create_time}\n")
            f.write("=" * 60 + "\n\n")
            
            for resp_wrapper in responses:
                resp = resp_wrapper.get('response', {})
                if not isinstance(resp, dict) or 'sender' not in resp:
                    continue
                
                sender = resp.get('sender', 'unknown')
                message = resp.get('message', '')
                
                if include_thinking:
                    thinking_traces = resp.get('agent_thinking_traces', [])
                    thinking_text = extract_thinking_text(thinking_traces)
                    if thinking_text:
                        f.write(format_thinking_for_text(thinking_text))
                
                if message:
                    f.write(f"{sender}:\n\n{message}\n\n")
                
                f.write("-" * 60 + "\n\n")
        
        return True
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        return False

def convert_to_jsonl(processed_conv, output_dir):
    """Convert processed conversation to JSON Lines file."""
    if not processed_conv:
        return False
    
    title_sanitized = processed_conv['title_sanitized']
    include_thinking = processed_conv['include_thinking']
    responses = processed_conv['responses']
    
    filename = os.path.join(output_dir, f"{title_sanitized}.jsonl")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for resp_wrapper in responses:
                resp = resp_wrapper.get('response', {})
                if not isinstance(resp, dict):
                    continue
                
                line_data = {
                    'sender': resp.get('sender', 'unknown'),
                    'message': resp.get('message', ''),
                    'create_time': resp.get('create_time', ''),
                    'model': resp.get('model', '')
                }
                
                if include_thinking:
                    thinking_traces = resp.get('agent_thinking_traces', [])
                    thinking_text = extract_thinking_text(thinking_traces)
                    line_data['thinking'] = thinking_text
                
                f.write(json.dumps(line_data, ensure_ascii=False) + '\n')
        
        return True
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        return False

def load_conversations(json_file):
    """Load and validate Grok conversations from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict) or 'conversations' not in data:
            print(f"Error: JSON file '{json_file}' does not contain Grok conversations format.")
            return None
        
        return data['conversations']
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file}'.")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def interactive_menu():
    """Display interactive menu and get user choices."""
    print("=" * 60)
    print("Grok Chat History Exporter")
    print("=" * 60)
    print()
    
    # Ask for JSON file path
    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prod-grok-backend.json')
    json_file = input(f"Path to Grok conversations JSON file\n[default: {default_path}]: ").strip()
    if not json_file:
        json_file = default_path
    
    if not os.path.exists(json_file):
        print(f"Error: File '{json_file}' not found.")
        sys.exit(1)
    
    print()
    print("Select output format:")
    print("1. Markdown (.md)")
    print("2. Plain Text (.txt)")
    print("3. JSON Lines (.jsonl)")
    print("4. All formats")
    choice = input("Enter choice [1-4] (default: 1): ").strip()
    
    formats = []
    if choice == '2':
        formats = ['txt']
    elif choice == '3':
        formats = ['jsonl']
    elif choice == '4':
        formats = ['md', 'txt', 'jsonl']
    else:
        formats = ['md']
    
    print()
    print("Include AI thinking traces?")
    print("1. No (only final responses)")
    print("2. Yes (include thinking process)")
    thinking_choice = input("Enter choice [1-2] (default: 1): ").strip()
    include_thinking = thinking_choice == '2'
    
    return json_file, formats, include_thinking

def main():
    parser = argparse.ArgumentParser(description='Grok Chat History Exporter')
    parser.add_argument('json_file', nargs='?', help='Path to Grok conversations JSON file')
    parser.add_argument('-o', '--output-dir', help='Output directory (default: script directory)')
    parser.add_argument('-md', '--markdown', action='store_true', help='Export to Markdown')
    parser.add_argument('-txt', '--text', action='store_true', help='Export to Plain Text')
    parser.add_argument('-jsonl', '--jsonlines', action='store_true', help='Export to JSON Lines')
    parser.add_argument('-all', '--all-formats', action='store_true', help='Export to all formats')
    parser.add_argument('-t', '--thinking', action='store_true', help='Include AI thinking traces')
    parser.add_argument('-i', '--interactive', action='store_true', help='Use interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive or not args.json_file:
        json_file, formats, include_thinking = interactive_menu()
    else:
        json_file = args.json_file
        include_thinking = args.thinking
        
        if args.all_formats:
            formats = ['md', 'txt', 'jsonl']
        elif args.text:
            formats = ['txt']
        elif args.jsonlines:
            formats = ['jsonl']
        else:
            formats = ['md']
    
    output_dir = args.output_dir or os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    
    conversations = load_conversations(json_file)
    if not conversations:
        sys.exit(1)
    
    total = len(conversations)
    processed = 0
    skipped = 0
    
    print()
    print(f"Processing {total} conversations...")
    print(f"Output formats: {', '.join(formats)}")
    print(f"Include thinking: {'Yes' if include_thinking else 'No'}")
    print()
    
    for conv in conversations:
        processed_conv = process_conversation(conv, include_thinking)
        if not processed_conv:
            skipped += 1
            continue
        
        for fmt in formats:
            if fmt == 'md':
                success = convert_to_markdown(processed_conv, output_dir)
            elif fmt == 'txt':
                success = convert_to_text(processed_conv, output_dir)
            elif fmt == 'jsonl':
                success = convert_to_jsonl(processed_conv, output_dir)
            else:
                success = False
            
            if success:
                processed += 1
            else:
                skipped += 1
    
    print("--- Export Report ---")
    print(f"Total conversations: {total}")
    print(f"Successfully exported: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
