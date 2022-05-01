# Human-made Climate Change discussion on Reddit

## ❓ How to

### Develop

Installing Hugo: 
> MacOS: ```brew install hugo```


> Windows: https://www.techielass.com/how-to-install-hugo-on-windows-10/

If you managed to install Hugo on your machine ([official guide](https://gohugo.io/getting-started/installing/) or an alternative for [Windows](https://www.techielass.com/how-to-install-hugo-on-windows-10/) users), and cloned the repo, you can run `hugo serve`. At this point, you can surf your website from a browser at: [http://localhost:1313/](http://localhost:1313/).

When you commit changes to the main branch, a job (which runs using Github Actions) will build a new copy of your website and publish it on Github Actions. You might need to check the repo settings (under the 'Pages' tab).

### Add new content

In the `content/` folder you can find several markdown files. `_index.md` would be your homepage. Therefore, you are free to create new markdown files. You need to make sure to include these fields in the beginning of your file:

```markdown
---
title: Page title
prev: link-prev-page
next: link-next page
---
```

Whereas, `prev` and `next` are the link to the pages displayed at the bottom of the page. If omitted, no link is going to be displayed!

Please, check the examples provided and the source code. By using Markdown you will be able to include:

* Formatted text (bold, italic)
* Images
* Tables
* Math formula
* Code
* Quotes
* Lists

### Update `config.toml`

The [`config.toml`](https://github.com/peterampazzo/project-website-template/blob/main/config.toml) file contains many variables related to your project. Here you can update much information such as: Project title, Authors, Links, Navbar. The changes are propagated and displayed automatically on every page you've created.

Make sure to update the `baseUrl` variable! This variable is extremely important for publishing the website on Github Pages. The variable should follow this format `https://<github_username>.github.io/<repo_name>`.

### Assets 

Images and other files can also make public together with the website. They must be stored in the `static/` folder. You may find already the DTU logo saved there. Also, you can export your Jupyter notebook and save it as an HTML file (`File > Export Notebook as > HTML`) and save it there. This way you can publish [your code](https://peterampazzo.github.io/project-website-template/explainer-notebook.html).

### Build and deploy

At every change committed to the `main` branch a job running using Github Actions will build and deploy your website on Github Actions. The [job workflow](https://github.com/peterampazzo/project-website-template/blob/main/.github/workflows/gh-pages.yml) is written in YAML, you shouldn't need to apply any changes. It is triggered every time a new commit is pushed to the `main` branch, and it builds and publishes a new version of the website on the `gh-pages` branch.

The website URL is going to be live at: `https://<github_username>.github.io/<repo_name>`.
Please make sure to check the repository settings, you would need to enable Github Pages: `Settings > Pages`. In `Source` select `gh-pages` as branch and keep `/ (root)` as directory. Click on Save 😉

## Tech stuff 🤠

This template has been built on top of [Minimal Blog](https://github.com/tailwindtoolbox/Minimal-Blog) and wrapped into a [Hugo](https://gohugo.io/) website. 

Some of the technologies used are:
* [Hugo](https://gohugo.io/)
* [Tailwind CSS](https://tailwindcss.com/)
* [MathJax](https://www.mathjax.org/)
* [Feather Icons](https://feathericons.com/)
