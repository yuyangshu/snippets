using System;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace Symonitor.SearchEngineScrapers
{
    public class GoogleScraper : ISearchEngineScraper
    {
        const string UrlPattern = "https://www.google.com/search?q={0}&num=100";
        // not all results are web pages, this only matches the most common format; can be refined further
        const string PagePattern = @"(?<=div class=""yuRUbf""><a href="")[^ ]+(?="" onmousedown)";
        static readonly HttpClient HttpClient;

        static GoogleScraper()
        {
            HttpClient = new HttpClient();
            HttpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0");
        }

        public async Task<int> SearchKeywordsAndCountUrlOccurrences(string keywords, string urlToCount)
        {
            // spaces in urls seems to work for google
            var targetUrl = String.Format(UrlPattern, keywords);

            using (var result = await HttpClient.GetAsync(targetUrl))
            {
                if (result.IsSuccessStatusCode)
                {
                    return CountOccurenceOfUrl(await result.Content.ReadAsStringAsync(), urlToCount);
                }
            }

            return 0;
        }

        int CountOccurenceOfUrl(string htmlContent, string urlToCount)
        {
            // without a proper (third-party) html parser, have to resort to a hacky solution
            var entryPattern = new Regex(PagePattern);

            var count = 0;
            foreach (Match match in entryPattern.Matches(htmlContent))
            {
                if (match.Value.Contains(urlToCount))
                {
                    count += 1;
                }
            }

            return count;
        }
    }
}