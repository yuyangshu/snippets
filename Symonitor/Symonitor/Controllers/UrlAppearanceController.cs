using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Symonitor.Models;
using Symonitor.Options;
using Symonitor.SearchEngineScrapers;

namespace Symonitor.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UrlAppearanceController : ControllerBase
    {
        private readonly int CancelAfterMilliSecond;
        private readonly MemoryCacheEntryOptions DefaultMemoryCacheEntryOptions;
        private readonly IMemoryCache _memoryCache;
        private readonly ISearchEngineScraper _scraper;
        private readonly ILogger<UrlAppearanceController> _logger;

        public UrlAppearanceController(IOptions<UrlAppearanceControllerOptions> options, IMemoryCache memoryCache, ISearchEngineScraper scraper, ILogger<UrlAppearanceController> logger)
        {
            CancelAfterMilliSecond = options.Value.CancelAfterMilliSecond;
            DefaultMemoryCacheEntryOptions = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.Parse(options.Value.CacheDuration)
            };

            _memoryCache = memoryCache;
            _scraper = scraper;
            _logger = logger;
        }

        [HttpPost("CountAppearances")]
        public async Task<UrlAppearanceCount> CountAppearances([FromBody] UrlAppearanceQuery query)
        {
            int count;
            var tokenSource = new CancellationTokenSource();
            tokenSource.CancelAfter(CancelAfterMilliSecond);

            if (!_memoryCache.TryGetValue((query.Keywords, query.Url), out count))
            {
                try
                {
                    count = await _scraper.SearchKeywordsAndCountUrlAppearances(query.Keywords, query.Url, tokenSource.Token);

                    _memoryCache.Set((query.Keywords, query.Url), count, DefaultMemoryCacheEntryOptions);
                }
                catch (InvalidOperationException ex)
                {
                    _logger.LogError(ex, "Scraper failed, did search engine change its layout?");

                    return GetUrlApperanceCount(query, "");
                }
            }

            return GetUrlApperanceCount(query, count.ToString());
        }

        private UrlAppearanceCount GetUrlApperanceCount(UrlAppearanceQuery query, string count)
        {
            return new UrlAppearanceCount
            {
                Keywords = query.Keywords,
                Url = query.Url,
                Count = count
            };
        }
    }
}
