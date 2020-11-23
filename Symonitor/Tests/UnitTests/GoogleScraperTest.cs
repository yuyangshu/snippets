using Xunit;
using Symonitor.SearchEngineScrapers;

namespace Symonitor.Tests.UnitTests
{
    public class GoogleScraperTests
    {
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
    }
}
