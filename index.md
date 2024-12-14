---
layout: default
title: Blog Posts
---
# Blogs

{% for post in site.posts %}
<article class="post-preview">
    <h2 class="post-title">
        <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
    </h2>
    <div class="post-meta">{{ post.date | date: "%B %d, %Y" }}</div>
    <div class="post-excerpt">
        {{ post.excerpt | strip_html | truncatewords: 30 }}
        <a href="{{ site.baseurl }}{{ post.url }}" class="read-more">Read more →</a>
    </div>
</article>
{% endfor %}