import React, { useState, useEffect } from 'react';
import { Settings, Eye, EyeOff, Save, AlertCircle } from 'lucide-react';

export interface APIConfig {
  provider: 'claude' | 'openai' | 'deepseek' | 'gemini';
  apiKey: string;
  model?: string;
}

interface ConfigSectionProps {
  onConfigSave: (config: APIConfig | null) => void;
}

const PROVIDER_INFO = {
  claude: {
    name: 'Claude (Anthropic)',
    defaultModel: 'claude-sonnet-4-20250514',
    keyPrefix: 'sk-ant-',
    placeholder: 'sk-ant-api03-...',
    color: 'neo-peach',
  },
  openai: {
    name: 'OpenAI',
    defaultModel: 'gpt-4o',
    keyPrefix: 'sk-',
    placeholder: 'sk-proj-...',
    color: 'neo-green',
  },
  deepseek: {
    name: 'DeepSeek',
    defaultModel: 'deepseek-chat',
    keyPrefix: 'sk-',
    placeholder: 'sk-...',
    color: 'neo-cyan',
  },
  gemini: {
    name: 'Gemini (Google)',
    defaultModel: 'gemini-1.5-pro',
    keyPrefix: 'AIza',
    placeholder: 'AIza...',
    color: 'neo-yellow',
  },
};

const ConfigSection: React.FC<ConfigSectionProps> = ({ onConfigSave }) => {
  const [provider, setProvider] = useState<APIConfig['provider']>('claude');
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [savedConfig, setSavedConfig] = useState<APIConfig | null>(null);

  // Load saved configuration from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('scirag-api-config');
    if (saved) {
      try {
        const config = JSON.parse(saved) as APIConfig;
        setProvider(config.provider);
        setApiKey(config.apiKey);
        setModel(config.model || '');
        setSavedConfig(config);
        onConfigSave(config);
      } catch (error) {
        console.error('Failed to load saved config:', error);
      }
    }
  }, []);

  const handleSave = () => {
    if (!apiKey.trim()) {
      alert('Please enter an API key');
      return;
    }

    // Validate API key format
    const providerInfo = PROVIDER_INFO[provider];
    if (!apiKey.trim().startsWith(providerInfo.keyPrefix)) {
      const proceed = confirm(
        `Warning: Your API key doesn't start with "${providerInfo.keyPrefix}". ` +
        `This might not be a valid ${providerInfo.name} API key. ` +
        `Do you want to save it anyway?`
      );
      if (!proceed) return;
    }

    const config: APIConfig = {
      provider,
      apiKey: apiKey.trim(),
      model: model.trim() || undefined,
    };

    localStorage.setItem('scirag-api-config', JSON.stringify(config));
    setSavedConfig(config);
    onConfigSave(config);
  };

  const handleClear = () => {
    localStorage.removeItem('scirag-api-config');
    setSavedConfig(null);
    onConfigSave(null);
    setApiKey('');
    setModel('');
  };

  const providerInfo = PROVIDER_INFO[provider];

  return (
    <div className="w-full">
      <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex items-center gap-3 mb-6">
          <Settings className="w-6 h-6" />
          <h2 className="text-2xl font-black">API Configuration</h2>
        </div>

        {/* Fun message about API keys */}
        <div className="bg-neo-pink border-4 border-black p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div className="text-sm">
            <p className="font-bold mb-1">🎉 Bring Your Own API Key!</p>
            <p>
              Free rides are over! 🚀 The server owner got tired of paying for your AI adventures.
              But don't worry—your API key stays safe in your browser and goes directly to your chosen provider.
              We're just the middleman here! 🤝
            </p>
          </div>
        </div>

        {/* Privacy notice */}
        <div className="bg-neo-cyan border-4 border-black p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div className="text-sm">
            <p className="font-bold mb-1">🔒 Privacy First:</p>
            <p>
              Your API key is stored locally in your browser only. It's sent directly to your chosen provider (Claude, OpenAI, etc.)
              and never touches our servers. Clear your browser data to remove it anytime.
            </p>
          </div>
        </div>

        <>
            {/* Provider Selection */}
            <div className="mb-6">
              <label className="block font-bold mb-2">Select Provider</label>
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(PROVIDER_INFO).map(([key, info]) => (
                  <button
                    key={key}
                    onClick={() => setProvider(key as APIConfig['provider'])}
                    className={`p-4 border-4 border-black font-bold transition-all
                      ${provider === key
                        ? `bg-${info.color} shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]`
                        : 'bg-white hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                      }`}
                  >
                    {info.name}
                  </button>
                ))}
              </div>
            </div>

            {/* API Key Input */}
            <div className="mb-6">
              <label className="block font-bold mb-2">
                API Key for {providerInfo.name}
              </label>
              <div className="relative">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder={providerInfo.placeholder}
                  className="w-full p-3 pr-12 border-4 border-black font-mono text-sm focus:outline-none focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
                />
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-gray-100"
                >
                  {showApiKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <p className="text-xs text-gray-600 mt-1">
                Your API key starts with: {providerInfo.keyPrefix}...
              </p>
            </div>

            {/* Model Input (Optional) */}
            <div className="mb-6">
              <label className="block font-bold mb-2">
                Model (Optional)
              </label>
              <input
                type="text"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                placeholder={`Default: ${providerInfo.defaultModel}`}
                className="w-full p-3 border-4 border-black font-mono text-sm focus:outline-none focus:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
              />
              <p className="text-xs text-gray-600 mt-1">
                Leave empty to use the default model for this provider
              </p>
            </div>
          </>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-6 py-3 bg-neo-green border-4 border-black font-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all"
          >
            <Save className="w-5 h-5" />
            Save Configuration
          </button>

          {savedConfig && (
            <button
              onClick={handleClear}
              className="px-6 py-3 bg-white border-4 border-black font-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all"
            >
              Clear Configuration
            </button>
          )}
        </div>

        {/* Status Message */}
        {savedConfig ? (
          <div className="mt-4 p-3 bg-neo-green border-4 border-black">
            <p className="font-bold">
              ✓ Using {PROVIDER_INFO[savedConfig.provider].name}
              {savedConfig.model && ` with model: ${savedConfig.model}`}
            </p>
          </div>
        ) : (
          <div className="mt-4 p-3 bg-neo-yellow border-4 border-black">
            <p className="font-bold">
              ⚠️ No API key configured. Please save your configuration above to use the chat feature.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConfigSection;
