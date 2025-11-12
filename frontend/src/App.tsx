import { useState } from 'react';
import { Search, Sparkles, FileText, MessageSquare } from 'lucide-react';
import SearchSection from './components/SearchSection';
import ChatSection from './components/ChatSection';
import PapersList from './components/PapersList';
import { Paper } from './api/client';

function App() {
  const [selectedPapers, setSelectedPapers] = useState<Paper[]>([]);
  const [processedPaperIds, setProcessedPaperIds] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'search' | 'chat'>('search');

  const handlePapersSelected = (papers: Paper[]) => {
    setSelectedPapers(papers);
  };

  const handlePapersProcessed = (paperIds: string[]) => {
    setProcessedPaperIds(paperIds);
    setActiveTab('chat');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b-4 border-black bg-neo-yellow">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-neo-pink border-4 border-black p-3 shadow-brutal">
                <Sparkles className="w-8 h-8" />
              </div>
              <div>
                <h1 className="font-display text-4xl font-black tracking-tight">
                  SciRAG
                </h1>
                <p className="text-sm font-bold mt-1">
                  Scientific Research Assistant
                </p>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => setActiveTab('search')}
                className={`btn-brutal flex items-center gap-2 shadow-brutal-sm ${
                  activeTab === 'search'
                    ? 'bg-neo-cyan'
                    : 'bg-white'
                }`}
              >
                <Search className="w-5 h-5" />
                <span className="hidden sm:inline">Search</span>
              </button>
              <button
                onClick={() => setActiveTab('chat')}
                disabled={processedPaperIds.length === 0}
                className={`btn-brutal flex items-center gap-2 shadow-brutal-sm ${
                  activeTab === 'chat'
                    ? 'bg-neo-green'
                    : 'bg-white'
                } ${processedPaperIds.length === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <MessageSquare className="w-5 h-5" />
                <span className="hidden sm:inline">Chat</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Main Content */}
          <div className="lg:col-span-2">
            {activeTab === 'search' ? (
              <SearchSection
                onPapersSelected={handlePapersSelected}
                onPapersProcessed={handlePapersProcessed}
                selectedPapers={selectedPapers}
              />
            ) : (
              <ChatSection />
            )}
          </div>

          {/* Right Column - Papers List */}
          <div className="lg:col-span-1">
            <PapersList
              selectedPapers={selectedPapers}
              processedPaperIds={processedPaperIds}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t-4 border-black mt-12 py-6 bg-neo-peach">
        <div className="container mx-auto px-4 text-center">
          <p className="font-bold text-sm">
            Powered by arXiv, Claude AI & Neobrutalism ✨
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
