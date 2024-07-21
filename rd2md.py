import praw
import markdown
import os
import requests
from datetime import datetime
from urllib.parse import urlparse
import re
import textwrap
import argparse

def get_reddit_instance(client_id=None, client_secret=None, user_agent="praw_bot"):
    client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
    client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = user_agent or os.getenv("REDDIT_USER_AGENT", "praw_bot")

    if not client_id or not client_secret:
        raise ValueError("Client ID and Client Secret must be provided either as arguments or environment variables.")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def is_interesting(post):
    return post.score > 100 and not post.stickied

def is_image_url(url):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    parsed = urlparse(url)
    return parsed.path.lower().endswith(image_extensions)

def download_image(url, folder):
    try:
        if not url.startswith('http'):
            return None
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(folder, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
    except requests.exceptions.RequestException:
        print(f"Failed to download image from {url}")
    return None

def extract_image_urls(text):
    pattern = r'\[.*?\]\((https?://\S+\.(?:jpg|jpeg|png|gif))\)'
    return re.findall(pattern, text)

def format_comment(comment, depth=0):
    indent = "  " * depth
    author_line = f"{indent}- u/{comment.author}:\n"

    dedented_body = textwrap.dedent(comment.body).strip()
    indented_body = textwrap.indent(dedented_body, indent + '  ')
    comment_block = f"{indent + '  '}```\n{indented_body}\n{indent + '  '}```\n\n"

    formatted = author_line + comment_block

    for reply in comment.replies:
        formatted += format_comment(reply, depth + 1)

    return formatted

def save_to_markdown(reddit, subreddit_name, limit=3):
    subreddit = reddit.subreddit(subreddit_name)
    interesting_posts = []

    for post in subreddit.hot(limit=None):
        if is_interesting(post):
            interesting_posts.append(post)
            if len(interesting_posts) == limit:
                break

    if interesting_posts:
        date_str = datetime.now().strftime('%Y-%m-%d')
        base_folder = f"{subreddit_name}_posts_{date_str}"
        os.makedirs(base_folder, exist_ok=True)
        images_folder = os.path.join(base_folder, "images")
        os.makedirs(images_folder, exist_ok=True)

        filename = os.path.join(base_folder, f"interesting_posts.md")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Interesting posts from r/{subreddit_name}\n\n")
            for post in interesting_posts:
                f.write(f"## {post.title}\n\n")
                f.write(f"* Score: {post.score}\n")
                f.write(f"* Author: u/{post.author}\n")
                f.write(f"* URL: {post.url}\n\n")

                if post.is_self:
                    content = post.selftext
                    image_urls = extract_image_urls(content)
                    for img_url in image_urls:
                        local_path = download_image(img_url, images_folder)
                        if local_path:
                            relative_path = os.path.relpath(local_path, base_folder)
                            content = content.replace(img_url, relative_path)
                    f.write(f"{content}\n\n")
                elif is_image_url(post.url):
                    local_path = download_image(post.url, images_folder)
                    if local_path:
                        relative_path = os.path.relpath(local_path, base_folder)
                        f.write(f"![Post Image]({relative_path})\n\n")
                else:
                    f.write(f"[Link to content]({post.url})\n\n")

                if post.thumbnail and post.thumbnail.startswith('http'):
                    local_path = download_image(post.thumbnail, images_folder)
                    if local_path:
                        relative_path = os.path.relpath(local_path, base_folder)
                        f.write(f"Thumbnail: ![Thumbnail]({relative_path})\n\n")

                f.write("### Comments:\n\n")
                post.comments.replace_more(limit=None)
                for comment in post.comments:
                    f.write(format_comment(comment))

                f.write("---\n\n")

        print(f"Saved interesting posts to {filename}")
    else:
        print("No interesting posts found.")

def main():
    parser = argparse.ArgumentParser(description="Reddit Scraper Bot")
    parser.add_argument("--client_id", help="Reddit API client ID")
    parser.add_argument("--client_secret", help="Reddit API client secret")
    parser.add_argument("--user_agent", default="praw_bot", help="User agent for Reddit API")
    parser.add_argument("--subreddit", default="LocalLLaMA", help="Subreddit to scrape")
    parser.add_argument("--limit", type=int, default=3, help="Number of posts to scrape")
    args = parser.parse_args()

    reddit = get_reddit_instance(args.client_id, args.client_secret, args.user_agent)
    save_to_markdown(reddit, args.subreddit, args.limit)

if __name__ == "__main__":
    main()
