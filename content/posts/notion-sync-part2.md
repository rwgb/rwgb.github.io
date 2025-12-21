---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 2)"
date: 2025-11-21
description: "How to setup Notion sync with GitHub Pages (Part 2)"
tags: ['hugo', 'github-pages', 'github-actions', 'web-development', 'tutorial']
categories: ["Uncategorized"]
draft: false
---

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/d389e5cc-1652-4095-afc8-bc6f33661856/9691f333-16af-4374-a0ee-44f1dab95d52.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662XAFVF26%2F20251221%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251221T043628Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEA0aCXVzLXdlc3QtMiJHMEUCIANQfuvikcXe4yL%2FiytuNWnKtsRP6e7m3%2Fu7uyfTn5wMAiEAibik6bskQGxPE0MRdgaowaYdWg0pCpd6VwGc4sTMhSsqiAQI1f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDDReiw8FcQl5dma%2BrircA5JzMtUynC4dDRxKGOSY3gUOVSe6SY7YlcElId10CSTgOZOH2ygQm0a3VnBRQUlNL%2F25N%2F17lnntxNGK%2F8acmHA6AbvozBsAjOf1Q7IYj9qFzS%2BrbY3AbC6ISqeWyRJvFVMpO%2FVGTRXOG9WCMVHHyQHn0msza30IcD3dLpKPUoa%2FOLZawosfW8CaZA7xkqtbLbW5aiGKcDvzu0eHeN13x1IdKzBYtEANpJnSt6S5fDgpm%2FKHXZQDd7kNLbUYIIAqF7AkaiuGUTshJ6mhKRqEM3tlQX1xw%2FEi22730sENs%2FjFU86%2BJOxpJ%2BJeSkJfmva9Fzfj%2B%2FGr4nFoE%2Bxbfhmsm%2FAfq2jNuXUuZUf2UEoS0WuyKXmt5iqmz4fDyaeMo0p1dWgHkyQo6qyQFCgfbmAZlnABc94ZXlLc5KCPty%2FS5ybQGOMCX5%2B6nDJMHcb4PSt6DWcMPvBbdNDd2BysEAMaTzTRt9vEHua2PzNfF%2FIIwmls63JwJ2u2ic2X6%2Fl99U2jUqfZFDM2CtHOGokyHOHH6a2oUjhrIqzxGfYzn1EaYDCRhbL2EJNe3r8NB3SimjGsFJCOBZ091Hr%2Fh5xdxv43hMwp8Nw%2By54GwGJBQqZSdyGljFEL9T8Bq7Vy2E1yMP7tncoGOqUBOUsN6m4YR9OqSU%2BbjWqfV40wiCOF5k8wvKeEpKDApDTFR%2BjVRJ1nf5tqDW1VES0K8apYFAaQUD5LjVUcNren20r4JJLwd4wwbXhKvO5mhPHWqu7JLXcO90cf6zDOE3Vq3UtWrMY%2Brwr%2BEAMK3PHKEIaflDDeJ0xOhtULhcEz8SuO0xwpKfOTBseYtu4s2YWSVWQ1DuNrLI6%2BKZpcpUXJ1aswrAlU&X-Amz-Signature=47bfd7a30f2d7c10a16def4b97806a071fc0e624eac75fcd40fab68f6c303a53&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

### Part 3: Setting Up GitHub Secrets

Let's store your Notion credentials securely in GitHub.

#### Step 1: Open Your Repository Settings

1. Go to your GitHub repository (rwgb.github.io)

1. Click **Settings** (top menu)

1. Click **Secrets and variables** → **Actions** (left sidebar)

#### Step 2: Add Your Secrets

Click **"New repository secret"** and add these two:

**First Secret:**

- Name: `NOTION_TOKEN`

- Value: Your integration token (ntn_...)

**Second Secret:**

- Name: `NOTION_DATABASE_ID`

- Value: Your database ID (32 characters)

These secrets are encrypted and only accessible to your GitHub Actions. Perfect for sensitive data.

### Part 4: Creating the Sync Script

Now for the fun part—the Python script that converts Notion pages to Hugo markdown.

#### Step 1: Create the Script Directory

In your repository, create a `scripts` folder:

```bash
mkdir scripts
cd scripts

```

#### Step 2: Create the Sync Script

Create `scripts/notion-sync.py`:

```python
#!/usr/bin/env python3
"""
Sync Notion database to Hugo markdown files
Converts Notion blocks to Hugo-compatible markdown
"""

import os
import re
import requests
from datetime import datetime
from pathlib import Path

# Configuration from environment variables
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
OUTPUT_DIR = 'content/posts'

# Notion API setup
NOTION_API = 'https://api.notion.com/v1'
HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}

def query_database():
    """Fetch all published posts from Notion"""
    url = f'{NOTION_API}/databases/{DATABASE_ID}/query'

    # Only fetch published posts
    data = {
        'filter': {
            'property': 'Status',
            'select': {
                'equals': 'Published'
            }
        },
        'sorts': [
            {
                'property': 'Published Date',
                'direction': 'descending'
            }
        ]
    }

    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()['results']

def get_page_content(page_id):
    """Fetch all blocks from a Notion page"""
    url = f'{NOTION_API}/blocks/{page_id}/children'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()['results']

def notion_to_markdown(blocks):
    """Convert Notion blocks to markdown"""
    markdown = []

    for block in blocks:
        block_type = block['type']

        # Paragraph
        if block_type == 'paragraph':
            text = rich_text_to_markdown(block['paragraph']['rich_text'])
            if text.strip():
                markdown.append(f'{text}\n')

        # Headings
        elif block_type == 'heading_1':
            text = rich_text_to_markdown(block['heading_1']['rich_text'])
            markdown.append(f'## {text}\n')

        elif block_type == 'heading_2':
            text = rich_text_to_markdown(block['heading_2']['rich_text'])
            markdown.append(f'### {text}\n')

        elif block_type == 'heading_3':
            text = rich_text_to_markdown(block['heading_3']['rich_text'])
            markdown.append(f'#### {text}\n')

        # Lists
        elif block_type == 'bulleted_list_item':
            text = rich_text_to_markdown(block['bulleted_list_item']['rich_text'])
            markdown.append(f'- {text}\n')

        elif block_type == 'numbered_list_item':
            text = rich_text_to_markdown(block['numbered_list_item']['rich_text'])
            markdown.append(f'1. {text}\n')

        # Code blocks
        elif block_type == 'code':
            code = rich_text_to_markdown(block['code']['rich_text'])
            language = block['code']['language']
            markdown.append(f'```{language}\n{code}\n```\n')

        # Quotes
        elif block_type == 'quote':
            text = rich_text_to_markdown(block['quote']['rich_text'])
            markdown.append(f'> {text}\n')

        # Images
        elif block_type == 'image':
            url = block['image'].get('file', {}).get('url') or \
                  block['image'].get('external', {}).get('url')
            if url:
                caption = rich_text_to_markdown(block['image'].get('caption', []))
                alt_text = caption if caption else 'Image'
                markdown.append(f'![{alt_text}]({url})\n')

        # Divider
        elif block_type == 'divider':
            markdown.append('---\n')

    return '\n'.join(markdown)

def rich_text_to_markdown(rich_text):
    """Convert Notion rich text to markdown formatting"""
    if not rich_text:
        return ''

    result = []

    for text_obj in rich_text:
        text = text_obj['plain_text']
        annotations = text_obj['annotations']

        # Apply markdown formatting
        if annotations['bold']:
            text = f'**{text}**'
        if annotations['italic']:
            text = f'*{text}*'
        if annotations['code']:
            text = f'`{text}`'
        if annotations['strikethrough']:
            text = f'~~{text}~~'

        # Handle links
        if text_obj.get('href'):
            text = f'[{text}]({text_obj["href"]})'

        result.append(text)

    return ''.join(result)

def extract_properties(page):
    """Extract front matter properties from Notion page"""
    props = page['properties']

    # Title
    title_prop = props.get('Name') or props.get('Title')
    title = ''
    if title_prop and title_prop.get('title'):
        title = title_prop['title'][0]['plain_text']

    # Date
    date_prop = props.get('Published Date') or props.get('Date')
    date = datetime.now().isoformat()
    if date_prop and date_prop.get('date'):
        date = date_prop['date']['start']

    # Slug
    slug_prop = props.get('Slug')
    slug = ''
    if slug_prop and slug_prop.get('rich_text'):
        slug = slug_prop['rich_text'][0]['plain_text']
    if not slug:
        # Auto-generate from title
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    # Description
    desc_prop = props.get('Description')
    description = ''
    if desc_prop and desc_prop.get('rich_text'):
        description = desc_prop['rich_text'][0]['plain_text']

    # Tags
    tags_prop = props.get('Tags')
    tags = []
    if tags_prop and tags_prop.get('multi_select'):
        tags = [tag['name'] for tag in tags_prop['multi_select']]

    # Category
    cat_prop = props.get('Category')
    category = 'Uncategorized'
    if cat_prop and cat_prop.get('select'):
        category = cat_prop['select']['name']

    return {
        'title': title,
        'date': date,
        'slug': slug,
        'description': description,
        'tags': tags,
        'category': category
    }

def create_hugo_post(page_id, properties, content):
    """Create Hugo markdown file with front matter"""
    slug = properties['slug']
    filename = f"{slug}.md"
    filepath = Path(OUTPUT_DIR) / filename

    # Build front matter
    tags_str = ', '.join([f'"{tag}"' for tag in properties['tags']])

    front_matter = f"""---
title: "{properties['title']}"
date: {properties['date']}
description: "{properties['description']}"
tags: [{tags_str}]
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
    return filename

def sync():
    """Main sync function"""
    print('🔄 Syncing Notion to Hugo...\n')

    # Fetch published posts
    try:
        pages = query_database()
        print(f'Found {len(pages)} published posts\n')
    except Exception as e:
        print(f'❌ Error querying database: {e}')
        return

    synced = 0
    errors = 0

    for page in pages:
        try:
            # Extract properties
            properties = extract_properties(page)

            # Fetch content
            blocks = get_page_content(page['id'])
            content = notion_to_markdown(blocks)

            # Create Hugo post
            create_hugo_post(page['id'], properties, content)
            synced += 1

        except Exception as e:
            print(f'✗ Error processing page: {e}')
            errors += 1

    print(f'\n✅ Sync complete!')
    print(f'   Synced: {synced} posts')
    if errors > 0:
        print(f'   Errors: {errors} posts')

if __name__ == '__main__':
    # Validate environment variables
    if not NOTION_TOKEN:
        print('❌ Error: NOTION_TOKEN not set')
        exit(1)
    if not DATABASE_ID:
        print('❌ Error: NOTION_DATABASE_ID not set')
        exit(1)

    sync()

```

This script does a lot, so let's break down the key parts:

`**query_database()**`: Fetches only posts with Status = "Published"

`**notion_to_markdown()**`: Converts Notion's block format to Hugo-compatible markdown

`**extract_properties()**`: Pulls metadata to create Hugo front matter

`**create_hugo_post()**`: Writes the final .md file

#### Step 3: Create Requirements File

Create `scripts/requirements.txt`:

```plain text
requests==2.31.0

```

That's it—we only need one dependency!

### Part 5: Creating the GitHub Action

Now we'll automate everything with GitHub Actions.

#### Create the Workflow File

Create `.github/workflows/notion-sync.yml`:

```yaml
name: Sync Notion to Hugo

on:
  # Run every hour
  schedule:
    - cron: '0 * * * *'

  # Allow manual trigger
  workflow_dispatch:

  # Run when this workflow changes
  push:
    paths:
      - '.github/workflows/notion-sync.yml'
      - 'scripts/notion-sync.py'

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r scripts/requirements.txt

      - name: Run Notion sync
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
        run: |
          python scripts/notion-sync.py

      - name: Check for changes
        id: verify_diff
        run: |
          git diff --quiet content/posts/ || echo "changed=true" >> $GITHUB_OUTPUT

      - name: Commit and push if changed
        if: steps.verify_diff.outputs.changed == 'true'
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add content/posts/
          git commit -m "🔄 Sync from Notion"
          git push

```

**What this workflow does:**

1. **Runs every hour** checking for new/updated posts

1. **Can be triggered manually** for immediate syncs

1. **Pulls your code** including the Hugo theme

1. **Installs Python** and dependencies

1. **Runs the sync script** with your Notion credentials

1. **Commits changes** if new posts were added

1. **Triggers Hugo rebuild** automatically (your existing workflow)

### Part 6: Testing Everything

Time for the moment of truth!

#### Step 1: Commit Everything

```bash
git add scripts/ .github/workflows/
git commit -m "Add Notion sync integration"
git push origin main

```

#### Step 2: Manual Trigger

Don't wait an hour—let's test now:

1. Go to **Actions** tab in GitHub

1. Click **"Sync Notion to Hugo"**

1. Click **"Run workflow"** → **"Run workflow"**

1. Watch it run (takes about 30 seconds)

#### Step 3: Check the Results

If everything worked:

1. **Check the Actions log** for the ✓ symbols

1. **Look at your repository** for new files in `content/posts/`

1. **Wait 2-3 minutes** for Hugo to rebuild

1. **Visit your site** and see your new post!

### Troubleshooting Common Issues

#### "400 Bad Request" Error

**Cause**: Integration doesn't have database access

**Fix**:

1. Open Notion database

1. Click "..." → "Add connections"

1. Select your integration

#### "401 Unauthorized" Error

**Cause**: Token is wrong or expired

**Fix**:

1. Check GitHub Secrets

1. Regenerate token in Notion if needed

1. Update the secret

#### Posts Not Syncing

**Checklist**:

- ✓ Status = "Published" in Notion?

- ✓ Database ID correct?

- ✓ Integration has access?

- ✓ Check Actions tab for errors

#### Images Not Showing

**Issue**: Notion image URLs expire after a while

**Solutions**:

1. **Use external images** (upload to Imgur, Cloudinary, etc.)

1. **Download images to repo** (modify script to download)

1. **Accept temporary URLs** (good enough for most use cases)

### Your New Publishing Workflow

Here's what publishing looks like now:

#### On Desktop:

1. Open Notion

1. Write your post

1. Set Status to "Published"

1. Done. (Seriously, that's it)

#### On Mobile:

1. Open Notion app

1. Create new entry in database

1. Write using voice-to-text while walking your dog

1. Hit "Published"

1. Post is live within an hour
