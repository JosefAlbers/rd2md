# Reddit to Markdown Scraper

This Python script uses PRAW (Python Reddit API Wrapper) to scrape interesting posts from a specified subreddit and save them in a formatted Markdown file. It also downloads and saves images associated with the posts.

## Features

- Scrapes hot posts from a specified subreddit
- Filters posts based on score and whether they're stickied
- Downloads and saves images from posts
- Formats post content, including comments, into a Markdown file
- Handles both text posts and image posts
- Can be used as a standalone script or imported as a module

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/JosefAlbers/rd2md.git
   cd rd2md
   ```

2. Install the required packages:
   ```
   pip install praw requests
   ```

## Setup

To use this script, you need to create a Reddit application to get the necessary credentials:

1. Log in to your Reddit account
2. Go to https://www.reddit.com/prefs/apps
3. Scroll down and click "create another app..."
4. Fill out the form:
   - Choose a name for your application
   - Select "script" as the app type
   - For "redirect uri", use http://localhost:8080
   - Add a description (optional)
5. Click "create app"

After creating the app, note down the following:
- client_id: The string under "personal use script"
- client_secret: The string next to "secret"

## Usage

### As a Standalone Script

You can run the script from the command line with the following syntax:

```
python rd2md.py --client_id=YOUR_CLIENT_ID --client_secret=YOUR_CLIENT_SECRET [options]
```

Options:
- `--client_id`: Your Reddit API client ID (required if not set as an environment variable)
- `--client_secret`: Your Reddit API client secret (required if not set as an environment variable)
- `--user_agent`: User agent for Reddit API (default: "praw_bot")
- `--subreddit`: Subreddit to scrape (default: "LocalLLaMA")
- `--limit`: Number of posts to scrape (default: 50)

Example:
```
python rd2md.py --client_id=YOUR_CLIENT_ID --client_secret=YOUR_CLIENT_SECRET --subreddit=ProgrammingHumor --limit=10
```

Note: If your client secret contains special characters (like hyphens), use the `=` sign to assign the value as shown above.

### As an Importable Module

You can also use the script as a module in your Python code:

```python
from rd2md import get_reddit_instance, save_to_markdown

# Create a Reddit instance
reddit = get_reddit_instance("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")

# Scrape and save posts
save_to_markdown(reddit, "ProgrammingHumor", limit=10)
```

### Using Environment Variables

Instead of passing the client ID and secret as arguments, you can set them as environment variables:

```
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret
```

Then you can run the script without these arguments:

```
python rd2md.py --subreddit=ProgrammingHumor --limit=10
```

## Output

The script creates a new directory named `{subreddit}_posts_{date}` in the current working directory. This directory contains:

- A Markdown file named `interesting_posts.md` with the scraped post content
- An `images` subdirectory containing any downloaded images

![Alt text](https://raw.githubusercontent.com/JosefAlbers/rd2md/main/assets/example_output.png)

## Customization

You can modify the `is_interesting` function in the script to change the criteria for which posts are considered interesting:

```python
def is_interesting(post):
    return post.score > 100 and not post.stickied
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
