---
title: "Building a Personal Website with Hugo and GitHub Pages"
date: 2025-11-07
description: "A complete guide to setting up a Hugo-powered personal website with automated deployment using GitHub Actions"
tags: ["hugo", "github-pages", "github-actions", "tutorial", "web-development"]
categories: ["Tutorials", "Web Development"]
draft: false
---

## Introduction

After wanting to create a personal website for a while, I finally took the plunge and built one using Hugo, the Congo theme, and GitHub Pages. The best part? It's completely free to host, lightning-fast, and automatically deploys whenever I push changes to my repository.

In this article, I'll walk you through exactly how I built this site, configured the deployment pipeline, and solved the challenges I encountered along the way.

## Why Hugo and GitHub Pages?

Before diving into the technical details, let me explain why I chose this stack:

**Hugo** is a static site generator written in Go that's:
- Incredibly fast (builds in milliseconds)
- Simple to set up and use
- Has a rich ecosystem of themes
- Supports Markdown for content
- Generates SEO-friendly static HTML

**GitHub Pages** is perfect because:
- It's free hosting for public repositories
- Supports custom domains
- Has built-in SSL/TLS certificates
- Integrates seamlessly with GitHub Actions
- Provides excellent performance via CDN

## Project Structure

Here's what the final project structure looks like:

```
rwgb.github.io/
├── .github/
│   └── workflows/
│       └── hugo.yml          # GitHub Actions workflow
├── content/
│   ├── posts/                # Blog posts
│   ├── projects/             # Project showcase
│   ├── about.md             # About page
│   └── contact.md           # Contact page
├── static/                   # Static assets
│   └── img/
├── themes/
│   └── congo/               # Theme (as git submodule)
├── .gitignore
├── .gitmodules
├── hugo.toml                # Hugo configuration
└── README.md
```

## Step 1: Setting Up Hugo

First, I installed Hugo on my Mac using Homebrew:

```bash
brew install hugo
```

Then created a new Hugo site:

```bash
hugo new site personal.site
cd personal.site
```

## Step 2: Adding the Congo Theme

I chose the [Congo theme](https://github.com/jpanther/congo) for its modern design and extensive customization options. I added it as a git submodule:

```bash
git submodule add -b stable https://github.com/jpanther/congo.git themes/congo
```

Using a git submodule is important because it allows the theme to be updated independently while keeping your site's repository clean.

## Step 3: Configuring Hugo

The `hugo.toml` file is where all the magic happens. Here's a breakdown of the key configuration:

```toml
baseURL = 'https://rwgb.github.io/'
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

### Important Configuration Details

**Pagination Update**: I initially used the deprecated `paginate` parameter but had to update it to the new format:
```toml
[pagination]
  pagerSize = 10
```

**Author Configuration**: The Congo theme requires author information in a specific structure:
```toml
[languages.en.params.author]
  name = "Ralph Brynard"
  image = "img/profile.jpg"
  headline = "Developer & Content Creator"
  bio = "Building innovative projects..."
  links = [
    { github = "https://github.com/rwgb" },
    { linkedin = "https://linkedin.com/in/ralphbrynard" }
  ]
```

## Step 4: Creating Content

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
- `content/about.md` - About page
- `content/contact.md` - Contact information

## Step 5: The GitHub Actions Workflow

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
        run: hugo --minify --baseURL "${{ steps.pages.outputs.base_url }}/"
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
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

### Breaking Down the Workflow

**Triggers**: The workflow runs on:
- Every push to the `main` branch
- Manual trigger via `workflow_dispatch`

**Permissions**: Critical for GitHub Pages deployment:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

**Build Job Steps**:
1. **Checkout**: Fetches the repository with `submodules: recursive` (important for the theme!)
2. **Setup Pages**: Configures GitHub Pages settings
3. **Setup Hugo**: Installs Hugo Extended (needed for SCSS/SASS support)
4. **Build**: Runs `hugo --minify` with the correct base URL
5. **Upload**: Creates an artifact from the `public/` directory

**Deploy Job**: 
- Depends on the build job
- Uses the official `actions/deploy-pages@v4` action
- Runs in the `github-pages` environment

## Step 6: GitHub Repository Configuration

Setting up the repository correctly is crucial:

1. **Repository Name**: Must be `username.github.io` (in my case: `rwgb.github.io`)

2. **GitHub Pages Settings**:
   - Go to Settings → Pages
   - Set Source to **"GitHub Actions"** (not "Deploy from a branch")
   - This enables the workflow to deploy

3. **Git Submodules**: Don't forget to initialize and update submodules:
```bash
git submodule init
git submodule update
```

## Challenges I Encountered

### Issue 1: Deprecated Actions
**Problem**: The workflow initially failed with `actions/upload-pages-artifact@v2`

**Solution**: Updated to v3:
```yaml
uses: actions/upload-pages-artifact@v3
```

### Issue 2: Author Configuration
**Problem**: Got errors like "can't evaluate field name in type string"

**Solution**: The theme needed author as an object, not a string:
```toml
# Wrong
author = "Ralph Brynard"

# Correct
[languages.en.params.author]
  name = "Ralph Brynard"
```

### Issue 3: Deployment Failures
**Problem**: "Failed to create deployment (status: 404)"

**Solution**: Had to:
1. Add `actions/configure-pages@v4` step
2. Set GitHub Pages source to "GitHub Actions" in repository settings
3. Update to `actions/deploy-pages@v4`

### Issue 4: Public Directory
**Problem**: The `.gitignore` was ignoring the `public/` directory

**Solution**: This is actually correct! GitHub Actions builds the site fresh on each deployment, so you don't want to commit the generated files.

## Local Development

Testing locally is easy:

```bash
# Start development server
hugo server -D

# Visit http://localhost:1313
```

The `-D` flag includes draft posts. Hugo's live reload makes development a breeze.

## The .gitignore File

Here's my `.gitignore` setup:

```gitignore
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

## Deployment Process

The actual deployment flow:

1. **Push changes** to the `main` branch:
```bash
git add .
git commit -m "Add new blog post"
git push origin main
```

2. **GitHub Actions triggers** automatically

3. **Build process**:
   - Checks out code with submodules
   - Installs Hugo
   - Builds the site with `hugo --minify`
   - Creates deployment artifact

4. **Deploy process**:
   - Takes the artifact
   - Deploys to GitHub Pages
   - Site is live in ~30 seconds!

## Performance and SEO

The resulting site is blazingly fast:
- Static HTML files (no server-side processing)
- Minified assets
- Served via GitHub's CDN
- Automatic HTTPS
- SEO-friendly URLs

## Cost Analysis

Total cost: **$0**

- Hugo: Free and open source
- Congo theme: Free
- GitHub Pages: Free for public repositories
- GitHub Actions: 2,000 minutes/month free (way more than needed)
- SSL Certificate: Included with GitHub Pages

## Tips and Best Practices

1. **Use Extended Hugo**: Many themes require SCSS/SASS support
2. **Submodules for themes**: Keep themes updatable
3. **Test locally first**: Always run `hugo server` before pushing
4. **Meaningful commit messages**: They show up in Actions logs
5. **Use frontmatter consistently**: Makes content management easier
6. **Enable draft mode**: Use `draft: true` for work-in-progress posts

## Useful Commands

```bash
# Create new post
hugo new posts/my-new-post.md

# Build site (output to public/)
hugo

# Build with minification
hugo --minify

# Start dev server with drafts
hugo server -D

# Update theme submodule
git submodule update --remote themes/congo
```

## Future Enhancements

Some ideas I'm considering:

- Add custom domain (easy with GitHub Pages)
- Implement comments system
- Add analytics
- Create custom shortcodes
- Add search functionality
- Implement dark/light theme toggle (Congo has this!)

## Conclusion

Building a personal website with Hugo and GitHub Pages is an excellent choice for developers who want:
- Complete control over their content
- Fast, reliable hosting
- Automated deployments
- Zero hosting costs
- Modern development workflow

The initial setup takes a bit of configuration, but once it's running, publishing new content is as simple as writing Markdown and pushing to GitHub.

The combination of Hugo's speed, Congo theme's beautiful design, and GitHub Actions' automation creates a powerful, maintainable platform for sharing your work with the world.

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Congo Theme](https://github.com/jpanther/congo)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [My GitHub Repository](https://github.com/rwgb/rwgb.github.io)

Feel free to fork my repository and use it as a starting point for your own site. If you run into any issues or have questions, reach out on GitHub!

---

*This site was built with Hugo, themed with Congo, and deployed via GitHub Actions. The source code is available on [GitHub](https://github.com/rwgb/rwgb.github.io).*
