package main

import (
	"encoding/json"
	"fmt"
	"github.com/gorilla/feeds"
	"io/ioutil"
	"log"
	"time"
)

type NewsPosts []struct {
	Title       string `json:"title"`
	Author      string `json:"author"`
	Date        string `json:"date"`
	URL         string `json:"url"`
	Description string `json:"description"`
}

const (
	jsonFile         = "posts.json"
	timeZoneLocation = "America/Los_Angeles"
)

func main() {
	jsonFile, err := ioutil.ReadFile(jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	var posts NewsPosts
	if err := json.Unmarshal(jsonFile, &posts); err != nil {
		log.Fatal(err)
	}

	feed := buildFeed(&posts)
	atom, err := feed.ToAtom()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(atom)
}

func buildFeed(posts *NewsPosts) *feeds.Feed {
	feed := &feeds.Feed{
		Title:       "Overwatch PC Updates",
		Link:        &feeds.Link{Href: "https://playoverwatch.com/en-us/game/patch-notes/pc/"},
		Description: "Patch notes and updates for Overwatch",
		Author:      &feeds.Author{Name: "Blizzard"},
		Created:     time.Now(),
	}

	layout := "January 2, 2006"
	default_timestamp := time.Unix(0, 0) // Use unix time 0 by default
	for _, post := range *posts {
		item := &feeds.Item{
			Title:       post.Title,
			Link:        &feeds.Link{Href: post.URL},
			Description: post.Description,
			Author:      &feeds.Author{Name: post.Author},
			Created:     default_timestamp,
		}
		if post.Date != "" {
			// valid date was parsed
			loc, err := time.LoadLocation(timeZoneLocation)
			if err == nil {
				t, err := time.ParseInLocation(layout, post.Date, loc)
				if err == nil {
					item.Created = t
				}
			}
		}
		feed.Items = append(feed.Items, item)
	}
	return feed
}
