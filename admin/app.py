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
        
        # Create proper YAML front matter
        front_matter = {
            'layout': 'post',
            'title': title,
            'date': date
        }
        
        # Ensure proper YAML formatting with dashes
        post_content = "---\n"
        post_content += yaml.dump(front_matter, default_flow_style=False, sort_keys=False)
        post_content += "---\n\n"
        post_content += content
        
        post_path = self.posts_dir / filename
        post_path.write_text(post_content)
        self._git_push(f"Add post: {filename}")
        return True

    def get_all_posts(self):
        posts = []
        for post_file in self.posts_dir.glob("*.md"):
            try:
                content = post_file.read_text()
                # Split content at the first and second '---'
                parts = content.split("---", 2)
                
                if len(parts) >= 3:
                    # Remove any leading/trailing whitespace from the YAML part
                    yaml_content = parts[1].strip()
                    try:
                        front_matter = yaml.safe_load(yaml_content)
                        if front_matter is None:
                            front_matter = {}
                        post_content = parts[2].strip()
                        posts.append({
                            'filename': post_file.name,
                            'title': front_matter.get('title', ''),
                            'date': front_matter.get('date', ''),
                            'content': post_content
                        })
                    except yaml.YAMLError as e:
                        st.error(f"Error parsing YAML in {post_file.name}: {e}")
            except Exception as e:
                st.error(f"Error reading {post_file.name}: {e}")
                continue
        return sorted(posts, key=lambda x: x['date'], reverse=True)

    def update_post(self, filename, title, content):
        post_path = self.posts_dir / filename
        date = self._extract_date(filename)
        
        # Create proper YAML front matter
        front_matter = {
            'layout': 'post',
            'title': title,
            'date': date
        }
        
        # Ensure proper YAML formatting with dashes
        post_content = "---\n"
        post_content += yaml.dump(front_matter, default_flow_style=False, sort_keys=False)
        post_content += "---\n\n"
        post_content += content
        
        post_path.write_text(post_content)
        self._git_push(f"Update post: {filename}")
        return True

    def delete_post(self, filename):
        try:
            post_path = self.posts_dir / filename
            if post_path.exists():
                post_path.unlink()
                self._git_push(f"Delete post: {filename}")
                return True
            return False
        except Exception as e:
            st.error(f"Error deleting post: {e}")
            return False

    def _create_slug(self, title):
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug

    def _extract_date(self, filename):
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        return date_match.group(1) if date_match else datetime.datetime.now().strftime('%Y-%m-%d')

    def _git_push(self, commit_message):
        try:
            # Store current directory
            original_dir = os.getcwd()
            
            # Change to repository root
            os.chdir('..')
            
            # Git operations
            subprocess.run(['git', 'add', '-A'], check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            # Return to original directory
            os.chdir(original_dir)
            return True
        except Exception as e:
            if original_dir != os.getcwd():
                os.chdir(original_dir)
            st.error(f"Git error: {e}")
            return False

def main():
    st.set_page_config(page_title="Blog Admin", layout="wide")
    
    blog_manager = BlogManager()
    
    st.title("Blog Admin Panel")
    
    if 'delete_confirm' not in st.session_state:
        st.session_state.delete_confirm = {}
    
    page = st.sidebar.radio("Select Operation", ["Create Post", "Manage Posts"])
    
    if page == "Create Post":
        st.header("Create New Post")
        
        title = st.text_input("Post Title")
        content = st.text_area("Post Content (Markdown)", height=300)
        
        if st.button("Create Post", type="primary"):
            if title and content:
                if blog_manager.create_post(title, content):
                    st.success("Post created and pushed to GitHub!")
                    st.balloons()
            else:
                st.error("Please fill in both title and content")

    else:
        st.header("Manage Existing Posts")
        
        posts = blog_manager.get_all_posts()
        
        for post in posts:
            with st.expander(f"📝 {post['title']} ({post['date']})"):
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
                            st.success("Post updated and pushed to GitHub!")
                            st.rerun()
                    
                    delete_key = f"delete_{post['filename']}"
                    if delete_key not in st.session_state.delete_confirm:
                        st.session_state.delete_confirm[delete_key] = False
                    
                    if st.button("🗑️ Delete Post", key=delete_key):
                        st.session_state.delete_confirm[delete_key] = True
                    
                    if st.session_state.delete_confirm[delete_key]:
                        st.warning("Are you sure you want to delete this post?")
                        col3, col4 = st.columns(2)
                        with col3:
                            if st.button("✅ Yes", key=f"yes_{post['filename']}"):
                                if blog_manager.delete_post(post['filename']):
                                    st.success("Post deleted and pushed to GitHub!")
                                    st.session_state.delete_confirm[delete_key] = False
                                    st.rerun()
                        with col4:
                            if st.button("❌ No", key=f"no_{post['filename']}"):
                                st.session_state.delete_confirm[delete_key] = False
                                st.rerun()

if __name__ == "__main__":
    main()