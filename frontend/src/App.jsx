import React, { useState, useRef, useEffect } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import TypingIndicator from './components/TypingIndicator';
import { sendChatMessage } from './services/api';
import { RefreshCw, Terminal, Cpu } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom of the chat window
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = { role: 'user', content: text };
    const updatedMessages = [...messages, userMessage];
    
    setMessages(updatedMessages);
    setIsLoading(true);
    setError(null);

    try {
      const responseContent = await sendChatMessage(updatedMessages);
      setMessages((prev) => [...prev, { role: 'assistant', content: responseContent }]);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Unable to connect to FondrAI. Make sure the backend server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectStarter = (text) => {
    handleSendMessage(text);
  };

  const handleResetChat = () => {
    if (window.confirm('Start a new session? This will clear the current conversation history.')) {
      setMessages([]);
      setError(null);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-h-screen bg-[#0b0f19] text-slate-100 overflow-hidden font-sans">
      
      {/* Brand Header */}
      <header className="glass-panel border-b border-slate-800/80 px-6 py-4 flex items-center justify-between z-10 flex-shrink-0">
        <div className="flex items-center space-x-3 select-none">
          <div className="bg-gradient-to-tr from-accent-teal to-accent-violet p-2 rounded-xl text-white">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-base leading-tight tracking-wide bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-300">
              FondrAI
            </h2>
            <p className="text-[10px] text-accent-teal font-medium tracking-wider uppercase">
              AI Co-Founder
            </p>
          </div>
        </div>

        {messages.length > 0 && (
          <button
            onClick={handleResetChat}
            className="flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 border border-slate-850 hover:text-slate-200 hover:border-slate-700 bg-slate-900/30 transition-all cursor-pointer"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset Session</span>
          </button>
        )}
      </header>

      {/* Main Container */}
      <main className="flex-grow flex flex-col justify-between overflow-hidden relative">
        {/* Ambient glow backgrounds */}
        <div className="absolute top-1/4 left-1/4 w-[350px] h-[350px] rounded-full bg-accent-teal/5 filter blur-[120px] -z-10 pointer-events-none"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-accent-violet/5 filter blur-[120px] -z-10 pointer-events-none"></div>

        {/* Conversation flow section */}
        <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-8">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <WelcomeScreen onSelectStarter={handleSelectStarter} />
            </div>
          ) : (
            <div className="max-w-3xl mx-auto space-y-2">
              {messages.map((message, index) => (
                <ChatMessage key={index} message={message} />
              ))}
              
              {isLoading && <TypingIndicator />}
              
              {error && (
                <div className="bg-red-950/20 border border-red-500/30 text-red-200 px-4 py-3.5 rounded-xl text-sm max-w-3xl mx-auto my-4 flex items-start space-x-2">
                  <Terminal className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold">Connection Error: </span>
                    {error}
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Bottom Dock for Input */}
        <div className="glass-panel border-t border-slate-900 px-4 py-4 sm:px-8 flex-shrink-0">
          <div className="max-w-3xl mx-auto flex flex-col space-y-2">
            <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
            <div className="text-[10px] text-slate-500 text-center select-none">
              FondrAI is an interactive AI partner. Discuss and build your startup roadmap.
            </div>
          </div>
        </div>
      </main>

    </div>
  );
}
