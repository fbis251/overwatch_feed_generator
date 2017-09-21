#!/bin/bash
set -eu
BASE_PATH="$HOME/go/src/github.com/fbis251/overwatch_feed_generator"
RSS_REPO_PATH="$HOME/src/overwatch_news_feed"
POSTS_URL="https://playoverwatch.com/en-us/game/patch-notes/pc/"
POSTS_HTML="$BASE_PATH/posts.html"
JSON_FILE="$BASE_PATH/posts.json"
ATOM_FILE="$RSS_REPO_PATH/pc.atom"
LATEST_POST_PARSED="$BASE_PATH/.latest_post_parsed"
LATEST_POST_COMMITTED="$RSS_REPO_PATH/.latest_post_committed"

cd "$BASE_PATH"
echo 'Downloading new posts page'
curl -s "$POSTS_URL" -H 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' > "$POSTS_HTML"
echo 'Parsing HTML and exporting posts JSON'
python soup.py > "$JSON_FILE"
echo 'Parsing posts JSON and writing Atom feed'
go run main.go -i "$JSON_FILE" -o "$ATOM_FILE" -l "$LATEST_POST_PARSED"
rm "$POSTS_HTML" "$JSON_FILE"
echo 'Done writing Atom feed'

echo
echo 'Checking if git commit is needed'
cd "$RSS_REPO_PATH"
touch "$LATEST_POST_COMMITTED"

if cmp -s "$LATEST_POST_PARSED" "$LATEST_POST_COMMITTED"; then
    echo 'No new commit needed'
else
    latest_parsed=$(cat "$LATEST_POST_PARSED")
    latest_committed=$(cat "$LATEST_POST_COMMITTED")
    echo "Latest parsed post:    $latest_parsed"
    echo "Latest committed post: $latest_committed"
    echo 'Creating new commit'
    cp "$LATEST_POST_PARSED" "$LATEST_POST_COMMITTED"
    git add "$ATOM_FILE" "$LATEST_POST_COMMITTED"
    git commit -m "$latest_parsed"
    git push origin master
fi

rm "$LATEST_POST_PARSED"
echo 'Done generating feed'
