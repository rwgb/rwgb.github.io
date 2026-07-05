---
title: "Building a Personal Website with Hugo and GitHub Pages"
date: 2025-11-08
description: "A complete guide to setting up a Hugo-powered personal website with automated deployment using GitHub Actions."
tags: ['hugo', 'github-pages', 'github-actions', 'tutorial', 'web-development']
categories: ["Uncategorized"]
draft: false
---

### 
Introduction

![Image](https://prod-files-secure.s3.us-west-2.amazonaws.com/9e3ec090-318c-4799-b781-4a29473b2c8f/ced86231-af74-479f-80dc-5eef83f898dc/building-a-personal-website.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665QH4MSYF%2F20260705%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260705T004431Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGcaCXVzLXdlc3QtMiJHMEUCIQDNsrGmsGO8tJKYg4nu0vX9ug%2FxV4Izc5zlVPDu2JcJ1AIgaNynkv96QbOreqPOvj%2Fle6jifHmOz80ZC%2BhuQk1E4C4q%2FwMIMBAAGgw2Mzc0MjMxODM4MDUiDM15Zbg1lCYJbKa5WCrcA1q4uG7Q4pqvhiLcTHJmfigzSchA%2BAPMlW1ZVvzV95W7QLaQa%2BjmGPe2p3YhZO9iUnJVoXwAmRsh%2Fxv0SjcYuRLJVK3MKrjqEttKh%2BNd4JA626PWhhzAzZg45RnQPn202jcEU6C3Pckjnv0zbFWT8ftZuv%2B5Y%2BmEfKSzXv5%2FzGPhu6mArREsYqBO%2FNloPWukEQtUwwf4K9uLrT48FQgk0waewHdQoIIrObl8PdfgukO74DthVFQBxITYsdZYDIc0zZ5f%2Fc1QXR%2BRdWZnKukCrY0Pr4CizDtkmkxwTFtBrtdgLQOUABNN9yW0oys71r%2FML89SGn%2Fq1QcUaXzOXldbif70ltwZEfbMpJ1rEh3%2BdY%2FN848JjSLQZX7%2FLiHGucuBGm8iGeMhM5DZizesmmnHbiueXZHLmW3aOXFOyWBDTWiQf%2FhR6sUf21k0cFe297DdHs4fQ0THKnA4ikBvP%2FK%2F1FRpC8O7MoaptxAifnSWpORWiVavn45jcnaH7Ugm5vDyKxGpNSadYbH%2FWaJeA6pVYz%2BqdqWixFBlpGpZQrJN8%2Bfh2B3bw1c270Tli9lWM3CUdgL89TENKCpOqJKTX7WhkhvL%2FKBV38xOeZZ945K7DwgliHFkpXsKRovcU3TpMKWoptIGOqUBYcLb1%2FDKstmT%2BRl2Z8cUFjlI75a7%2FnRUHDwj%2BL0%2B%2F6YaXkuJRtrotvQ%2BYYi5bj3BVUW9A8NrJ6TXqgSYQI7Z%2BreZMHvrJwxQPKFK8B2%2BrjpZItJ22Yirr5BtfNBNUhVPAVNrpZ3mw1qtTBuPpDwuzgmM81ukakI5l07RYILsjq3w9Q0F6moZ6ADt9SLmDf9dvBwQ2csc%2FSttQ8TvrJvbdOnYtt1i&X-Amz-Signature=e71e42542f8e8c388e38755ab090327533eaa0cc9742a40e477531a354f20114&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

After wanting to create a personal website for a while, I finally took the plunge and built one using Hugo, the Congo theme, and GitHub Pages. The best part? It's completely free to host, lightning-fast, and automatically deploys whenever I push changes to my repository.

In this article, I'll walk you through exactly how I built this site, configured the deployment pipeline, and solved the challenges I encountered along the way.

### Why Hugo and GitHub Pages?

Before diving into the technical details, let me explain why I chose this stack:

- **Hugo** is a static site generator written in Go that's:

- **GitHub Pages** is perfect because:

### Project Structure

Here's what the final project structure looks like:

```javascript
[rwgb.github.io/](http://rwgb.github.io/)
├── .github/
│   └── workflows/
│       └── hugo.yml          # GitHub Actions workflow
├── content/
│   ├── posts/                # Blog posts
│   ├── projects/             # Project showcase
│   ├── [about.md](http://about.md/)             # About page
│   └── [contact.md](http://contact.md/)           # Contact page
├── static/                   # Static assets
│   └── img/
├── themes/
│   └── congo/               # Theme (as git submodule)
├── .gitignore
├── .gitmodules
├── hugo.toml                # Hugo configuration
└── [README.md](http://readme.md/)
```

### Step 1: Setting Up Hugo

First, I installed Hugo on my Mac using Homebrew:

```bash
brew install hugo
```

Then created a new Hugo site:

```bash
hugo new site [personal.site](http://personal.site/)
cd [personal.site](http://personal.site/)
```

### Step 2: Adding the Congo Theme

I chose the [Congo theme](https://github.com/jpanther/congo) for its modern design and extensive customization options. I added it as a git submodule:

```bash
git submodule add -b stable [https://github.com/jpanther/congo.git](https://github.com/jpanther/congo.git) themes/congo
```

Using a git submodule is important because it allows the theme to be updated independently while keeping your site's repository clean.

### Step 3: Configuring Hugo

The `hugo.toml` file is where all the magic happens. Here's a breakdown of the key configuration:

```toml
baseURL = '[https://rwgb.github.io/](https://rwgb.github.io/)'
languageCode = 'en-us'
title = 'Ralph Brynard | Developer & Creator'
theme = 'congo'
enableRobotsTXT = true
summaryLength = 30

[pagination]
pagerSize = 10

[outputs]
home = ["HTML", "RSS", "JSON"]
```

#### Important Configuration Details

- **Pagination Update**: I initially used the deprecated `paginate` parameter but had to update it to the new format:

```toml
[pagination]
pagerSize = 10
```

- **Author Configuration**: The Congo theme requires author information in a specific structure:

```toml
[[languages.en.params.author](http://languages.en.params.author/)]
name = "Ralph Brynard"
image = "img/profile.jpg"
headline = "Developer & Content Creator"
bio = "Building innovative projects..."
links = [
{ github = "[https://github.com/rwgb](https://github.com/rwgb)" },
{ linkedin = "[https://linkedin.com/in/ralphbrynard](https://linkedin.com/in/ralphbrynard)" }
]
```

### Step 4: Creating Content

Creating content in Hugo is straightforward. Each blog post is a Markdown file with frontmatter:

```markdown
---
title: "My Post Title"
date: 2025-11-07
description: "A brief description"
tags: ["tutorial", "hugo"]
categories: ["Web Development"]
draft: false
---

Your content here...
```

I organized content into logical directories:

- `content/posts/` - Blog articles

- `content/projects/` - Project showcases

- `content/`[`about.md`](http://about.md/) - About page

- `content/`[`contact.md`](http://contact.md/) - Contact information

### Step 5: The GitHub Actions Workflow

This is where automation comes in. The workflow automatically builds and deploys the site whenever I push to the main branch.

Here's the complete workflow file (`.github/workflows/hugo.yml`):

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true

      - name: Build with Hugo
        env:
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: hugo --minify --baseURL "$ steps.pages.outputs.base_url /"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: $ [steps.deployment.outputs.page](http://steps.deployment.outputs.page/)_url 
    runs-on: ubuntu-latest
    needs: build
    permissions:
      pages: write
      id-token: write
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### Breaking Down the Workflow

- **Triggers**: The workflow runs on:

- **Permissions**: Critical for GitHub Pages deployment:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

- **Build Job Steps**:

- **Deploy Job**:

### Step 6: GitHub Repository Configuration

Setting up the repository correctly is crucial:

1. **Repository Name**: Must be [`username.github.io`](http://username.github.io/) (in my case: [`rwgb.github.io`](http://rwgb.github.io/))

1. **GitHub Pages Settings**:

1. **Git Submodules**: Don't forget to initialize and update submodules:

```bash
git submodule init
git submodule update
```

### Challenges I Encountered

#### Issue 1: Deprecated Actions

- **Problem**: The workflow initially failed with `actions/upload-pages-artifact@v2`

- **Solution**: Updated to v3:

```yaml
uses: actions/upload-pages-artifact@v3
```

#### Issue 2: Author Configuration

- **Problem**: Got errors like "can't evaluate field name in type string"

- **Solution**: The theme needed author as an object, not a string:

```toml
# Wrong
author = "Ralph Brynard"

# Correct
[[languages.en.params.author](http://languages.en.params.author/)]
name = "Ralph Brynard"
```

#### Issue 3: Deployment Failures

- **Problem**: "Failed to create deployment (status: 404)"

- **Solution**: Had to:

#### Issue 4: Public Directory

- **Problem**: The `.gitignore` was ignoring the `public/` directory

- **Solution**: This is actually correct! GitHub Actions builds the site fresh on each deployment, so you don't want to commit the generated files.

### Local Development

Testing locally is easy:

```bash
# Start development server
hugo server -D

# Visit [http://localhost:1313](http://localhost:1313/)
```

The `-D` flag includes draft posts. Hugo's live reload makes development a breeze.

### The .gitignore File

Here's my `.gitignore` setup:

```plain text
# Hugo
/public/
/resources/_gen/
/.hugo_build.lock

# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/

# Backup Files
*.bak
*.old
```

The `public/` directory is ignored because GitHub Actions generates it during deployment.

### Deployment Process

The actual deployment flow:

1. **Push changes** to the `main` branch:

```bash
git add .
git commit -m "Add new blog post"
git push origin main
```

1. **GitHub Actions triggers** automatically

1. **Build process**:

1. **Deploy process**:

### Performance and SEO

The resulting site is blazingly fast:

- Static HTML files (no server-side processing)

- Minified assets

- Served via GitHub's CDN

- Automatic HTTPS

- SEO-friendly URLs

### Cost Analysis

Total cost: **$0**

- Hugo: Free and open source

- Congo theme: Free

- GitHub Pages: Free for public repositories

- GitHub Actions: 2,000 minutes/month free (way more than needed)

- SSL Certificate: Included with GitHub Pages

### Tips and Best Practices

1. **Use Extended Hugo**: Many themes require SCSS/SASS support

1. **Submodules for themes**: Keep themes updatable

1. **Test locally first**: Always run `hugo server` before pushing
