---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SR65YCLN%2F20261030%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261030T180759Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHEaCXVzLXdlc3QtMiJIMEYCIQCzK4LmfFuW0vM%2FdoNKZcPUlLwVADJYnt9X1TlAooc9BgIhAIZl146TG8tLjrnF4hEE067Oa3NGfVSYjK%2FJ%2BNnHruZeKv8DCDkQABoMNjM3NDIzMTgzODA1IgzGzqzAZQ73Mkvkz7Qq3APrGx8YfGHnlPmnSnrF31VrRV6kQMmC%2FNYQwnLA8kxX5d6Sx%2Fz%2BIpJ9F7KYGgTBy%2FHkoK0PjMd1rCm0IA8xEXYN%2BdvzKVQzFC%2FNEOPLHU7T6A0eilsX5Z7hvWLCnNkRfSC6OL2zwxRhYvejdIWdSUjhCs5esB1r7LqgR2cgvD8LzVooG8Q7VH7I7%2FinKft2IG2LaTbh4%2FBuJ%2BoHgn3Cnv8bc%2BF8vVz7K7naBauYVNzEnK4xREYu%2FatMm16GS04GlW%2Fc6CP3fb9RBytCLT0B3w%2FvMy5%2FC1pRscs0tUgm6mqp24A%2B0FGmf3ZFjDPfxuFSp70aavjausl3%2BqphNMBN7ia89k9%2BTYmwtDQN34%2Byr5S4P8jbWI5YjZoeMSvKsED4MFpAG8p1yY6Rv%2BiYY5h7MfMe7aUz0RpnaVcxNTCyH3wM6Lu4nJ9Zksg8f1il%2BvNHQZ1ZrsEtv2N1tK0asDVrqMpQ3dlf%2BHtgaT69eYu5AL%2FlTfirpQp%2Bqff%2FbMzhPv%2BE7XuTPl%2BQ1ofyunEneJp%2BxiAeM8JePIhApSPWYwKCa1xpa8KUhq1jRpCNk6dmbk1l8DD8YHyx17xhb9gNYc2qOnsyGYpZ1oTaU01%2FpBdvxYHC2uTrOSK172c%2B1wGVXDDiiJPXBjqkAYgx4qUa2kLZUh7Mw7ie88rOCg0Kzf%2Ft3M9L6Pls6g2I2lnUTpZ9VQszl1d8AC7kFg%2FQFLjkr%2F7dP%2FRMXvVAGKQDfG68y4WW1moVqfbg1tBWQW4QfTOXn2SseTVQaLWigRjCioLohxTmDP93NcoLVN8NLD9bnkiu0SEQyvjAX%2BG1nGu6M8cUGphJc1TB52SBEjyrqIKrwbrTW51ks0h8NgGdFMcP&X-Amz-Signature=99767134961d9e7155e5800e78458016c0f645f819f585a1a13a68d57c0390f7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
