from tracker_scraper import scrape

results = scrape(
    tracker="udp://explodie.org:6969",
    hashes=[
        "82026E5C56F0AEACEDCE2D7BC2074A644BC50990",
        "04D9A2D3FAEA111356519A0E0775E5EAEE9C944A",
    ],
)

print(results)
