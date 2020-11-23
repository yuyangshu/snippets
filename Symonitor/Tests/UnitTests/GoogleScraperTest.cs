using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Moq;
using Moq.Protected;
using Xunit;
using Symonitor.SearchEngineScrapers;

namespace Symonitor.Tests.UnitTests
{
    public class GoogleScraperTests
    {
        // this needs to be fixed; source: https://stackoverflow.com/questions/36425008/mocking-httpclient-in-unit-tests
        // is it possible to overwrite static field with this?
        // to test different exceptions return different exceptions from GetClientThatThrowsException()
        // then use scraperType.TypeInitializer.Invoke(null, new object[0]);
        // source: https://stackoverflow.com/questions/11279582/unit-test-static-constructor-w-different-config-values
        [Fact]
        public async Task SearchKeywordsAndCountUrlAppearances_ReturnsZeroAndLog_WhenTaskTimeout()
        {
            // Arrange
            var scraperType = typeof(GoogleScraper);
            var fieldInfo = scraperType.GetField("ClientFactory");
            fieldInfo.SetValue(scraperType, GetClientThatThrowsException(new TaskCanceledException()));
            var logger = new Mock<ILogger<GoogleScraper>>();

            // Act
            var scraper = new GoogleScraper(logger.Object);
            var result = await scraper.SearchKeywordsAndCountUrlAppearances("kant", "", CancellationToken.None);

            // Assert
            Assert.Equal(0, result);
            logger.Verify(l => l.LogInformation(It.IsAny<TaskCanceledException>(), "Timeout when fetching https://www.google.com/search?q={kant}&num=100"), Times.Once);
        }

        [Fact]
        public void CountOccurenceOfUrl_ReturnsExpectedCount_WhenUrlInHtml()
        {
            // Arrange
            var htmlContent = TestHelper.GetEmbeddedResource("TestFiles.kant.html");
            var url = "en.wikipedia.org";

            // Act
            var result = GoogleScraper.CountOccurenceOfUrl(htmlContent, url);

            // Assert
            Assert.Equal(1, result);
        }

        [Fact]
        public void CountOccurenceOfUrl_ReturnsZeroCount_WhenUrlNotInHtml()
        {
            // Arrange
            var htmlContent = "dummy_html_with_no_url";
            var url = "en.wikipedia.org";

            // Act
            var result = GoogleScraper.CountOccurenceOfUrl(htmlContent, url);

            // Assert
            Assert.Equal(0, result);
        }

        private Func<HttpClient> GetClientThatThrowsException(Exception ex)
        {
            return () =>
            {
                var mockHandler = new Mock<HttpMessageHandler>();
                mockHandler.Protected().Setup<Task<HttpResponseMessage>>("SendAsync", It.IsAny<HttpRequestMessage>(), It.IsAny<CancellationToken>()).Throws(ex);

                return new HttpClient(mockHandler.Object);
            };
        }
    }
}
