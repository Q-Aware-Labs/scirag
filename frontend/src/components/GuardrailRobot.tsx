import React from 'react';
import { Shield, AlertTriangle, XCircle, Info } from 'lucide-react';

export interface GuardrailWarning {
  type: string;
  message: string;
  severity: 'warning' | 'error';
}

interface GuardrailRobotProps {
  warning: GuardrailWarning;
  onDismiss?: () => void;
}

const GuardrailRobot: React.FC<GuardrailRobotProps> = ({ warning, onDismiss }) => {
  const getIcon = () => {
    switch (warning.type) {
      case 'harmful':
        return <Shield className="w-8 h-8" />;
      case 'off_topic':
        return <Info className="w-8 h-8" />;
      case 'jailbreak':
        return <XCircle className="w-8 h-8" />;
      case 'hallucination':
      case 'not_grounded':
        return <AlertTriangle className="w-8 h-8" />;
      default:
        return <Shield className="w-8 h-8" />;
    }
  };

  const getColor = () => {
    return warning.severity === 'error' ? 'neo-pink' : 'neo-yellow';
  };

  const getTitle = () => {
    switch (warning.type) {
      case 'harmful':
        return '🛡️ Content Safety Alert';
      case 'off_topic':
        return '📚 Topic Reminder';
      case 'jailbreak':
        return '🔒 Security Notice';
      case 'hallucination':
        return '⚠️ Verification Needed';
      case 'not_grounded':
        return '📖 Source Limitation';
      default:
        return '🤖 Guardrail Notice';
    }
  };

  return (
    <div className="w-full animate-slide-in">
      <div className={`bg-${getColor()} border-4 border-black p-6 shadow-brutal relative`}>
        {/* Cute Robot Icon */}
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            {/* Robot Head with Animation */}
            <div className="relative">
              {/* Robot Face Container */}
              <div className="w-16 h-16 bg-neo-cyan border-4 border-black rounded-sm shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] animate-bounce-subtle">
                {/* Robot Eyes */}
                <div className="flex justify-center gap-2 mt-3">
                  <div className="w-2 h-2 bg-black rounded-full animate-blink"></div>
                  <div className="w-2 h-2 bg-black rounded-full animate-blink" style={{ animationDelay: '0.1s' }}></div>
                </div>
                {/* Robot Mouth */}
                <div className="flex justify-center mt-2">
                  <div className="w-6 h-1 bg-black rounded-full"></div>
                </div>
              </div>

              {/* Robot Antenna */}
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
                <div className="w-0.5 h-3 bg-black mx-auto"></div>
                <div className="w-2 h-2 bg-neo-pink border-2 border-black rounded-full animate-pulse-glow"></div>
              </div>

              {/* Robot Body */}
              <div className="w-16 h-8 bg-white border-4 border-black border-t-0 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                {/* Control Panel */}
                <div className="flex justify-center gap-1 mt-1">
                  <div className="w-1 h-1 bg-neo-green rounded-full"></div>
                  <div className="w-1 h-1 bg-neo-yellow rounded-full"></div>
                  <div className="w-1 h-1 bg-neo-pink rounded-full"></div>
                </div>
              </div>

              {/* Shield Icon Overlay for warnings */}
              <div className="absolute -right-1 -top-1 bg-white border-2 border-black p-1 rounded-sm shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                {getIcon()}
              </div>
            </div>
          </div>

          {/* Warning Content */}
          <div className="flex-1">
            <h3 className="font-black text-xl mb-2 flex items-center gap-2">
              {getTitle()}
            </h3>
            <p className="font-bold text-base leading-relaxed">
              {warning.message}
            </p>

            {/* Helpful Tips */}
            {warning.type === 'off_topic' && (
              <div className="mt-3 p-3 bg-white border-2 border-black">
                <p className="text-sm font-bold">💡 Try asking:</p>
                <ul className="text-sm mt-1 space-y-1">
                  <li>• "What are the main findings?"</li>
                  <li>• "Explain the methodology"</li>
                  <li>• "How do these papers compare?"</li>
                </ul>
              </div>
            )}

            {warning.type === 'not_grounded' && (
              <div className="mt-3 p-3 bg-white border-2 border-black">
                <p className="text-sm font-bold">
                  ℹ️ The answer below may contain information beyond your processed papers.
                  Please verify important details with the original sources.
                </p>
              </div>
            )}
          </div>

          {/* Dismiss Button (only for non-error warnings) */}
          {onDismiss && warning.severity !== 'error' && (
            <button
              onClick={onDismiss}
              className="flex-shrink-0 w-8 h-8 bg-white border-2 border-black hover:bg-neo-peach transition-colors font-black"
              aria-label="Dismiss warning"
            >
              ×
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default GuardrailRobot;
