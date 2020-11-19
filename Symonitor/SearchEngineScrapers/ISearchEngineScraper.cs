using System.Threading.Tasks;

namespace Symonitor.SearchEngineScrapers
{
    public interface ISearchEngineScraper
    {
        Task<int> SearchKeywordsAndCountUrlOccurrences(string keywords, string urlToCount);
    }
}