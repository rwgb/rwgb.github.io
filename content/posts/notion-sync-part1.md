---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YD5DE3KZ%2F20260523%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260523T162325Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGsaCXVzLXdlc3QtMiJHMEUCIQCxXyxtcMzaR0IwqaVsY7ag0DY2HwoKQbhgzBVlYXffNQIgTQ0hEMBzkddec6dty5byTBUCUwUhrc49zT0zUQn59dYq%2FwMINBAAGgw2Mzc0MjMxODM4MDUiDKpVCaOaPbRn3zH2XCrcA7D5OH4ypMAcOlnzqQvJmiezZdluKQ53CdraDGRaeFIzWLzLx3MhcWiZZXhoRJ0W6cZKOnE3LAUeHkj1Yxn%2BAO8nOKODeRm4%2Bi%2FsZWInoULAkk5pUEkpKxfEo4Uk5vpYUCDMtIIW6ppSZ0%2BoMV%2Bsj8JEH64%2B6Zsis5JkfQYyNxP2OSpXlnvfeMantmYkyJRl0lpWymeJ1UGnuMkbVqBZzb%2BJzSz1VAJZo0wvSAzoPq6bseyxXnI3lrFL0jpiHzZHpQCOZLeHOeme9qOBgm%2FY3kRMWFXY%2BKgmcw8rtGTuEq7q%2FCN1c5dE6KKXpUEYAXlrP3CUU37%2ByEeQM8jfg8TU8K2OtTt%2Fi0F4N7%2FjsdNdbnjlGf5F60EXleblAU1pdhJYT9%2Fhgnl2mD49284TMg7AlfJQyBO1V2aTxxE4vr%2BSj7y8qYGqKiI%2BROGAkuzYCWMPTmZv1MY9XwvbzuCRlJw%2FSdRqBxafRx7r4ViZeYp8U%2Fwg1TzB8TtwM96Uti4Ovz0M4pa3t98bIC6K9xsz9Vnrhgzqu6pe8qfsXcNK88Ye97GGDU8iCoZV6bkgLu6OgVV80vJIIxAXKgfCBDETqmIn1UXCJ4dZEe7yYuyJcc5eI038OuyEm0O3tI9IejLsMOaSxtAGOqUBEG%2ByXCtXwHqU2Aiw2oIB5UABn%2FQCqx3h%2FOqQ5SRZkrNawYfJ3uyE6BhrqAJOlOz%2BN40fDiHXfOjnM7TJUTKNYZk7PI6%2BaGGk3kh5vcJJ953irBmVSE0%2B9vw1XDAeYlj4RnMLQ%2Fhgm4YD%2BUITJ2iQzLpGtVOt383WNUVRmwCZFeB%2Bdqg6yNoRHUx%2Ba6QP9QvZBYuHIEcVktd9bynyocU2Rodb%2FC40&X-Amz-Signature=a059c66de9e85af0f217ea396d13b17d8163b62ca45a62381d4c540cac57c04b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
