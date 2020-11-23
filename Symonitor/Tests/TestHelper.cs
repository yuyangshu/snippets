using System.IO;
using System.Net.Http;
using System.Reflection;
using System.Text;
using Newtonsoft.Json;

namespace Symonitor.Tests
{
    public static class TestHelper
	{
		public static string GetEmbeddedResource(string resourceName)
		{
			var fullResourceName = Assembly.GetExecutingAssembly().GetName().Name + '.' + resourceName;

            using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(fullResourceName))
            using (var streamReader = new StreamReader(stream))
            {
                return streamReader.ReadToEnd();
            }
		}

        public static StringContent ToJsonContent(object obj)
            => new StringContent(JsonConvert.SerializeObject(obj), Encoding.Default, "application/json");
    }
}
