# Jekyll Blog with Streamlit Admin

A minimalist Jekyll blog with a Streamlit admin interface for easy content management. This blog features a clean, markdown-inspired design with automatic GitHub Pages deployment.

## Features

- 🎨 Clean, minimal design
- 📱 Fully responsive
- 🌓 Dark/light mode
- ✍️ Streamlit admin panel
- 🚀 Automatic GitHub Pages deployment
- 📝 Markdown support
- 🔄 Automatic git push on content updates

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/blog.git
cd blog
```

2. Install Jekyll dependencies:
```bash
gem install jekyll bundler
bundle init
bundle add jekyll
bundle install
```

3. Install Python dependencies for admin panel:
```bash
cd admin
pip install -r requirements.txt
```

## Local Development

1. Start Jekyll server:
```bash
bundle exec jekyll serve
```
Your blog will be available at `http://localhost:4000`

2. Start Streamlit admin panel (in a new terminal):
```bash
cd admin
streamlit run app.py
```
The admin interface will be available at `http://localhost:8501`

## GitHub Pages Setup

1. Update `_config.yml`:
```yaml
baseurl: "/blog"  # Replace with your repository name
url: "https://YOUR_USERNAME.github.io"
title: "Your Blog Title"
author: "Your Name"
```

2. Enable GitHub Pages:
- Go to your repository settings
- Navigate to "Pages"
- Select "GitHub Actions" as the source
- The site will be available at `https://YOUR_USERNAME.github.io/blog`

## File Structure

```
blog/
├── _posts/          # Blog posts
├── _layouts/        # HTML layouts
├── _includes/       # Reusable components
├── assets/
│   └── css/        # Stylesheets
├── admin/          # Streamlit admin panel
├── _config.yml     # Jekyll configuration
└── index.md        # Homepage
```

## Creating Posts

You can create posts in two ways:

1. Using the Streamlit admin panel:
   - Navigate to `http://localhost:8501`
   - Click "Create Post"
   - Fill in the title and content
   - Changes will be automatically pushed to GitHub

2. Manually:
   - Create a new file in `_posts/` with format `YYYY-MM-DD-title.md`
   - Add front matter and content
   - Commit and push to GitHub

## Customization

- Edit `assets/css/style.css` to modify the design
- Update `_layouts/default.html` for layout changes
- Modify `_includes/navigation.html` for navigation links

## License

This project is open source and available under the [MIT License](LICENSE).