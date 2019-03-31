package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/gorilla/feeds"
	"io/ioutil"
	"log"
	"os"
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
	defaultJsonFile       = "posts.json"
	defaultAtomFile       = "posts.atom"
	defaultLatestPostFile = ".latest_post_parsed"
	timeZoneLocation      = "America/Los_Angeles"
)

var (
	jsonFile       = flag.String("i", defaultJsonFile, "The JSON file to read posts from")
	atomFile       = flag.String("o", defaultAtomFile, "The file to write the ATOM feed to")
	latestPostFile = flag.String("l", defaultLatestPostFile, "The file to write the title of the most recent post to")
)

func main() {
	flag.Parse()
	fmt.Printf("Reading posts from: %s\n", *jsonFile)
	fmt.Printf("Writing feed to: %s\n", *atomFile)
	fmt.Printf("Writing latest post title to: %s\n", *latestPostFile)
	jsonFile, err := ioutil.ReadFile(*jsonFile)
	if err != nil {
		log.Fatal(err)
	}

	var posts NewsPosts
	if err := json.Unmarshal(jsonFile, &posts); err != nil {
		log.Fatal(err)
	}

	feed := buildFeed(&posts)
	err = writeAtomFile(feed)
	if err != nil {
		log.Fatal(err)
	}
}

func buildFeed(posts *NewsPosts) *feeds.Feed {
	feed := &feeds.Feed{
		Title:       "Overwatch PC Updates",
		Link:        &feeds.Link{Href: "https://playoverwatch.com/en-us/game/patch-notes/pc/"},
		Description: "Patch notes and updates for Overwatch",
		Author:      &feeds.Author{Name: "Blizzard"},
		Created:     time.Now(),
	}

	isLatestPostTimeWritten := false
	layout := "1/2/2006"
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
			if err != nil {
				log.Fatal(err)
			}
			t, err := time.ParseInLocation(layout, post.Date, loc)
			if err != nil {
				log.Fatal(err)
			}
			item.Created = t
		}

		if !isLatestPostTimeWritten {
			writeLatestPostFile(string(item.Title) + " - " + string(post.Date))
			isLatestPostTimeWritten = true
		}

		feed.Items = append(feed.Items, item)
	}
	return feed
}

func writeAtomFile(feed *feeds.Feed) error {
	atom, err := feed.ToAtom()
	if err != nil {
		return err
	}
	return writeStringToFile(atom, *atomFile)
}

func writeLatestPostFile(contents string) error {
	return writeStringToFile(contents, *latestPostFile)
}

func writeStringToFile(str string, filename string) error {
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()
	w := bufio.NewWriter(f)
	fmt.Fprint(w, str)
	w.Flush()

	return nil
}
