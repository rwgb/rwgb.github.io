---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 2)"
date: 2025-11-21
description: "How to setup Notion sync with GitHub Pages (Part 2)"
tags: ['hugo', 'github-pages', 'github-actions', 'web-development', 'tutorial']
categories: ["Uncategorized"]
draft: false
---

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/d389e5cc-1652-4095-afc8-bc6f33661856/9691f333-16af-4374-a0ee-44f1dab95d52.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QOMIE2FX%2F20260227%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260227T091658Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHAaCXVzLXdlc3QtMiJHMEUCIQCM8NX0Uv1XCtwJoV7k%2BMYzeCGcxVHqtpeCOVXlywE1XQIgDB0nd8OJfhkkmVluAlNF1vb0IblMrgyy7BpgluSFvzEq%2FwMIORAAGgw2Mzc0MjMxODM4MDUiDCRPn%2FUxJLGhiW1FGyrcA1GSQ8W8NHlg1ulNXQpIP0rKJH69lHVwyFDabdrN0noSp87sCSWkr8IQd9nzBClKsQsmenTywr4MEDYJeJhPF0i0c7AvgbJ2skYnMB1IJ1ZyrJny34LAhFsCwdQUkLmnU%2B%2F9hDBIBuy0n7CqCM4dKnY7gk%2BdIZ1%2Ff6a4yrbuNdzhc%2Fs5gWDo1EvQc2bHXq7s3sOBwPXK%2FUAnOOAKj8%2BkMz8LDxMN9mCHNiQy2FFzmfYRjrxUSNGS6pmJEJVYWrl0uu6ZKwXT6xHYe1aLlCwUUuM%2BmYfu9jic5OmaZilkd6KrHZQiJTlb3dqJ8bBKQfPBxL7LbXX0cf%2BPil8Sm6tUGPnRIQq2DR9xJ%2BMkl5TxWdpbqa4ZHmtzmPtAVeCk8G8AbHMufysomf0rOL4H3x3Fb%2FGnuxr8VG0qMbdTsARyOlXat%2BMf6vywaCAKq2yjfOw7R%2B7rRGJgUrvQ27q0Yru4WyyHso56h6iZaDNBjtMbVnHv10O4cm9b6Y6tqVpJ6EBA6iYxq9V6K5328o0FkOM8a28VtvQht4i6TZ2y5lKWm6izvRktnAcTuX2ud%2BdCjHZt%2FG6NnYRqXa744R%2BgVd8XGkEJI8E1CK4KZoJzTAcaKc%2BTkEuCWk05wLwHhC4eMLOahc0GOqUBXlMcGDirlTt9i4MvASq4VveEgOW1YljtpTgfSiwxdLINPFyMnnPIvi%2Fw0oNWay44uFKLmtyQ%2BoPEbN5zWgT7MPKJRVeqy2irdfJIw3lFk3FCguuTHItEcyKmRPaEwBe2YhftIESXDP1BS7DUmAhlHacoyT5%2B1Ge73pKRgW7ZCozY55LSpgRsVBFzTv99jUofAXR2I9j7VvE5TNgJbAsdbyRaZWsf&X-Amz-Signature=2a734d6b3e4eb7f5321fdc6673ee0ce214280c6a66030cca8a6a96016c428fdf&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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
