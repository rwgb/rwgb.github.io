---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663QJNWIHQ%2F20260703%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260703T051938Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDwaCXVzLXdlc3QtMiJHMEUCID3GnQwCjD9wEahqreTwnpn0vX1I7z2BzweUlH%2F42ev4AiEAyb7TkR1Yb6p%2Fd9vhV%2FxLP45i522qMBSD5643f2860KAq%2FwMIBRAAGgw2Mzc0MjMxODM4MDUiDGX%2BYW%2FvJf43%2BsaEyCrcAxB6m64jPGnxGKA3LSliCUXE9BH4w%2BhhM5M4qmQcKVnzvr1XmJJqFVIM%2BvVQUO36BMYueudE1kqzyZj9xbR2THJULdlT75Y2%2FNTnJ8qzUj9Dp7vkGZBb8awoch8ekaGoRCyF2IAdV4MTl2R%2FJvMk2FBuCd4cHQKOtHZA2oQV%2FYkQXJ70VlJ5dAY8o%2B1xGz97dVUmtJc0GcGivVOjJPkL9ctlEiMLkgN0PBns2l%2BNvR%2FTC1Lk1OnnKmVubKk9yAywpR%2BCjKLG9ZQGDJIXpBY92ST%2FCsA5eBwlyyDDeERF8c9sDNxCP9syJGMdoReqDJd7SMOF6VM4cGS%2BI2BDP1cZr44%2BelRNZWN9LZXxgBLVlsdXrQyuC%2FCQREv%2BacJD2dNSo4j4vAiQaX4BHcF0CCODuQXtWFMMYPPBmIZxKzhvJ5SvXQ677Qg5O5kcerNFf6c99X%2B%2BKSMdOzoVnT4oQmqbdXFtw%2Big4ihXN%2Bp4Ymv1yT2zrtexY7VRX5H%2F3s3DB%2FcJh%2BtlS02Tp3x2w4r6mnd0MLBgeJe6BOlo4PzwoPjSMe5E%2FpBehtPvr6bDs3imist%2BTBc0UFJiNPcZyVwb0yXXdbh%2BKlzj%2BgnwK%2FcyOlzY9uP4A94BRlBu%2BKf%2FTNVXMLDpnNIGOqUBiqyUVxi70d2ZyhyEIQTuykbps5gF8raSvfphNaSYEb%2Fa2nSvWNHZtwLf7bETYqvS3olPtVN7UbjTbL2eQr3WgE%2FceZbS%2FCwI2soo%2BKnDDWK9n4hE0dDZz1CyJZ%2FNmxA1zTHMqq%2F%2BwB%2FILfjw%2FfFR9w1DFouTwdQm0loWQVkBwrxg6OPoz0bwE%2FprBBaFOrM%2F6cjZH4QRrCmKPe6rd2szKg7%2BIz7h&X-Amz-Signature=ecd0a04a3b36b234155b2eeb4c9c0d4b8bfd19e6d6c7d53d7a56495b49686f08&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
