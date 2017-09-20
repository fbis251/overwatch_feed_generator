# Overwatch Atom Feed Generator

This project uses [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) to scrape the [Overwatch PC patch notes page](https://playoverwatch.com/en-us/game/patch-notes/pc/) to generate an Atom feed using [gorilla/feeds](https://github.com/gorilla/feeds)

An example systemd service that runs the feed generator once per hour is included. If you're going to use the service make sure you update the paths in the `ExecStart` and `WorkingDirectory` variables to where you installed this project

## Installation

Install using go get
```bash
go get -u github.com/fbis251/overwatch_feed_generator
```

## Usage

Once installed, run the `get.sh` script to generate the `pc.atom` file containing the Atom feed created from the patch notes page

```bash
cd $GOPATH/github.com/fbis251/overwatch_feed_generator
./get.sh
less pc.atom
```

## Demo

You can see a hosted version of the generated feed on [my github site](https://fbis251.github.io/overwatch_news_feed/pc.atom)
