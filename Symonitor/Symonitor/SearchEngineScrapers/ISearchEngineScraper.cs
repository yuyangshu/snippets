using System.Threading;
using System.Threading.Tasks;

namespace Symonitor.SearchEngineScrapers
{
    public interface ISearchEngineScraper
    {
        Task<int> SearchKeywordsAndCountUrlAppearances(string keywords, string urlToCount, CancellationToken cancellationToken);
    }
}
