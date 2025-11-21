---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

**TL;DR**: Learn how to use Notion as your CMS for a Hugo/GitHub Pages website. Write in Notion's beautiful editor, hit publish, and watch your content automatically sync to your site. No manual exports, no copy-pasting, just pure automation magic.

### The Problem with Traditional Static Sites

I love static sites. They're fast, secure, and basically free to host. But let's be honest—writing directly in Markdown files gets old fast.

You're sitting at your desk, ready to write that brilliant blog post. You open VS Code, create a new `.md` file, manually type out the front matter, and then... you want to add an image. Time to save the file, move the image to `static/img/`, reference it correctly, check the preview, realize you got the path wrong, fix it, rinse, repeat.

And forget about writing on your phone. Good luck editing Markdown on a 6-inch screen while waiting for your coffee.

### Enter Notion: Your New Best Friend

Notion changes everything. It's got a gorgeous editor, works beautifully on mobile, handles images like a dream, and makes organizing content actually enjoyable. Plus, database views mean you can see your blog posts in a calendar, kanban board, or good old-fashioned table.

The only problem? Notion isn't a static site generator. Your Hugo site can't read Notion pages directly.

**But what if it could?**

That's exactly what we're building today.

### What You'll Build

By the end of this guide, you'll have:

- 📝 A Notion database where you write and manage all your content

- 🔄 Automatic syncing to your GitHub repository

- 🚀 New posts going live on your site within minutes

- 📱 The ability to publish from anywhere (yes, even your phone)

- 🎨 All of Hugo's power with all of Notion's convenience

The best part? Once it's set up, you literally never think about it again. Write in Notion, toggle a "Published" status, and your site updates automatically.

### Prerequisites

Before we dive in, make sure you have:

- A Hugo site deployed to GitHub Pages (check out [my previous tutorial](https://claude.ai/chat/9aaa2f5b-1611-47b6-8be7-ea9e36ff09d8#) if you need help with this)

- A Notion account (free plan works perfectly)

- Basic familiarity with GitHub Actions

- About 30 minutes to set everything up

### Part 1: Setting Up Your Notion Workspace

#### Creating Your Content Database

First, let's build the Notion database that will power your blog.

**Step 1: Create a new page in Notion**

I like to keep mine in a "Website" section of my workspace, but put it wherever makes sense for you.

**Step 2: Add a database**

Click the `/` menu and select "Table - Inline" (or full page if you prefer).

**Step 3: Set up your properties**

Here's the structure I use, refined over months of actually using this system:

**Why these specific properties?**

- **Status**: Lets you control exactly when posts go live

- **Slug**: Gives you control over URLs (crucial for SEO)

- **Description**: Hugo needs this for meta tags

- **Tags/Category**: Hugo uses these for organization

- **Featured**: Nice to have for highlighting your best work

**Pro tip**: Start simple. You can always add properties later. The only truly required ones are Name, Status, and Published Date.

#### Creating Your First Post

Let's create a test post to make sure everything works:

1. Click **"+ New"** in your database

1. Set **Name**: "Test Post from Notion"

1. Set **Status**: Published

1. Set **Published Date**: Today

1. Set **Slug**: test-post-from-notion

1. Set **Description**: "Testing my Notion integration"

1. Add a tag: "test"

Now write some content in the page body. Try different formatting:

- Headers

- **Bold** and *italic* text

- Bullet lists

- Code blocks

- Images

This will help us verify the sync handles everything correctly.

#### Database Views (Optional but Awesome)

One of Notion's superpowers is multiple views of the same data. Try adding:

**Calendar View**: See your publishing schedule

- Click "Add a view" → Calendar

- Group by Published Date

**Kanban Board**: Track post status

- Add view → Board

- Group by Status

**Gallery View**: Visual overview with featured images

- Add view → Gallery

- Customize preview

Suddenly, content management becomes actually enjoyable.

### Part 2: Creating Your Notion Integration

Now we need to give our GitHub Action permission to read from Notion.

#### Step 1: Create the Integration

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)

1. Click **"+ New integration"**

1. Fill out the form:

1. Click **"Submit"**

#### Step 2: Copy Your Token

You'll see a section called "Integration Token" (previously "Internal Integration Token").

Click **"Show"** and then **"Copy"**.

Your token will start with `ntn_` and look like this:

```plain text
ntn_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

```

**Important**: Treat this like a password. Don't commit it to Git, don't share it publicly, don't post it in Discord. We'll store it securely in GitHub Secrets in a moment.

#### Step 3: Give the Integration Access

This is the step everyone forgets, and it's the #1 cause of "400 Bad Request" errors.

1. Go back to your Notion database

1. Click the **"..."** menu (top right)

1. Scroll down to **"Connections"**

1. Click **"Add connections"**

1. Select "GitHub Pages Sync" (your integration)

You should see a small badge appear showing the integration is connected.

**Why is this necessary?** Notion is security-first. Even though you created the integration, it doesn't automatically have access to your pages. You have to explicitly share each database.

#### Step 4: Get Your Database ID

Open your database in full-page view and look at the URL:

```plain text
https://www.notion.so/GitHub-Sync-2a4cae697a1080aeba80d51b75251c50?pvs=94

```

The database ID is the 32-character code:

```plain text
2a4cae697a1080aeba80d51b75251c50

```

Copy this—we'll need it next.

### Part 3: Setting Up GitHub Secrets

Let's store your Notion credentials securely in GitHub.


---

## Troubleshooting Guide

Even with careful setup, you might encounter issues. This section covers common problems and their solutions.

### Common Synchronization Issues

#### Issue 1: Post Status Set to "Published" But Not Syncing

**Symptoms:**
- Changed post status to "Published" in Notion
- Post doesn't appear on your Hugo site after waiting
- No errors visible in GitHub Actions

**Possible Causes & Solutions:**

1. **Integration Not Connected to Database**
   - Go to your Notion database
   - Click the "..." menu → "Connections"
   - Verify your integration appears in the list
   - If not, click "Add connections" and select it

2. **Wrong Database ID**
   - Verify the database ID in GitHub Secrets matches your actual database
   - Get the ID from the URL when viewing your database
   - Update `NOTION_DATABASE_ID` secret if incorrect

3. **GitHub Actions Not Running**
   - Go to your repository → Actions tab
   - Check if the workflow is enabled
   - Look for any recent runs and their status
   - Try manually triggering the workflow

4. **Post Properties Missing**
   - Ensure your post has all required fields:
     - Title (required)
     - Status = "Published" (required)
     - Date (recommended)
     - Slug (auto-generated if missing)

#### Issue 2: Posts Not Syncing At All

**Symptoms:**
- No posts appearing despite multiple published items
- Workflow runs but creates no files

**Diagnosis Steps:**

1. **Enable Verbose Logging**
   ```bash
   # Run locally with verbose output
   export VERBOSE=true
   python scripts/notion-sync.py --verbose
   ```

2. **Check Health Status**
   - The script now includes automatic health checks
   - Look for these messages in logs:
     - ✓ Authentication successful
     - ✓ Database accessible
     - ✓ All required properties present

3. **Run Dry-Run Mode**
   ```bash
   # Preview what would be synced
   python scripts/notion-sync.py --dry-run --verbose
   ```

**Common Solutions:**

- **401 Unauthorized**: Token is invalid or expired
  - Regenerate your Notion integration token
  - Update `NOTION_TOKEN` in GitHub Secrets

- **403 Forbidden**: Integration lacks database access
  - Share the database with your integration in Notion
  - Wait a few minutes and try again

- **404 Not Found**: Database ID is incorrect
  - Double-check the database ID from the Notion URL
  - Ensure you're using the database ID, not a page ID

#### Issue 3: Some Posts Sync, Others Don't

**Symptoms:**
- Only certain posts appear on the site
- Inconsistent synchronization behavior

**Check These:**

1. **Status Property**
   - Verify the Status property is exactly "Published" (case-sensitive)
   - Check for typos or extra spaces

2. **Property Names**
   - Ensure database properties match expected names:
     - "Title" not "Name"
     - "Date" not "Published Date"
     - "Status" not "Publication Status"

3. **Content Format**
   - Check if problematic posts have unusual formatting
   - Look for unsupported block types
   - Review logs for conversion errors

### Adjusting Sync Frequency

The default sync runs every hour. You can customize this:

#### Method 1: Edit Workflow File

Edit `.github/workflows/notion-sync.yml`:

```yaml
schedule:
  # Choose one:
  - cron: '*/30 * * * *'    # Every 30 minutes
  - cron: '0 */2 * * *'     # Every 2 hours  
  - cron: '0 */6 * * *'     # Every 6 hours
  - cron: '0 0 * * *'       # Daily at midnight
  - cron: '0 9 * * 1-5'     # Weekdays at 9am
```

**Common Cron Patterns:**
- `*/15 * * * *` - Every 15 minutes
- `0 * * * *` - Every hour
- `0 */4 * * *` - Every 4 hours
- `0 0,12 * * *` - Twice daily (midnight & noon)
- `0 8 * * *` - Daily at 8am

#### Method 2: Manual Trigger

For immediate updates:

1. Go to repository → Actions → "Sync Notion to Hugo"
2. Click "Run workflow"
3. Optionally enable:
   - **Verbose logging**: See detailed output
   - **Dry run**: Preview changes without applying

### Using Verbose Logging

Enable detailed logging to diagnose issues:

#### Local Testing

```bash
# Set environment variable
export VERBOSE=true
export NOTION_TOKEN="your-token"
export NOTION_DATABASE_ID="your-db-id"

# Run with verbose flag
python scripts/notion-sync.py --verbose

# Combine with dry-run
python scripts/notion-sync.py --verbose --dry-run
```

#### In GitHub Actions

1. Go to Actions → "Sync Notion to Hugo"
2. Click "Run workflow"
3. Check "Enable verbose logging"
4. Review detailed logs in the workflow run

**What Verbose Logging Shows:**
- Authentication details
- Database connection status
- Each post being processed
- Property extraction details
- File creation/update operations
- API retry attempts
- Detailed error messages

### Advanced Troubleshooting

#### Configure Retry Behavior

Adjust how the script handles API failures:

```bash
# Set environment variables
export MAX_RETRIES=5          # Default: 3
export RETRY_DELAY=3          # Default: 2 seconds

python scripts/notion-sync.py
```

In GitHub workflow:

```yaml
- name: Run Notion sync
  env:
    MAX_RETRIES: 5
    RETRY_DELAY: 3
```

#### Check Sync Statistics

After each sync, the script outputs detailed statistics:

```
📊 Statistics:
   Created: 2    # New posts added
   Updated: 1    # Existing posts modified
   Deleted: 0    # Posts removed (unpublished)
   Errors:  0    # Failed operations
   Duration: 3.5s
```

**Interpreting Stats:**
- **High errors**: Check API connectivity and tokens
- **No updates**: Posts might already be in sync
- **Unexpected deletions**: Verify post statuses in Notion
- **Slow duration**: Consider rate limiting or large content

#### Database Schema Verification

The health check verifies your database structure:

**Required Properties:**
- Title (title)
- Status (select)
- Date (date)

**Optional But Recommended:**
- Slug (text)
- Description (text)
- Tags (multi-select)
- Category (select)

**Missing Properties:**
The script will warn about missing properties but continue syncing.

### Getting Help

If you're still stuck:

1. **Enable verbose logging** and capture full output
2. **Run health check** to identify configuration issues
3. **Check GitHub Actions logs** for detailed error messages
4. **Review recent commits** in your sync history

**Useful Commands:**

```bash
# Full diagnostic run
python scripts/notion-sync.py --verbose --dry-run

# Test connectivity only
python -c "
import requests
token = 'your-token'
response = requests.get(
    'https://api.notion.com/v1/users/me',
    headers={'Authorization': f'Bearer {token}', 'Notion-Version': '2022-06-28'}
)
print(response.status_code, response.json())
"

# View recent sync commits
git log --oneline --grep="Sync from Notion" -10
```

### Best Practices

1. **Test with dry-run first** before enabling automatic sync
2. **Use verbose logging** during initial setup
3. **Start with hourly sync**, adjust frequency based on needs
4. **Monitor first few syncs** to catch configuration issues
5. **Keep integration token secure** - never commit to repository
6. **Back up your database** before making structural changes

---

