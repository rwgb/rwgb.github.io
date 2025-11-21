#!/usr/bin/env python3
"""
Sync Notion database to Hugo markdown files with enhanced logging and error handling
"""

import os
import re
import sys
import json
import time
import logging
import argparse
import requests
from datetime import datetime
from pathlib import Path
from functools import wraps
from typing import Optional, Dict, List, Set

# Configuration
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
VERBOSE = os.environ.get('VERBOSE', 'false').lower() == 'true'
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', '3'))
RETRY_DELAY = int(os.environ.get('RETRY_DELAY', '2'))

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

# Setup logging
def setup_logging(verbose: bool = False):
    """Configure logging with appropriate level"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

logger = setup_logging(VERBOSE)

# Sync statistics
class SyncStats:
    """Track sync statistics"""
    def __init__(self):
        self.created = 0
        self.updated = 0
        self.deleted = 0
        self.errors = 0
        self.start_time = time.time()
    
    def duration(self):
        return time.time() - self.start_time
    
    def summary(self):
        return {
            'created': self.created,
            'updated': self.updated,
            'deleted': self.deleted,
            'errors': self.errors,
            'duration_seconds': round(self.duration(), 2)
        }

stats = SyncStats()

# Retry decorator
def retry_on_failure(max_attempts: int = MAX_RETRIES, delay: int = RETRY_DELAY):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(f"Attempting {func.__name__} (attempt {attempt}/{max_attempts})")
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait_time = delay * (2 ** (attempt - 1))
                        logger.warning(f"{func.__name__} failed (attempt {attempt}), retrying in {wait_time}s: {str(e)}")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                except Exception as e:
                    logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                    raise
            
            raise last_exception
        return wrapper
    return decorator

def health_check() -> bool:
    """Verify Notion API connectivity and permissions"""
    logger.info("🏥 Running health check...")
    
    try:
        # Check authentication
        logger.debug("Checking authentication...")
        url = f'{NOTION_API}/users/me'
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        user = response.json()
        logger.info(f"✓ Authentication successful (User: {user.get('name', 'Unknown')})")
        
        # Check database access
        logger.debug(f"Checking database access (ID: {DATABASE_ID})...")
        url = f'{NOTION_API}/databases/{DATABASE_ID}'
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        db = response.json()
        logger.info(f"✓ Database accessible: {db.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        
        # Check if database has required properties
        logger.debug("Verifying database schema...")
        properties = db.get('properties', {})
        required = ['Title', 'Status', 'Date']
        missing = [prop for prop in required if prop not in properties]
        
        if missing:
            logger.warning(f"⚠️  Missing recommended properties: {', '.join(missing)}")
        else:
            logger.info("✓ All required properties present")
        
        logger.info("✅ Health check passed\n")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Health check failed: {str(e)}")
        if hasattr(e.response, 'status_code'):
            if e.response.status_code == 401:
                logger.error("   → Invalid NOTION_TOKEN. Check your secret configuration.")
            elif e.response.status_code == 404:
                logger.error("   → Database not found. Verify DATABASE_ID is correct.")
            elif e.response.status_code == 403:
                logger.error("   → Integration lacks access. Share the database with your integration.")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during health check: {str(e)}")
        return False

@retry_on_failure()
def query_database():
    """Fetch all published posts from Notion"""
    logger.debug(f"Querying database {DATABASE_ID}...")
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
    
    response = requests.post(url, headers=HEADERS, json=data, timeout=30)
    response.raise_for_status()
    results = response.json()['results']
    logger.info(f"Found {len(results)} published posts")
    return results

@retry_on_failure()
def get_page_content(page_id: str):
    """Fetch page content blocks"""
    logger.debug(f"Fetching content for page {page_id[:8]}...")
    url = f'{NOTION_API}/blocks/{page_id}/children'
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()['results']

def notion_to_markdown(blocks: List[Dict]) -> str:
    """Convert Notion blocks to Markdown"""
    logger.debug(f"Converting {len(blocks)} blocks to markdown...")
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

def extract_properties(page: Dict) -> Dict:
    """Extract properties from Notion page"""
    props = page['properties']
    page_id = page['id']
    
    logger.debug(f"Extracting properties for page {page_id[:8]}...")
    
    # Title
    title = props['Title']['title'][0]['plain_text'] if props['Title']['title'] else 'Untitled'
    
    # Date
    date = props.get('Date', {}).get('date', {}).get('start', datetime.now().isoformat())
    
    # Slug
    slug = props.get('Slug', {}).get('rich_text', [{}])[0].get('plain_text')
    if not slug:
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        logger.debug(f"Generated slug from title: {slug}")
    
    # Description
    description = props.get('Description', {}).get('rich_text', [{}])[0].get('plain_text', '')
    
    # Tags
    tags = [tag['name'] for tag in props.get('Tags', {}).get('multi_select', [])]
    
    # Category
    category = props.get('Category', {}).get('select', {}).get('name', 'Uncategorized')
    
    result = {
        'title': title,
        'date': date,
        'slug': slug,
        'description': description,
        'tags': tags,
        'category': category
    }
    
    logger.debug(f"Properties: title='{title}', slug='{slug}', tags={tags}")
    return result

def create_hugo_post(page_id: str, properties: Dict, content: str, dry_run: bool = False) -> str:
    """Create Hugo markdown file"""
    slug = properties['slug']
    filename = f"{slug}.md"
    filepath = Path(OUTPUT_DIR) / filename
    
    # Check if file exists (update vs create)
    is_update = filepath.exists()
    
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
    
    if dry_run:
        action = "Would update" if is_update else "Would create"
        logger.info(f"[DRY RUN] {action}: {filename}")
        return filename
    
    # Write file
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(content)
        
        if is_update:
            logger.info(f'✓ Updated: {filename}')
            stats.updated += 1
        else:
            logger.info(f'✓ Created: {filename}')
            stats.created += 1
        
        return filename
    except Exception as e:
        logger.error(f"Failed to write {filename}: {str(e)}")
        stats.errors += 1
        raise

def sync(dry_run: bool = False):
    """Main sync function"""
    logger.info('🔄 Starting Notion to Hugo sync...')
    logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")
    
    # Run health check
    if not health_check():
        logger.error("❌ Health check failed. Aborting sync.")
        sys.exit(1)
    
    # Fetch published posts
    try:
        pages = query_database()
        logger.info(f'📚 Processing {len(pages)} published posts\n')
    except Exception as e:
        logger.error(f"Failed to query database: {str(e)}")
        stats.errors += 1
        sys.exit(1)
    
    # Track synced files
    synced_files: Set[str] = set()
    
    for i, page in enumerate(pages, 1):
        page_id = page['id']
        try:
            logger.debug(f"Processing page {i}/{len(pages)}: {page_id[:8]}...")
            
            # Extract properties
            properties = extract_properties(page)
            
            # Fetch content
            blocks = get_page_content(page_id)
            content = notion_to_markdown(blocks)
            
            # Create Hugo post
            slug = properties['slug']
            filename = f"{slug}.md"
            synced_files.add(filename)
            create_hugo_post(page_id, properties, content, dry_run=dry_run)
            
        except Exception as e:
            logger.error(f'✗ Error processing page {page_id[:8]}: {str(e)}')
            stats.errors += 1
            continue
    
    # Remove posts that are no longer published
    logger.info("\n🗑️  Checking for posts to remove...")
    output_path = Path(OUTPUT_DIR)
    if output_path.exists():
        deleted_count = 0
        for existing_file in output_path.glob('*.md'):
            if existing_file.name not in synced_files:
                if dry_run:
                    logger.info(f'[DRY RUN] Would remove: {existing_file.name}')
                else:
                    try:
                        existing_file.unlink()
                        logger.info(f'🗑️  Removed: {existing_file.name}')
                        stats.deleted += 1
                        deleted_count += 1
                    except Exception as e:
                        logger.error(f"Failed to delete {existing_file.name}: {str(e)}")
                        stats.errors += 1
        
        if deleted_count == 0 and not dry_run:
            logger.info("No posts to remove")
    
    # Print summary
    summary = stats.summary()
    logger.info('\n' + '='*60)
    logger.info('✅ Sync complete!')
    logger.info('='*60)
    logger.info(f"📊 Statistics:")
    logger.info(f"   Created: {summary['created']}")
    logger.info(f"   Updated: {summary['updated']}")
    logger.info(f"   Deleted: {summary['deleted']}")
    logger.info(f"   Errors:  {summary['errors']}")
    logger.info(f"   Duration: {summary['duration_seconds']}s")
    logger.info('='*60)
    
    # Return non-zero exit code if there were errors
    if stats.errors > 0:
        logger.warning(f"⚠️  Completed with {stats.errors} error(s)")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sync Notion database to Hugo markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Normal sync
  python notion-sync.py
  
  # Dry run (preview changes without making them)
  python notion-sync.py --dry-run
  
  # Verbose logging
  python notion-sync.py --verbose
  
  # Combination
  python notion-sync.py --dry-run --verbose

Environment Variables:
  NOTION_TOKEN       - Notion integration token (required)
  NOTION_DATABASE_ID - Database ID to sync (required)
  VERBOSE            - Enable verbose logging (true/false, default: false)
  MAX_RETRIES        - Maximum retry attempts for API calls (default: 3)
  RETRY_DELAY        - Initial retry delay in seconds (default: 2)
        """
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without actually creating/updating/deleting files'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Override VERBOSE setting if --verbose flag is used
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Validate environment variables
    if not NOTION_TOKEN:
        logger.error("❌ NOTION_TOKEN environment variable is required")
        sys.exit(1)
    
    if not DATABASE_ID:
        logger.error("❌ NOTION_DATABASE_ID environment variable is required")
        sys.exit(1)
    
    try:
        sync(dry_run=args.dry_run)
    except KeyboardInterrupt:
        logger.info("\n⚠️  Sync interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)