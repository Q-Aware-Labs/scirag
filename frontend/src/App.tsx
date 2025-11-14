import { useState } from 'react';
import { Search, Sparkles, MessageSquare, Settings, Github, Heart, HelpCircle } from 'lucide-react';
import SearchSection from './components/SearchSection';
import ChatSection from './components/ChatSection';
import PapersList from './components/PapersList';
import ConfigSection from './components/ConfigSection';
import { Paper, APIConfig } from './api/client';

function App() {
  const [selectedPapers, setSelectedPapers] = useState<Paper[]>([]);
  const [processedPaperIds, setProcessedPaperIds] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'search' | 'chat' | 'config'>('search');
  const [apiConfig, setApiConfig] = useState<APIConfig | null>(null);

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
                <p className="text-xl font-bold mt-1">
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
              <button
                onClick={() => setActiveTab('config')}
                className={`btn-brutal flex items-center gap-2 shadow-brutal-sm ${
                  activeTab === 'config'
                    ? 'bg-neo-peach'
                    : 'bg-white'
                }`}
              >
                <Settings className="w-5 h-5" />
                <span className="hidden sm:inline">Config</span>
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
            {activeTab === 'search' && (
              <SearchSection
                onPapersSelected={handlePapersSelected}
                onPapersProcessed={handlePapersProcessed}
                selectedPapers={selectedPapers}
                apiConfig={apiConfig}
              />
            )}
            {activeTab === 'chat' && (
              <ChatSection apiConfig={apiConfig} />
            )}
            {activeTab === 'config' && (
              <ConfigSection onConfigSave={setApiConfig} />
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
      <footer className="border-t-4 border-black mt-12 py-8 bg-neo-peach">
        <div className="container mx-auto px-4">
          <div className="flex flex-col items-center gap-4">
            {/* Main Info */}
            <div className="text-center">
              <p className="font-bold text-lg flex items-center justify-center gap-2">
                Made with <Heart className="w-4 h-4 fill-red-500 text-red-500" /> by{' '}
                <a
                  href="https://github.com/Q-Aware-Labs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline hover:text-neo-pink transition-colors"
                >
                  Q-Aware Labs
                </a>
              </p>
              <p className="font-bold text-sm mt-1 opacity-75">
                Powered by arXiv, Claude AI & Neobrutalism ✨
              </p>
            </div>

            {/* Links */}
            <div className="flex flex-wrap justify-center gap-3">
              <a
                href="https://github.com/Q-Aware-Labs/scirag"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-brutal bg-black text-white shadow-brutal-sm flex items-center gap-2 text-sm"
              >
                <Github className="w-4 h-4" />
                View on GitHub
              </a>
              <a
                href="https://github.com/Q-Aware-Labs/scirag#usage"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-brutal bg-neo-cyan shadow-brutal-sm flex items-center gap-2 text-sm"
              >
                <HelpCircle className="w-4 h-4" />
                Usage Guide
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
