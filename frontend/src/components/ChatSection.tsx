import { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Loader2, User } from 'lucide-react';
import { api, Source, APIConfig, GuardrailWarning } from '../api/client';
import GuardrailRobot from './GuardrailRobot';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
  guardrailWarning?: GuardrailWarning;
}

interface ChatSectionProps {
  apiConfig?: APIConfig | null;
}

export default function ChatSection({ apiConfig }: ChatSectionProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      console.log('Sending query with config:', apiConfig ? `${apiConfig.provider} (${apiConfig.model || 'default'})` : 'server default');
      const response = await api.query(input, 5, apiConfig);
      console.log('Received response:', { success: response.success, hasAnswer: !!response.answer, answerLength: response.answer?.length });

      // Check if response was blocked by guardrails
      if (response.guardrail_warning && response.guardrail_warning.severity === 'error') {
        // Input was blocked - show warning message
        const blockedMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: '',
          timestamp: new Date(),
          guardrailWarning: response.guardrail_warning
        };
        setMessages(prev => [...prev, blockedMessage]);
        return;
      }

      // Check if response is successful and has an answer
      if (!response.success || !response.answer) {
        const errorMsg = response.message || 'No answer received from the API';
        throw new Error(errorMsg);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date(),
        guardrailWarning: response.guardrail_warning  // Include warning if present
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      console.error('Chat error:', err);

      // Extract error message from various possible sources
      let errorText = 'Failed to get response';

      if (err.response?.data?.detail) {
        errorText = err.response.data.detail;
      } else if (err.message) {
        errorText = err.message;
      } else if (typeof err === 'string') {
        errorText = err;
      }

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `❌ Error: ${errorText}`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-300px)] flex flex-col">
      {/* Chat Header */}
      <div className="card-brutal bg-neo-green p-4 shadow-brutal-lg mb-4">
        <h2 className="font-display text-2xl font-black flex items-center gap-3">
          <Sparkles className="w-7 h-7" />
          Ask Questions
        </h2>
        <p className="text-sm font-bold mt-1 opacity-75">
          {apiConfig
            ? `Powered by ${apiConfig.provider.charAt(0).toUpperCase() + apiConfig.provider.slice(1)} AI + RAG`
            : 'Powered by Claude AI + RAG (default)'}
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.length === 0 && (
          <div className="card-brutal bg-neo-peach p-8 text-center shadow-brutal">
            <Sparkles className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p className="font-bold text-lg">Start asking questions!</p>
            <p className="text-sm mt-2 opacity-75">
              Try: "What are the key findings?", "Explain the methodology", "Compare the approaches"
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={message.id}
            className={`animate-slide-in ${
              message.type === 'user' ? 'ml-auto max-w-[80%]' : 'mr-auto max-w-[90%]'
            }`}
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            {message.type === 'user' ? (
              <div className="card-brutal bg-neo-cyan p-4 shadow-brutal-sm">
                <div className="flex items-start gap-3">
                  <div className="bg-black text-white p-2 border-2 border-black">
                    <User className="w-5 h-5" />
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold">{message.content}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                {/* Guardrail Warning (if present) */}
                {message.guardrailWarning && (
                  <GuardrailRobot warning={message.guardrailWarning} />
                )}

                {/* Assistant Message (only if not purely a guardrail error) */}
                {message.content && (
                  <div className="card-brutal bg-white p-4 shadow-brutal">
                    <div className="flex items-start gap-3">
                      <div className="bg-neo-pink p-2 border-2 border-black">
                        <Sparkles className="w-5 h-5" />
                      </div>
                      <div className="flex-1 space-y-3">
                        <p className="font-medium leading-relaxed whitespace-pre-wrap">
                          {message.content}
                        </p>

                        {message.sources && message.sources.length > 0 && (
                      <div className="border-t-2 border-black pt-3 mt-3">
                        <p className="font-bold text-sm mb-2">📚 Sources:</p>
                        <div className="space-y-2">
                          {message.sources.map((source, idx) => (
                            <div
                              key={idx}
                              className="bg-neo-yellow border-2 border-black p-2 text-sm"
                            >
                              <p className="font-bold">{idx + 1}. {source.title}</p>
                              <p className="text-xs opacity-75 mt-1">
                                {source.authors.slice(0, 2).join(', ')}
                                {source.authors.length > 2 && ` +${source.authors.length - 2} more`}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="card-brutal bg-white p-4 shadow-brutal animate-bounce-in mr-auto max-w-[90%]">
            <div className="flex items-center gap-3">
              <div className="bg-neo-pink p-2 border-2 border-black">
                <Sparkles className="w-5 h-5" />
              </div>
              <div className="flex gap-1">
                <div className="loading-dot w-2 h-2 bg-black rounded-full"></div>
                <div className="loading-dot w-2 h-2 bg-black rounded-full"></div>
                <div className="loading-dot w-2 h-2 bg-black rounded-full"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="card-brutal bg-neo-yellow p-4 shadow-brutal-lg">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the papers..."
            disabled={isLoading}
            className="input-brutal flex-1 bg-white shadow-brutal-sm disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="btn-brutal bg-neo-pink shadow-brutal flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
