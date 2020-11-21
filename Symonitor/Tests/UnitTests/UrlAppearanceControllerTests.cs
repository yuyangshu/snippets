using System.Threading.Tasks;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Options;
using Moq;
using Xunit;
using Symonitor.Controllers;
using Symonitor.Models;
using Symonitor.Options;
using Symonitor.SearchEngineScrapers;

namespace Symonitor.Tests.UnitTests
{
    public class UrlAppearanceControllerTests
    {
        private readonly Mock<IOptions<UrlAppearanceControllerOptions>> _options;
        private readonly Mock<ISearchEngineScraper> _scraper;

        public UrlAppearanceControllerTests()
        {
            _options = new Mock<IOptions<UrlAppearanceControllerOptions>>();
            _scraper = new Mock<ISearchEngineScraper>();

            _options.Setup(o => o.Value).Returns(new UrlAppearanceControllerOptions { CacheDuration = "0:0:01"});
        }

        [Fact]
        public async Task CountAppearances_UsesCache_WhenCacheHasEntryAndNotExpired()
        {
            // Arrange
            var query = new UrlAppearanceQuery
            {
                Keywords = "abc",
                Url = "def"
            };
            var expected = 1;
            var _memoryCacheWithHit = MockMemoryCacheService.GetMemoryCache(expected, true);
            var controller = new UrlAppearanceController(_options.Object, _memoryCacheWithHit, _scraper.Object);

            // Act
            var result = await controller.CountAppearances(query);

            // Assert
            _scraper.Verify(s => s.SearchKeywordsAndCountUrlAppearances(It.IsAny<string>(), It.IsAny<string>()), Times.Never);
            Assert.Equal("abc", result.Keywords);
            Assert.Equal("def", result.Url);
            Assert.Equal("1", result.Count);
        }

        [Fact]
        public async Task CountAppearances_DoesNotUsesCache_WhenNoCacheEntry()
        {
            // Arrange
            var query = new UrlAppearanceQuery
            {
                Keywords = "abc",
                Url = "def"
            };
            var _memoryCacheWithMiss = MockMemoryCacheService.GetMemoryCache(null, false);
            _scraper.Setup(s => s.SearchKeywordsAndCountUrlAppearances(It.IsAny<string>(), It.IsAny<string>())).ReturnsAsync(2);
            var controller = new UrlAppearanceController(_options.Object, _memoryCacheWithMiss, _scraper.Object);

            // Act
            var result = await controller.CountAppearances(query);

            // Assert
            _scraper.Verify(s => s.SearchKeywordsAndCountUrlAppearances(It.IsAny<string>(), It.IsAny<string>()), Times.Once);
            Assert.Equal("abc", result.Keywords);
            Assert.Equal("def", result.Url);
            Assert.Equal("2", result.Count);
        }
    }

        public static class MockMemoryCacheService
    {
        public static IMemoryCache GetMemoryCache(object expectedValue, bool hit)
        {
            var mockMemoryCache = new Mock<IMemoryCache>();
            var cachEntry = Mock.Of<ICacheEntry>();

            mockMemoryCache
                .Setup(x => x.TryGetValue(It.IsAny<object>(), out expectedValue))
                .Returns(hit);
            mockMemoryCache
                .Setup(m => m.CreateEntry(It.IsAny<object>()))
                .Returns(cachEntry);

            return mockMemoryCache.Object;
        }
    }
}
