from selenium import webdriver
import bs4
import json
import subprocess


def main():
    chart_list_url = "https://textage.cc/score/?sC11B000"  # all level 12 charts
    web = webdriver.Chrome()
    web.get(chart_list_url)
    soup = bs4.BeautifulSoup(markup=web.page_source, features="html.parser")
    results = []
    for row in soup.select("tr"):
        title_element = row.select_one('td[class="tt1"]')
        if title_element is None:
            continue
        title = title_element.get_text()
        for chart_link in row.select("a"):
            if chart_link.get_text() != "1P":
                continue
            chart_url = chart_link.get("href")
            if "?1X" in chart_url:
                difficulty = "leggendaria"
            elif "?1A" in chart_url:
                difficulty = "another"
            elif "?1H" in chart_url:
                difficulty = "hyper"
            elif "?1N" in chart_url:
                difficulty = "normal"
            elif "?1P" in chart_url:
                difficulty = "beginner"
            else:
                difficulty = "unknown"
            print(f"found a 1P chart for {title} ({difficulty}) at {chart_link.get('href')}")
            full_url = f"https://textage.cc/score/{chart_url}"
            results.append({
                "title": title,
                "difficulty": difficulty,
                "full_url": full_url,
                "file_key": chart_url[chart_url.find("/") + 1:].replace(".html?", ""),
            })
    with open("charts_info.json", "w") as f:
        json.dump(results, f)
    for item in results:
        subprocess.call(["python", "gen_npy.py", item["full_url"]])


if __name__ == "__main__":
    main()
