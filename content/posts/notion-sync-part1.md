---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466VJ3GRSRC%2F20260925%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260925T131128Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECMaCXVzLXdlc3QtMiJHMEUCIA2OojVPSt%2Fno5SbKao%2Bb2U1UFFIPvyHqfhnZVYbCkDnAiEA8WcwWJcS0elCGSpIgItgrV5qAMPUAop6FCVNPhYUhWcqiAQI7P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDIWBvy%2FfJOVf7LhQPCrcA%2BLmZhWHa12SHqxFvM5%2BHL8eX%2FxyC5MHFLUCkxTtia2eIbTr%2B2gkHPKboEaxcytphrWoOGggMpvJSf9j4tibnfDcAKka2Q3IvA%2BMSPpbi%2Fwddcaa9pMQdgAHZ7FLGn0wlzzcMJxdZa7a%2FgS0pefXZ%2BJZ1syGf1Iqhyvl4SMRu3vJDDcI%2BqIhuk9P%2BgKs1dG8HdWkFkHK13yPg8a%2Bh6Gipe6reVnb1R4WKdpqSz%2Fggprj3wZHCl7Hz%2FEFa8Rl%2BPEudC7Ep%2BsiJOw6%2BtxsKEejGvynXM3dZVcRE63a4Qg2tkWmOU7ZzjOJNKObm406wfFCct%2FPd3xo6ROJYFz9yrUlQGYC80s186pz1tD7Z5QdDrnowzllMqjWlCjEwx8ZU6uNcqygJlU9SqI3AsjfN7u80xjbN2szTfLy0XpAk%2F3snqVSALe5qYuO2Seylj%2Bvit9HBKusTGhD25gTBVbe63YJl2YLG%2FIAzdlq%2BIroP7DaszVCMGWYSYtiM4nTj%2B9ctsCtlKxb%2BA7Kddax7X4I5Bw0P5KP4%2FGa3UgLWeDboljS9ksTKscV6pTwCgRDlVLWSMazTPNHT7XGCiK%2BYnTHHzP1mFX3C%2BnVbB3jRXpuAaAhE%2BZdM6lsHvDIx0LIdbayMOin2dUGOqUBu2%2BGDftjm9JzRhZBaqfXyL2DKXj6nCEWTobz%2FUFzQReCtX1UFeuEzgM%2FA6yf4giuzrNwQHOMByKS3vtpX6Vf%2BxRHfCc1JpVMmRMfpNaYNYhxdl1s7aXE2o3D0hRw8K%2FXJDEMvmfWHRfLXtqdo0A6vGx5L1bmdZk8UeRe5%2FMcMzre%2B3E4qsY659QXZ7rHeAbkWcFOkmEuKxT9lMxMWTbFwroWuXA6&X-Amz-Signature=bc0730b54aee36a4ebcf69b43c3dc9868c138930f904b688e1828dc9250dd12d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
