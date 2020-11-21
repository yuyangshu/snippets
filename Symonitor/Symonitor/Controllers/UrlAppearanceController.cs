using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Memory;
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
        private readonly MemoryCacheEntryOptions DefaultMemoryCacheEntryOptions;
        private readonly IMemoryCache _memoryCache;
        private readonly ISearchEngineScraper _scraper;

        public UrlAppearanceController(IOptions<UrlAppearanceControllerOptions> options, IMemoryCache memoryCache, ISearchEngineScraper scraper)
        {
            DefaultMemoryCacheEntryOptions = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.Parse(options.Value.CacheDuration)
            };

            _memoryCache = memoryCache;
            _scraper = scraper;
        }

        [HttpPost("CountAppearances")]
        public async Task<UrlAppearanceCount> CountAppearances([FromBody] UrlAppearanceQuery query)
        {
            int count;

            if (!_memoryCache.TryGetValue((query.Keywords, query.Url), out count))
            {
                count = await _scraper.SearchKeywordsAndCountUrlAppearances(query.Keywords, query.Url);

                _memoryCache.Set((query.Keywords, query.Url), count, DefaultMemoryCacheEntryOptions);
            }

            return new UrlAppearanceCount
            {
                Keywords = query.Keywords,
                Url = query.Url,
                Count = count.ToString()
            };
        }
    }
}
