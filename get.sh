#!/bin/bash
set -eu
POSTS_URL="https://playoverwatch.com/en-us/game/patch-notes/pc/"
ATOM_FILE="pc.atom"
POSTS_HTML="posts.html"
JSON_FILE="posts.json"

set -x
curl -s $POSTS_URL -H "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0" > $POSTS_HTML
python soup.py > $JSON_FILE
go run main.go > $ATOM_FILE

rm $POSTS_HTML $JSON_FILE
