import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { api, Paper } from '../api/client';
import PaperCard from './PaperCard';

interface Props {
  onPapersSelected: (papers: Paper[]) => void;
  onPapersProcessed: (paperIds: string[]) => void;
  selectedPapers: Paper[];
}

export default function SearchSection({ onPapersSelected, onPapersProcessed, selectedPapers }: Props) {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(3);
  const [searchResults, setSearchResults] = useState<Paper[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    setError('');
    setSearchResults([]);

    try {
      const response = await api.searchPapers(query, maxResults);
      setSearchResults(response.papers);
      onPapersSelected(response.papers);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to search papers');
    } finally {
      setIsSearching(false);
    }
  };

  const handleProcessPapers = async () => {
    if (selectedPapers.length === 0) return;

    setIsProcessing(true);
    setError('');

    try {
      const paperIds = selectedPapers.map(p => p.paper_id);
      const response = await api.processPapers(paperIds);
      
      if (response.success) {
        onPapersProcessed(paperIds);
      } else {
        setError(response.message);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process papers');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Search Card */}
      <div className="card-brutal bg-neo-cyan p-6 shadow-brutal-lg">
        <h2 className="font-display text-3xl font-black mb-4 flex items-center gap-3">
          <Search className="w-8 h-8" />
          Search arXiv
        </h2>

        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label className="block font-bold mb-2 text-sm">
              Research Topic
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., neural networks, quantum computing..."
              className="input-brutal w-full bg-white shadow-brutal-sm"
            />
          </div>

          <div className="flex gap-4 items-end">
            <div className="flex-1">
              <label className="block font-bold mb-2 text-sm">
                Max Papers: {maxResults}
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={maxResults}
                onChange={(e) => setMaxResults(Number(e.target.value))}
                className="w-full h-3 bg-white border-4 border-black appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #000 0%, #000 ${maxResults * 10}%, #fff ${maxResults * 10}%, #fff 100%)`
                }}
              />
            </div>

            <button
              type="submit"
              disabled={isSearching || !query.trim()}
              className="btn-brutal bg-neo-yellow shadow-brutal flex items-center gap-2 disabled:opacity-50"
            >
              {isSearching ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Search
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Error */}
      {error && (
        <div className="card-brutal bg-red-200 border-red-600 p-4 shadow-brutal animate-bounce-in">
          <p className="font-bold text-red-900">❌ {error}</p>
        </div>
      )}

      {/* Results */}
      {searchResults.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-display text-2xl font-black">
              Found {searchResults.length} Papers
            </h3>
            <button
              onClick={handleProcessPapers}
              disabled={isProcessing}
              className="btn-brutal bg-neo-pink shadow-brutal flex items-center gap-2 disabled:opacity-50"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                `Process ${selectedPapers.length} Paper${selectedPapers.length !== 1 ? 's' : ''}`
              )}
            </button>
          </div>

          <div className="space-y-4">
            {searchResults.map((paper, index) => (
              <div
                key={paper.paper_id}
                className="animate-slide-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <PaperCard paper={paper} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!isSearching && searchResults.length === 0 && !error && (
        <div className="card-brutal bg-neo-green p-12 text-center shadow-brutal-lg">
          <Search className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p className="font-bold text-lg">
            Search for papers to get started! 🚀
          </p>
          <p className="mt-2 text-sm opacity-75">
            Try: "attention mechanisms", "quantum computing", "deep learning"
          </p>
        </div>
      )}
    </div>
  );
}
