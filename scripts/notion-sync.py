#!/usr/bin/env python3
"""
Sync Notion database to Hugo markdown files
"""

import os
import re
import requests
from datetime import datetime
from pathlib import Path

# Configuration
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
# OUTPUT_DIR is relative to the script directory
OUTPUT_DIR = SCRIPT_DIR / '../content/posts'

NOTION_API = 'https://api.notion.com/v1'
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

def query_database():
    """Fetch all published posts from Notion"""
    url = f'{NOTION_API}/databases/{DATABASE_ID}/query'
    
    # Filter for published posts only
    data = {
        'filter': {
            'property': 'Status',
            'select': {
                'equals': 'Published'
            }
        },
        'sorts': [
            {
                'property': 'Date',
                'direction': 'descending'
            }
        ]
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()['results']

def get_page_content(page_id):
    """Fetch page content blocks"""
    url = f'{NOTION_API}/blocks/{page_id}/children'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()['results']

def notion_to_markdown(blocks):
    """Convert Notion blocks to Markdown"""
    markdown = []
    
    for block in blocks:
        block_type = block['type']
        
        if block_type == 'paragraph':
            text = rich_text_to_markdown(block['paragraph']['rich_text'])
            markdown.append(f'{text}\n')
        
        elif block_type == 'heading_1':
            text = rich_text_to_markdown(block['heading_1']['rich_text'])
            markdown.append(f'## {text}\n')
        
        elif block_type == 'heading_2':
            text = rich_text_to_markdown(block['heading_2']['rich_text'])
            markdown.append(f'### {text}\n')
        
        elif block_type == 'heading_3':
            text = rich_text_to_markdown(block['heading_3']['rich_text'])
            markdown.append(f'#### {text}\n')
        
        elif block_type == 'bulleted_list_item':
            text = rich_text_to_markdown(block['bulleted_list_item']['rich_text'])
            markdown.append(f'- {text}\n')
        
        elif block_type == 'numbered_list_item':
            text = rich_text_to_markdown(block['numbered_list_item']['rich_text'])
            markdown.append(f'1. {text}\n')
        
        elif block_type == 'code':
            code = rich_text_to_markdown(block['code']['rich_text'])
            language = block['code']['language']
            markdown.append(f'```{language}\n{code}\n```\n')
        
        elif block_type == 'quote':
            text = rich_text_to_markdown(block['quote']['rich_text'])
            markdown.append(f'> {text}\n')
        
        elif block_type == 'image':
            url = block['image'].get('file', {}).get('url') or block['image'].get('external', {}).get('url')
            markdown.append(f'![Image]({url})\n')
    
    return '\n'.join(markdown)

def rich_text_to_markdown(rich_text):
    """Convert Notion rich text to markdown"""
    result = []
    
    for text_obj in rich_text:
        text = text_obj['plain_text']
        annotations = text_obj['annotations']
        
        if annotations['bold']:
            text = f'**{text}**'
        if annotations['italic']:
            text = f'*{text}*'
        if annotations['code']:
            text = f'`{text}`'
        if annotations['strikethrough']:
            text = f'~~{text}~~'
        
        if text_obj.get('href'):
            text = f'[{text}]({text_obj["href"]})'
        
        result.append(text)
    
    return ''.join(result)

def extract_properties(page):
    """Extract properties from Notion page"""
    props = page['properties']
    
    # Title
    title = props['Title']['title'][0]['plain_text'] if props['Title']['title'] else 'Untitled'
    
    # Date
    date = props.get('Date', {}).get('date', {}).get('start', datetime.now().isoformat())
    
    # Slug
    slug = props.get('Slug', {}).get('rich_text', [{}])[0].get('plain_text')
    if not slug:
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    # Description
    description = props.get('Description', {}).get('rich_text', [{}])[0].get('plain_text', '')
    
    # Tags
    tags = [tag['name'] for tag in props.get('Tags', {}).get('multi_select', [])]
    
    # Category
    category = props.get('Category', {}).get('select', {}).get('name', 'Uncategorized')
    
    return {
        'title': title,
        'date': date,
        'slug': slug,
        'description': description,
        'tags': tags,
        'category': category
    }

def create_hugo_post(page_id, properties, content):
    """Create Hugo markdown file"""
    slug = properties['slug']
    filename = f"{slug}.md"
    filepath = Path(OUTPUT_DIR) / filename
    
    # Create front matter
    front_matter = f"""---
title: "{properties['title']}"
date: {properties['date']}
description: "{properties['description']}"
tags: {properties['tags']}
categories: ["{properties['category']}"]
draft: false
---

"""
    
    # Write file
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(content)
    
    print(f'✓ Created: {filename}')

def sync():
    """Main sync function"""
    print('🔄 Syncing Notion to Hugo...\n')
    
    # Fetch published posts
    pages = query_database()
    print(f'Found {len(pages)} published posts\n')
    
    # Track synced files
    synced_files = set()
    
    for page in pages:
        try:
            # Extract properties
            properties = extract_properties(page)
            
            # Fetch content
            blocks = get_page_content(page['id'])
            content = notion_to_markdown(blocks)
            
            # Create Hugo post
            slug = properties['slug']
            filename = f"{slug}.md"
            synced_files.add(filename)
            create_hugo_post(page['id'], properties, content)
            
        except Exception as e:
            print(f'✗ Error processing {page["id"]}: {e}')
    
    # Remove posts that are no longer published
    output_path = Path(OUTPUT_DIR)
    if output_path.exists():
        for existing_file in output_path.glob('*.md'):
            if existing_file.name not in synced_files:
                existing_file.unlink()
                print(f'🗑️  Removed: {existing_file.name}')
    
    print(f'\n✅ Sync complete!')

if __name__ == '__main__':
    sync()