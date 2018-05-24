# wiki firefox history tweets

This is my first python project. It looks into the user firefox history, filters
for Wikipedia entries and then tweets about them. The twitter account where those
tweets are posted is https://twitter.com/caioleusobre

I'm sure there are more elegant and efficient ways to implement this.

## Details

There are three .py files.

The first one (past_wiki_history_tweeter.py) code looks into the firefox history
and tweets about past wikipedia accesses from time to time (3 to 4 hours between tweets).

The second one (real_time_wiki_tweeter.py) "polls" firefox history for new
wikipedia entries and tweets about about these "real time" accesses.

The last one (wiki_reader_bot.py) combines the two and while it is running, it
tweets about past entries from time to time and instantly tweets about real time
accesses on wikipedia.

All those use the 'tweets.txt' to avoid repeating tweets.

## Notes

I believe this can be easily modified to be used with chrome or any other browser,
also could be used to tweet about whatever is in the browser's history.
This can be achieved by modifying 'history_db' and 'select_statement', then
adjusting the building of the sentence to be tweeted.

## Acknowledgments

This was made taking heavily from https://geekswipe.net/technology/computing/analyze-chromes-browsing-history-with-python/
