---
title: "Write in Notion, Publish to GitHub Pages: The Ultimate Content Workflow (Part 1)"
date: 2025-11-07
description: "How to setup Notion sync with GitHub Pages (Part 1)"
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

![Image]()

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/60aa9ac9-35f4-4664-aabb-818587404733/0864ca02-d51a-47cd-9b67-5280dd5ab85f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZW3PIKC5%2F20260409%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260409T073550Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEgaCXVzLXdlc3QtMiJHMEUCIQDrfNDy4oFUeVVGCOMat4MVmy15wkuBc84Ivf%2BCjRU%2FOwIgSO%2BZUXUekerrw9NvWwuBbfDYo%2FbhZr3MM4HmwmjNR%2B8q%2FwMIEBAAGgw2Mzc0MjMxODM4MDUiDACZZXGN8xlYRlHbTCrcA3J4BFW4IaPc4JAQ6QGCucZAFCK%2BVFXumxdrruhrDXhVU35lXhy1NCYURIe5IcOEv7LdaHWZqAHFaNt08%2FX20occY7DUiZKV4dPaAuoIn8tt04%2FXH65tbHARkmvumYbvyt94LXkGZUWTVAELLjeUn37esPex5G9Ji6IUUYhugMmYQHV%2FwPc%2BT8xj0vxzMGe8dwe1%2BmY6fCwXPtyembzXS8qc%2F76RHVsg1hCqnZB85caedliBNsb%2B77rTdKuv30AZpGgaEyvsvGvn6I%2B1L5jM2JMOf7fkVFrKsLD%2FkdbX0KMqIV6wMWQTjY4h1sshKIKdWOlQJqR1NucUYR2Qng8Q6zmd25XOTNX8vA9gsWgfOYONZA%2FS%2BYi%2F%2FBNQkeOpPZ3lZ%2B9ck70sCBcDXhYmbNvmDbtR1ZIrsAWzxj9LC8hT4Vq3GwyWDdWxrYWHODSwKtA%2FEcwMvqiRV5NFDm1u1sScnk3weSqMTfOiQMrslcqcqIT45SiJJUD5RBuiIKhDAhIEFfgCoz1ErIqa3G2kG%2Fc76okfAPlkgGRf2YRwGGJ7SqRtfP3TSwiByNtE1eTV%2FEbDf9yxTf7elsqkxt4dqFlZIYx%2F5YvOk%2FK2BolVjBaPpQEj68yfl6NvVmzU8Q%2BrMOml3c4GOqUBDCqWUlRaYjClBzARm6nbJircOq4UA%2BOSM9y0h9vZwXepocLmsNVQlTllhBvgOzDOE56ya2DYHjrHgJBmKs4r0dTT3m25Z5hV%2BX2mb6I1Twr5ODc8ltq0VRYCfYZ%2Fqh%2FxeFbBmo%2BwR0L%2Fon6GBTUPTl1StYgl%2BLTdcvE%2BntY%2BD6uvDPP1yTDC0MZJVnlZJaTz1O6HpfivvIEDCPvK48NDCTY%2B%2FT%2FO&X-Amz-Signature=abc74be3cb541f6024ca2eac250ef27831ddb13239c0da525d31511504c33ee5&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)



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
