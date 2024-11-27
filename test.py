import praw

reddit = praw.Reddit(
    client_id="WB7MVXKOsVqF-DVR-jtcRg",
    client_secret="f78PlFxDGY_w-foXoQPWv7mlZcoAdQ",
    user_agent="android:com.example.myredditapp:v1.2.3",
)
print(reddit.read_only)

# continued from code above

# for submission in reddit.subreddit("stardewvalley").hot(limit=10):
#     print(submission)
#     print(submission.title)
#     print(submission.selftext)

test = reddit.submission("1h0133r")
print(f"Title: {test.title}")
print(f"Selftext: {test.selftext}")

# Check if the specific submission is an image
if test.post_hint == "image":
    print(f"Image URL: {test.url}")
else:
    print("No image associated with this post.")

# Output: 10 submissions