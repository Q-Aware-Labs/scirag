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
  const [useDefaultKey, setUseDefaultKey] = useState(true);
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
        setUseDefaultKey(false);
        setSavedConfig(config);
        onConfigSave(config);
      } catch (error) {
        console.error('Failed to load saved config:', error);
      }
    }
  }, []);

  const handleSave = () => {
    if (useDefaultKey) {
      // Clear custom configuration
      localStorage.removeItem('scirag-api-config');
      setSavedConfig(null);
      onConfigSave(null);
      setApiKey('');
      setModel('');
      return;
    }

    if (!apiKey.trim()) {
      alert('Please enter an API key');
      return;
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
    setUseDefaultKey(true);
  };

  const providerInfo = PROVIDER_INFO[provider];

  return (
    <div className="w-full">
      <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex items-center gap-3 mb-6">
          <Settings className="w-6 h-6" />
          <h2 className="text-2xl font-black">API Configuration</h2>
        </div>

        {/* Warning about API keys */}
        <div className="bg-neo-yellow border-4 border-black p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div className="text-sm">
            <p className="font-bold mb-1">Privacy Notice:</p>
            <p>
              Your API key is stored locally in your browser and sent directly to the API provider.
              It's never stored on our servers. Clear your browser data to remove it.
            </p>
          </div>
        </div>

        {/* Use Default Key Toggle */}
        <div className="mb-6">
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={useDefaultKey}
              onChange={(e) => setUseDefaultKey(e.target.checked)}
              className="w-5 h-5 border-2 border-black"
            />
            <span className="font-bold">Use default API key (from server)</span>
          </label>
          <p className="text-sm text-gray-600 mt-2 ml-8">
            If checked, the system will use the API key configured on the server.
          </p>
        </div>

        {!useDefaultKey && (
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
        )}

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-6 py-3 bg-neo-green border-4 border-black font-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all"
          >
            <Save className="w-5 h-5" />
            Save Configuration
          </button>

          {savedConfig && !useDefaultKey && (
            <button
              onClick={handleClear}
              className="px-6 py-3 bg-white border-4 border-black font-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all"
            >
              Clear & Use Default
            </button>
          )}
        </div>

        {/* Status Message */}
        {savedConfig && !useDefaultKey && (
          <div className="mt-4 p-3 bg-neo-green border-4 border-black">
            <p className="font-bold">
              ✓ Using {PROVIDER_INFO[savedConfig.provider].name}
              {savedConfig.model && ` with model: ${savedConfig.model}`}
            </p>
          </div>
        )}

        {useDefaultKey && (
          <div className="mt-4 p-3 bg-neo-cyan border-4 border-black">
            <p className="font-bold">
              ✓ Using default server configuration
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConfigSection;
