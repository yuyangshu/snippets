using System;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace Symonitor.SearchEngineScrapers
{
    public class GoogleScraper : ISearchEngineScraper
    {
        const string UrlPattern = "https://www.google.com/search?q={0}&num=100";
        const string PagePattern = @"(?<=div class=""yuRUbf""><a href="")[^ ]+(?="" onmousedown)";
        static readonly HttpClient _httpClient;
        private readonly ILogger<GoogleScraper> _logger;

        static GoogleScraper()
        {
            // TODO wrap HttpClient to test SearchKeywordsAndCountUrlAppearances()
            _httpClient = new HttpClient();
            _httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0");
        }

        public GoogleScraper(ILogger<GoogleScraper> logger)
        {
            _logger = logger;
        }

        public async Task<int> SearchKeywordsAndCountUrlAppearances(string keywords, string urlToCount, CancellationToken cancellationToken)
        {
            var targetUrl = String.Format(UrlPattern, keywords);

            try
            {
                using (var result = await _httpClient.GetAsync(targetUrl, cancellationToken))
                {
                    if (result.IsSuccessStatusCode)
                    {
                        return CountOccurenceOfUrl(await result.Content.ReadAsStringAsync(), urlToCount);
                    }

                    return 0;
                }
            }
            catch (InvalidOperationException ex)
            {
                _logger.LogError(ex, $"Invalid URL {targetUrl}");
                throw ex;
            }
            catch (HttpRequestException ex)
            {
                _logger.LogInformation(ex, $"Network issue when trying to fetch {targetUrl}");
                return 0;
            }
            catch (TaskCanceledException ex)
            {
                _logger.LogInformation(ex, $"Timeout when fetching {targetUrl}");
                return 0;
            }
        }

        // a (3rd party) html parser is needed to have a less hacky solution; PagePattern does not match all results
        public static int CountOccurenceOfUrl(string htmlContent, string urlToCount)
        {
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
