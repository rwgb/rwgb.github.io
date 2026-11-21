---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664M72C4HB%2F20261121%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261121T100635Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHkaCXVzLXdlc3QtMiJHMEUCIDpP8UudP0r%2B2AGzyRoEOYFx9dRt70THPfE7sp3eH0b3AiEAkCFEfw60fquf2JMAUhR%2Fvu%2B7nGWNNfIrv0lf0sE8Y6wq%2FwMIQhAAGgw2Mzc0MjMxODM4MDUiDEGiZ1V0RlnMcvF12yrcAzp1bqQMNbcDKn64yYy%2B7V78WZMYoyOXNHL2pCOs3Tw%2Fs6XiT7VX8IZKInS5Y9oOtYvVoB2Own8LOjukcMuj2kxkzPMFa59BZRd1nkbzQte67rbSZmu8Jw5CmOhTe1%2BRN0PCe6FpLf58yOmQehXmU9Awfj91QDKQGxBoj8aPrVqbPWFOxWkuYH2rMKCDk10eSHJV82pXc1zz3J9ZaNnMRE%2B3Ael0hI%2FqSUcVlson7zwT%2BJEykQhozf8H06CbHtpkB2nXRM6O4YakGrX%2BQEIX7A9VWsCcQ%2FHFiwD4YPNHMjerQpHHt%2FpLnOINSK5zaE2%2FBgI0OQVRi%2BIXHicZ7awmLnnW96BjzdmgzmmODdwVb6wOLIzDJsQ4J5uzWWIOF7Sv8H1GL0plNFunm0ouqbaYNWDAyixEpLT%2BMj4%2BO6zX%2BrZ4jxH%2FcFD31PYCCY%2BmOHAV2JmP%2Fdl9FM3xi4NzGfSop8ot8XpnsApAcwybOTM%2FAtLSggVnsI9zu7tmw1r5oeVCR8RoRuFl0DF6KIBbiJEWtSiIiqFH1wFGBx91%2F2qzR%2FPsmyhaftp%2B8ZFpWeUezX24WVh38uggUG0QnVwe4ryj3b2UX3HWolbyp%2Fb7or289Tz872B5ii4e9vHAvBEVMI%2FAhdgGOqUBN4ESOgNM393uLFvXAYcXQzWVd%2FjJ%2BjMd0MK6mQnzR6uxR9h0fiDcnBIgioG2WCxHf%2Bqj5a2EntmTT54Oq7D9QrXNTT7mHRD5Vh3yEQY20f%2FWsZNMDHZbs0Nex6nDj%2BzbE470ltRbF61ZwpsNAzP77W7fNuj6m3fWwPhppVQZvyOAau%2FG12uCnK%2BVb39eI6kuSmhUjFWbHQ1HTkxNaijWzHcGkd5T&X-Amz-Signature=9e4f287ea4ac97e614ca51b27d7eda614e83471abeabdecba680e9bc6dcd85cc&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
