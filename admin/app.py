# admin/app.py
import streamlit as st
import os
import datetime
import yaml
from pathlib import Path
import re
import subprocess

class BlogManager:
    def __init__(self):
        self.posts_dir = Path("../_posts")
        self.posts_dir.mkdir(exist_ok=True)

    def create_post(self, title, content):
        slug = self._create_slug(title)
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = f"{date}-{slug}.md"
        
        front_matter = {
            'layout': 'post',
            'title': title,
            'date': date,
        }
        
        post_content = f"""---
{yaml.dump(front_matter)}---

{content}"""
        
        post_path = self.posts_dir / filename
        post_path.write_text(post_content)
        return True

    def get_all_posts(self):
        posts = []
        for post_file in self.posts_dir.glob("*.md"):
            content = post_file.read_text()
            # Split front matter and content
            parts = content.split("---", 2)
            if len(parts) >= 3:
                front_matter = yaml.safe_load(parts[1])
                post_content = parts[2].strip()
                posts.append({
                    'filename': post_file.name,
                    'title': front_matter.get('title', ''),
                    'date': front_matter.get('date', ''),
                    'content': post_content
                })
        return sorted(posts, key=lambda x: x['date'], reverse=True)

    def update_post(self, filename, title, content):
        post_path = self.posts_dir / filename
        date = self._extract_date(filename)
        
        front_matter = {
            'layout': 'post',
            'title': title,
            'date': date,
        }
        
        post_content = f"""---
{yaml.dump(front_matter)}---

{content}"""
        
        post_path.write_text(post_content)
        return True

    def delete_post(self, filename):
        try:
            post_path = self.posts_dir / filename
            if post_path.exists():
                post_path.unlink()
                return True
            return False
        except Exception as e:
            st.error(f"Error deleting file: {e}")
            return False

    def _create_slug(self, title):
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug

    def _extract_date(self, filename):
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        return date_match.group(1) if date_match else datetime.datetime.now().strftime('%Y-%m-%d')

def push_to_github():
    try:
        # Change to the root directory of the blog
        os.chdir('..')
        
        # Add all changes including deletions
        subprocess.run(['git', 'add', '--all'], check=True)
        
        # Create commit
        subprocess.run(['git', 'commit', '-m', 'Updated blog posts'], check=True)
        
        # Push changes
        subprocess.run(['git', 'push'], check=True)
        
        # Change back to admin directory
        os.chdir('admin')
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Git command failed: {e}")
        os.chdir('admin')  # Ensure we return to admin directory
        return False
    except Exception as e:
        st.error(f"Error pushing to GitHub: {e}")
        os.chdir('admin')  # Ensure we return to admin directory
        return False

def main():
    st.set_page_config(page_title="Blog Admin", layout="wide")
    
    blog_manager = BlogManager()
    
    st.title("Blog Admin Panel")
    
    # Sidebar for navigation
    page = st.sidebar.radio("Select Operation", ["Create Post", "Manage Posts"])
    
    if page == "Create Post":
        st.header("Create New Post")
        
        title = st.text_input("Post Title")
        content = st.text_area("Post Content (Markdown)", height=300)
        
        if st.button("Create Post", type="primary"):
            if title and content:
                if blog_manager.create_post(title, content):
                    st.success("Post created successfully!")
                    if push_to_github():
                        st.success("Changes pushed to GitHub!")
                    st.balloons()
            else:
                st.error("Please fill in both title and content")

    else:  # Manage Posts
        st.header("Manage Existing Posts")
        
        posts = blog_manager.get_all_posts()
        
        for post in posts:
            with st.expander(f"📝 {post['title']} ({post['date']})"):
                # Create columns for the edit form
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    edited_title = st.text_input(
                        "Edit Title", 
                        value=post['title'],
                        key=f"title_{post['filename']}"
                    )
                    edited_content = st.text_area(
                        "Edit Content", 
                        value=post['content'],
                        height=200,
                        key=f"content_{post['filename']}"
                    )
                
                with col2:
                    if st.button("💾 Save Changes", key=f"save_{post['filename']}"):
                        if blog_manager.update_post(post['filename'], edited_title, edited_content):
                            st.success("Post updated!")
                            if push_to_github():
                                st.success("Changes pushed to GitHub!")
                            st.rerun()
                    
                    if st.button("🗑️ Delete Post", key=f"delete_{post['filename']}", type="secondary"):
                        if st.checkbox("Confirm deletion?", key=f"confirm_{post['filename']}"):
                            if blog_manager.delete_post(post['filename']):
                                st.success("Post deleted!")
                                if push_to_github():
                                    st.success("Changes pushed to GitHub!")
                                st.rerun()

if __name__ == "__main__":
    main()