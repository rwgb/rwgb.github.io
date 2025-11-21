---
title: "Troubleshooting Notion to GitHub Pages Sync: A Complete Guide"
date: 2025-11-21
description: "A comprehensive troubleshooting guide for diagnosing and fixing issues with Notion to GitHub Pages synchronization"
tags: ['troubleshooting', 'notion', 'github-actions', 'hugo', 'debugging']
categories: ["Technical"]
draft: false
---

## Introduction

Setting up automated synchronization between Notion and GitHub Pages is powerful, but things can go wrong. This guide documents real-world troubleshooting steps, common issues, and proven solutions based on actual implementation experience.

### Who This Guide Is For

- You've set up Notion to GitHub Pages sync and it's not working
- Posts aren't appearing on your site after publishing
- GitHub Actions workflows are failing
- You need systematic debugging steps
- You want to prevent future issues

## Understanding the System

Before troubleshooting, let's understand the components:

### The Sync Pipeline

```
Notion Database → Notion API → Sync Script → Git Commit → Hugo Build → GitHub Pages
```

Each step can fail. We'll test them systematically.

### Required Components

1. **Notion Integration** with proper permissions
2. **GitHub Secrets** (NOTION_TOKEN, NOTION_DATABASE_ID)
3. **Sync Script** (notion-sync.py)
4. **GitHub Actions Workflow** (notion-sync.yml)
5. **Hugo Deployment Workflow** (hugo.yml)

## Diagnostic Approach

### Step 1: Verify Notion Setup

#### Check Database ID

The most common issue is an incorrect database ID.

**How to get the correct ID:**

1. Open your Notion database in **full-page view** (important!)
2. Copy the URL from your browser
3. Extract the 32-character hex code

Example URL:
```
https://www.notion.so/workspace/2a4cae697a1080eb9320d65eaa071bb1?v=...
```

Database ID: `2a4cae697a1080eb9320d65eaa071bb1`

**Common mistakes:**
- ❌ Using a page ID instead of database ID (causes 400 error)
- ❌ Copying ID with dashes in wrong places
- ❌ Including the `?v=` parameter
- ❌ Using the workspace name

**Test your database ID:**

```bash
export NOTION_TOKEN="your_token_here"
export NOTION_DATABASE_ID="your_database_id_here"

# Test query
curl -X POST "https://api.notion.com/v1/databases/${NOTION_DATABASE_ID}/query" \
  -H "Authorization: Bearer ${NOTION_TOKEN}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json"
```

**Expected response:** JSON with your posts
**Error 400:** Wrong database ID (likely a page ID)
**Error 404:** Database doesn't exist or no access

#### Check Integration Connection

**Problem:** Integration isn't connected to the database

**Solution:**
1. Open your Notion database
2. Click **"..."** menu (top right)
3. Click **"Connections"**
4. Verify your integration is listed
5. If not, click **"Add connections"** and select it

**Why this matters:** Even with a valid token, the integration needs explicit permission to access each database.

#### Verify Published Status

**Problem:** Posts aren't marked as "Published"

**Check:**
1. Open your Notion database
2. Look at the **Status** column
3. Ensure posts you want synced have Status = "Published"

**Common issues:**
- Status is "Draft" or "Ready" 
- Status property is named differently
- Status property doesn't exist

### Step 2: Test Locally

Local testing gives immediate feedback without waiting for GitHub Actions.

#### Set Environment Variables

```bash
export NOTION_TOKEN="ntn_your_token_here"
export NOTION_DATABASE_ID="your_32_char_database_id"
```

**Verify they're set:**

```bash
echo $NOTION_TOKEN
echo $NOTION_DATABASE_ID
```

#### Run Health Check

```bash
cd /path/to/your/repo
python3 scripts/notion-sync.py --verbose --dry-run
```

**What to look for:**

✅ **Success output:**
```
INFO - 🏥 Running health check...
INFO - ✓ Authentication successful (User: your_name)
INFO - ✓ Database accessible: Your Database Name
INFO - ✓ All required properties present
INFO - ✅ Health check passed
INFO - Found 4 published posts
```

❌ **Failure patterns:**

**401 Unauthorized:**
```
ERROR - ❌ Health check failed: 401 Client Error: Unauthorized
```
→ **Fix:** Token is invalid. Regenerate in Notion and update GitHub Secret.

**400 Bad Request:**
```
ERROR - ❌ Health check failed: 400 Client Error: Bad Request
```
→ **Fix:** Database ID is wrong (probably a page ID). Get the correct database ID.

**404 Not Found:**
```
ERROR - ❌ Health check failed: 404 Client Error: Not Found
```
→ **Fix:** Database doesn't exist or integration isn't connected to it.

**403 Forbidden:**
```
ERROR - ❌ Health check failed: 403 Client Error: Forbidden
```
→ **Fix:** Integration doesn't have read permissions. Check integration capabilities.

#### Test Full Sync

```bash
# Dry run first (safe - no changes)
python3 scripts/notion-sync.py --verbose --dry-run

# If dry run works, try actual sync
python3 scripts/notion-sync.py --verbose
```

**Check the output:**
- Number of posts found
- Files created/updated
- Any error messages

**Verify files created:**
```bash
ls -la content/posts/
```

You should see `.md` files matching your Notion post slugs.

### Step 3: Check GitHub Secrets

#### List Current Secrets

```bash
gh secret list
```

**Expected output:**
```
NOTION_TOKEN          Updated 2025-11-21
NOTION_DATABASE_ID    Updated 2025-11-21
```

If they're missing, add them:

```bash
# Add NOTION_TOKEN
gh secret set NOTION_TOKEN --body "ntn_your_token_here"

# Add NOTION_DATABASE_ID  
gh secret set NOTION_DATABASE_ID --body "your_database_id"
```

#### Verify Secret Values

You can't view secrets directly, but you can test them in a workflow.

**Add a test step to your workflow temporarily:**

```yaml
- name: Debug Secrets
  run: |
    echo "Token length: ${#NOTION_TOKEN}"
    echo "Database ID length: ${#NOTION_DATABASE_ID}"
    echo "Token starts with: ${NOTION_TOKEN:0:4}"
    echo "Database ID: $NOTION_DATABASE_ID"
  env:
    NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
    NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
```

**What to verify:**
- Token length should be ~50+ characters
- Token should start with `ntn_`
- Database ID should be exactly 32 characters

### Step 4: Debug GitHub Actions

#### View Workflow Runs

```bash
gh run list --workflow=notion-sync.yml --limit 5
```

Or visit: `https://github.com/your-username/your-repo/actions`

#### Get Detailed Logs

```bash
# Get the latest run ID
RUN_ID=$(gh run list --workflow=notion-sync.yml --limit 1 --json databaseId --jq '.[0].databaseId')

# View the logs
gh run view $RUN_ID --log
```

**Common workflow failures:**

**Import Error:**
```
ModuleNotFoundError: No module named 'requests'
```
→ **Fix:** Check `requirements.txt` exists and `pip install` step runs.

**Syntax Error:**
```
SyntaxError: invalid syntax
```
→ **Fix:** Python version mismatch. Ensure workflow uses Python 3.9+.

**Permission Denied:**
```
remote: Permission to user/repo.git denied
```
→ **Fix:** Workflow needs `contents: write` permission.

**No Changes to Commit:**
```
nothing to commit, working tree clean
```
→ **Fix:** This is actually fine! It means no new posts. Check Notion status filter.

### Step 5: Verify Workflow Integration

#### Check Workflow Triggers

The sync workflow should trigger the Hugo deployment. Verify:

**In `notion-sync.yml`:**
```yaml
- name: Commit changes
  run: |
    git commit -m "🔄 Sync from Notion"
    # NOT: "🔄 Sync from Notion [skip ci]"
```

**The problem:** If commit message contains `[skip ci]`, Hugo deployment won't trigger.

**The fix:** Remove `[skip ci]` from commit message.

#### Verify Hugo Workflow Runs

After sync completes:

```bash
gh run list --workflow=hugo.yml --limit 3
```

**Expected:** You should see a run triggered immediately after the sync workflow.

**If missing:**
1. Check for `[skip ci]` in commit messages
2. Verify `hugo.yml` has `push: branches: [main]` trigger
3. Check workflow permissions

### Step 6: Test End-to-End

#### Create a Test Post

1. In Notion, create a post titled "Sync Test [timestamp]"
2. Set Status = "Published"
3. Add some content
4. Note the time

#### Trigger Manual Sync

```bash
gh workflow run "Sync Notion to Hugo" --ref main
```

#### Monitor Progress

```bash
# Watch in real-time
gh run watch

# Or check status
gh run list --workflow=notion-sync.yml --limit 1
```

**Timeline:**
- Sync workflow: 20-30 seconds
- Hugo deployment: 1-2 minutes
- Total: ~3 minutes

#### Verify Results

**Check repository:**
```bash
git pull origin main
ls -la content/posts/sync-test*.md
```

**Check website:**
Visit your GitHub Pages URL after 3-5 minutes.

## Common Issues and Solutions

### Issue 1: Posts Not Syncing

**Symptoms:**
- Workflow succeeds but no new files
- "Found 0 published posts" in logs

**Diagnosis:**
```bash
python3 scripts/notion-sync.py --verbose --dry-run
```

**Common causes:**
1. **Status not "Published"** → Check Notion status column
2. **Filter case-sensitive** → Ensure exact match "Published" not "published"
3. **Wrong property name** → Script expects "Status", check your database
4. **Date filter** → Check "Published Date" is set

**Solution:**
Update your Notion database or modify the script filter:

```python
data = {
    'filter': {
        'property': 'Status',  # Match your property name
        'select': {
            'equals': 'Published'  # Match your status value
        }
    }
}
```

### Issue 2: Deployment Not Triggering

**Symptoms:**
- Sync workflow succeeds
- No Hugo deployment follows
- Changes committed but site not updated

**Diagnosis:**
Check commit message:
```bash
git log -1 --pretty=%B
```

**If you see:** `🔄 Sync from Notion [skip ci]`

**Fix:** Remove `[skip ci]` in `.github/workflows/notion-sync.yml`:

```yaml
git commit -m "🔄 Sync from Notion"
```

Then push:
```bash
git add .github/workflows/notion-sync.yml
git commit -m "fix: Remove [skip ci] to allow Hugo deployment"
git push origin main
```

### Issue 3: Images Not Appearing

**Symptoms:**
- Post syncs successfully
- Images show in markdown but not on site
- Broken image links

**Cause:** Notion image URLs are temporary (expire after ~1 hour)

**Solutions:**

**Option 1: Use External Images**
Upload images to:
- Imgur
- Cloudinary
- GitHub repository (`static/img/`)

**Option 2: Download and Store Images**
Modify sync script to download images:

```python
import urllib.request

def download_image(url, filename):
    """Download image from Notion URL"""
    img_dir = Path('static/img')
    img_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = img_dir / filename
    urllib.request.urlretrieve(url, filepath)
    
    return f'/img/{filename}'
```

### Issue 4: Rate Limiting

**Symptoms:**
- Sync works sometimes but fails randomly
- "429 Too Many Requests" errors
- Timeouts in logs

**Diagnosis:**
```bash
# Check recent error logs
gh run list --workflow=notion-sync.yml --limit 10
```

**Solution:** Add retry logic (already implemented in enhanced script):

```python
@retry_on_failure(max_retries=3, delay=5)
def query_database():
    # API call here
    pass
```

**Also consider:**
- Reduce sync frequency (hourly → every 2 hours)
- Add delays between API calls
- Cache results temporarily

### Issue 5: Missing Front Matter

**Symptoms:**
- Post appears but formatting is wrong
- Hugo throws template errors
- Missing title, date, or tags

**Diagnosis:**
Check generated markdown file:

```bash
cat content/posts/your-post.md | head -15
```

**Expected front matter:**
```yaml
---
title: "Your Post Title"
date: 2025-11-21
description: "Post description"
tags: ['tag1', 'tag2']
categories: ["Category"]
draft: false
---
```

**If missing properties:**

1. Check Notion database has required properties:
   - Name/Title
   - Published Date
   - Description (optional but recommended)
   - Tags
   - Category

2. Verify property types:
   - Status: Select
   - Tags: Multi-select
   - Category: Select
   - Published Date: Date

3. Update script property mapping if names differ

## Monitoring and Maintenance

### Set Up Notifications

Get alerts when workflows fail:

1. Go to repository **Settings** → **Notifications**
2. Enable **"Actions"**
3. Choose notification method (email, Slack, etc.)

### Regular Health Checks

Add to your routine:

```bash
# Weekly check
gh run list --workflow=notion-sync.yml --limit 10

# Look for failures
gh run list --workflow=notion-sync.yml --status failure

# Test sync manually
gh workflow run "Sync Notion to Hugo" --ref main
```

### Log Monitoring

Enable verbose logging in production:

```yaml
env:
  VERBOSE: "true"
```

Or trigger with verbose flag:
```bash
gh workflow run "Sync Notion to Hugo" --ref main -f verbose=true
```

## Prevention Best Practices

### 1. Test Before Publishing

Always test in dry-run mode:
```bash
python3 scripts/notion-sync.py --dry-run
```

### 2. Use Consistent Naming

- Status values: Always "Published" (capital P)
- Property names: Match exactly between Notion and script
- Slugs: Use lowercase with hyphens

### 3. Validate Environment

Create a validation script:

```bash
#!/bin/bash
# validate-setup.sh

echo "🔍 Validating Notion sync setup..."

# Check environment variables
if [ -z "$NOTION_TOKEN" ]; then
    echo "❌ NOTION_TOKEN not set"
    exit 1
fi

if [ -z "$NOTION_DATABASE_ID" ]; then
    echo "❌ NOTION_DATABASE_ID not set"
    exit 1
fi

# Check GitHub secrets
if ! gh secret list | grep -q "NOTION_TOKEN"; then
    echo "❌ NOTION_TOKEN secret not set in GitHub"
    exit 1
fi

# Test health check
python3 scripts/notion-sync.py --dry-run

echo "✅ All checks passed!"
```

### 4. Document Your Setup

Keep a checklist:
- [ ] Notion integration created
- [ ] Database connected to integration
- [ ] GitHub secrets configured
- [ ] Local environment variables set
- [ ] Health check passes
- [ ] Test post syncs successfully

## Advanced Troubleshooting

### Enable Debug Mode

Modify script to add extensive logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Inspect API Responses

Add response debugging:

```python
response = requests.post(url, headers=HEADERS, json=data)
logger.debug(f"Response status: {response.status_code}")
logger.debug(f"Response body: {response.text}")
response.raise_for_status()
```

### Test Individual Functions

Create a test script:

```python
# test_sync.py
from notion_sync import query_database, get_page_content, extract_properties

# Test database query
pages = query_database()
print(f"Found {len(pages)} pages")

# Test first page
if pages:
    page = pages[0]
    print(f"Testing page: {page['id']}")
    
    props = extract_properties(page)
    print(f"Properties: {props}")
    
    content = get_page_content(page['id'])
    print(f"Content blocks: {len(content)}")
```

## Getting Help

### Collect Diagnostic Info

Before asking for help, gather:

```bash
# System info
python3 --version
git --version
hugo version

# Workflow status
gh run list --workflow=notion-sync.yml --limit 5

# Recent logs
gh run view $(gh run list --workflow=notion-sync.yml --limit 1 --json databaseId --jq '.[0].databaseId') --log

# Repository info
gh repo view
```

### Where to Get Support

1. **GitHub Issues** - Check your repository issues
2. **Hugo Discourse** - https://discourse.gohugo.io/
3. **Notion Developers** - https://developers.notion.com/
4. **Stack Overflow** - Tag: `notion-api`, `hugo`, `github-actions`

## Conclusion

Troubleshooting sync issues is systematic:

1. **Verify Notion setup** (database ID, integration, status)
2. **Test locally** (environment variables, health checks)
3. **Check GitHub** (secrets, workflow configuration)
4. **Monitor workflows** (logs, error messages)
5. **Test end-to-end** (create test post, watch deployment)

Most issues fall into these categories:
- **Configuration** (wrong IDs, missing secrets)
- **Permissions** (integration not connected)
- **Status filtering** (posts not marked published)
- **Workflow chaining** (`[skip ci]` preventing deployment)

With the enhanced troubleshooting features (verbose logging, health checks, dry-run mode), you have all the tools needed to diagnose and fix issues quickly.

Remember: **test locally first**, then validate in GitHub Actions. This saves time and provides better error messages.

Happy syncing! 🚀
