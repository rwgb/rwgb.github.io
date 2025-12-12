---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46636F6L66V%2F20251212%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251212T152242Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjED8aCXVzLXdlc3QtMiJGMEQCIEIhvkt85pyMs4%2BrCc19CNHp0QNrWPvQHcmEsJkmGX8gAiAWtb5bWscYbsUsQK2f8zeszERHkX0siYTcxrlg%2FnGwyCr%2FAwgIEAAaDDYzNzQyMzE4MzgwNSIMZg%2B61CTwIB8ckgbdKtwDitUFpanT6E6gsWTD5FOg1EPLVQ%2Ftcxf4bRY%2BfF8OrKSIjvvy7IDfIdoilYfh%2FGMvuBak6jcz%2BEqnmYJzGMSioh5RUEUtL1qF2LGqHIUZCnC5Ypd1sr3ucn1eEZ0HYzvj37Nft45jR6sbp56w86VcRjZL79akvI7PiKcIzVVHg3%2BJCaGraXUMk1Uvz88bOW87ogn30FkYZxW6fscuEYqJfvJnFuS3iDNeWHtt%2B3CdKrncxXIQzwj%2F5bzV3NncH8m5kJ41U3Q9HTx%2FVlJ%2FsbS%2BM7h4fdstiCk2yLE3cy%2F%2Bb3c%2By6UUtM0E3MlAStw2H%2FCmSxyr0zwe9zi%2FUaQDDgMCUzBJe577S1reE77StsOGmCpMN8pyjyemmJbY9tTwCwYaC%2BVQljIqtXeobO4Pz7KIM6z9WiLRkzPKSHqbikKNp%2BDiPwVqA0yaWHSIdLPwOXIEigRjEpbmhc0mhLP2t6qDUNSRpBAlzxN8xp2g%2B2a%2Blh40i7ETxOmAbt8VKGK9wGV7Z7G0FxxxnlIPGu6WNdBi4FOtNvPOytaNtBNexNj237cyeLM0Cm%2FPvfytMpz%2Bsb1YFCoR1DCtP8rtS5o0o08dgZv3xlSFBJyjLbWFcSDW5LcJqVStPUSqEi0iMSIwq9LwyQY6pgHm859d4EM4b%2FDtI5ydi5mza%2FZO8InM3vitYM30vnmvmHaWhHIopp77CtwcHtoO%2B9reYBP1iv0rs1m4awgrAqqbGnR25cD%2BSj8x%2BeYXeeg4PiX2akgqOl%2FLNGXDn9RY8co2SqyPwSxAKfbWD%2F21js0eQ5A%2B6ivHs%2FyCuJLL0E6xYH3fHYGpFJOZrJlb2IAQG12%2F9MJ%2B6vxlqaWtUZ%2FAflG%2Bzeeqh7N6&X-Amz-Signature=1f25b5cbb424fcc3b2fdf51f2dd587d51c9d4d4bf12feb2b83347f6dcdf38ba7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
