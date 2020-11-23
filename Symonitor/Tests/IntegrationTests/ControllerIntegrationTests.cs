using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.Testing;
using Newtonsoft.Json;
using Xunit;
using Symonitor.Models;

namespace Symonitor.Tests.IntegrationTests
{
    public class ControllerIntegrationTests : IClassFixture<WebApplicationFactory<Startup>>
    {
        readonly WebApplicationFactory<Startup> _factory;

        public ControllerIntegrationTests(WebApplicationFactory<Startup> factory)
        {
            _factory = factory;
        }

        [Fact]
        public async Task UrlAppearance_CountAppearances_ReturnsExpectedCount()
        {
            // Arrange
            var client = _factory.CreateClient();
            var url = "UrlAppearance/CountAppearances";
            var payload = new
            {
                Keywords = "e-settlements",
                Url = "www.sympli.com.au"
            };

            // Act
            var response = await client.PostAsync(url, TestHelper.ToJsonContent(payload));

            // Assert
            response.EnsureSuccessStatusCode();
            var result = JsonConvert.DeserializeObject<UrlAppearanceCount>(await response.Content.ReadAsStringAsync());
            Assert.Equal("e-settlements", result.Keywords);
            Assert.Equal("www.sympli.com.au", result.Url);
            Assert.Equal("1", result.Count);
        }
    }
}
