---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4667BWZFL5T%2F20261029%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20261029T121248Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFMaCXVzLXdlc3QtMiJGMEQCIAkJZ6DwrT71%2B%2BY1Lw%2BxhgCKra6%2FvfTFVGaWkY2OcYzDAiA%2FzNpuH4wd5ORrW%2FYCz%2B2kvDO8N2qcV9DpfEG4gUmHiir%2FAwgbEAAaDDYzNzQyMzE4MzgwNSIMWNI%2FI3UBud9I%2BM9%2BKtwDzY469n%2FLHIMCk3D5IU5%2F%2BRVAU1gt4K6mG5Pmi87IwhjHigW%2FqIvenPLMHA5oYviUoNQ2x2cIfDY8IUmto7EG%2Fuunt18G%2FH4sNXUVE1Tlxd%2B%2FVBZSJsz7IwPxlALLmYzzP6sR4jkg7gO%2BUF3mZeu%2BOwWS3PZ6iqd2EyOlPMJ5GisQilpVkv%2F9qvWVynpRXqi7UH9hGZEGV3XeyiPtK1dlUCxAfN01yGXiubat7W%2FjqwMi7J38RopIakTbvS5cW6gpvVCeeR%2Bme4CCChFZfX%2B%2F0PG%2Fw2wU6eFbCqGASnjT7whKPyq3kHPiA%2FbUWsTs44cZjb5e50avAGberdNoZM2kcmRGCco%2BBZxHZHOAtVt6riTZvkaFXwEmWIYC%2FBmxz0oBFlUjzUiGve3fe7LTfa04ljM5S%2FV1s9qhkS08KL%2FsyYPjNteqmROxmHzHEAPxL9dsuwLvUVC6C1EBDTLh%2BzxbzFpLFnpbKji1DeFEucdqzHLdXV9g%2BxJf0C3VF30TSTzJD6s5wOjehbSJov52XN1RJi%2FITmnvVdcq3Qviix8Sw6QbI3BHlqX70Aqqcd%2F1SrtfZZsrIRapB%2BJ%2BUGL5mWq1cBGWrSLOW%2FetnYlonXSwN0XnbmdGFQZ4mtTCQcgwzMKM1wY6pgHps0xvAa%2BtA1ZwlZe1p9J1h1%2BpJRWZxXgdl%2BuahZ%2Bg91iVcBJJi6Zwc0IbJ90JgulBQs1pC2IKGsAAOMhdQk2gl0uopa06tPMl2JNTHf%2FlMzYQoEIPN%2BjL5G%2BwL6V3o98VoJZCbf4yhCkSLvJ%2FeFyPewbfaQA2NTD0frlq5uLl7%2FV0MfepNHBAmzsAOFE02MNend7v6336vI%2FjGaqZg5nWPSVfF%2Fge&X-Amz-Signature=f9da94349922943aee2cf2945da6a5e39b11f0e12ab07f4414e8639e0d9f154d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
