---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662QYSOPUX%2F20260104%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260104T132923Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGEaCXVzLXdlc3QtMiJIMEYCIQDbMrtQc5qauiYyZyQvPiDxUPXWJe7mszNYeCd4glXq3wIhAPuscy%2BXU9s%2FCAAH2eQ1QmNjpyE%2B%2FfY1Fzqoe41lc8%2BwKv8DCCoQABoMNjM3NDIzMTgzODA1Igw0%2BTAqoXuv3jXIEz8q3AN3zuq%2FJNcpClTZub8baY7YZP2NRoK6OKNXv%2FO4j44HY91oAXXARU666d%2FwCQbs3uhkzWuY8mkqsBP1lGsBspMlQ%2FD9bicurG42dzUwrOMrZTMxJmJQDzn04mVLKsgDHuWfMTrfFPocMjhGw%2BX4KTlInn64RkR1l%2BXg8SNzrIwELsMLthyqEivp77To1tNE3B3y47yxAvtK14Uy%2BNLcN9QZNR6ragtKarSrUDdozz0kIUzZNvbrgR%2F6Rvl7Js6erRhJAeotRimefNuVKNLHMicR%2F9G%2BF3oRtXVtkelLdPoY0FBqdsSpAvOtTFFlUbkA2p4uOl65zfBjuFsK9nBMLgJ6Ns4thtQ8Ei5tKfByF%2BBJF3lG7gDjn1NBW2meD6jMKZF5DwA8i9ytPPMrUs57RiXoC1GaS0rag3JGq6Xwxk1A%2BSWZ49k8FtRyIZ%2BY4%2BZYjFMDgBktumCI4FgivOrOAC%2FbKWa2x%2FqaDuKThTx3aFw3n4OLa6xUdwpbk2%2B%2FLtLRJ9aQNvTEyHp4b%2FBGwHJT8CVWdl4J9arzKttVBX6nLk0%2BxOO5%2Bm%2B4XCCmqdTAaSd6zyj%2BR5MHOdqrIY1%2Blp0znJ5rwDLgU7%2BcFK0wWRSR0NGcxvBMrUepphcs3%2BkmgTC92OjKBjqkAT3UpfQd5ON47p2j290ey%2Fq%2FwrbMe8bRkaOletFmYmCdlgLPAsrsYJEia8KjE3fVSwBfU%2BXBOXxp2W3dw54mV4itfTHWBTAHvveMdi30We%2BSdxot%2FHK1ZGav%2FdVpy%2Bp5QceOXB2aw8UJwB0StiCLaQvxPWe8HugMsJUM2p8yIWG8VqS3D1mmWIe%2FJkx%2FPoXWVYQjaSrfIqD2K1b51cgm%2F3JbzlPz&X-Amz-Signature=6b27e66faf2b301fd04c8e6d0494cf0acd41fd4652b3d5be9e5a21edb880c8ef&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
