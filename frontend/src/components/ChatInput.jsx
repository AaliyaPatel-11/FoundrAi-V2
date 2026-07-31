import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

export default function ChatInput({ onSendMessage, isLoading }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea to fit text height (up to a max height)
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [text]);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!text.trim() || isLoading) return;
    onSendMessage(text);
    setText('');
    // Reset textarea height after sending
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    // Send message on Enter, allow shift+Enter for newlines
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex items-end bg-[#0f172a]/95 border border-slate-700/80 rounded-2xl p-2 focus-within:border-accent-teal/50 transition-colors shadow-lg">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Talk to your AI co-founder..."
          rows={1}
          disabled={isLoading}
          className="flex-grow max-h-[160px] bg-transparent border-none outline-none text-slate-100 text-sm sm:text-base px-3 py-2.5 resize-none placeholder-slate-500 disabled:text-slate-400 disabled:cursor-not-allowed"
        />
        
        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          className="p-3 rounded-xl bg-gradient-to-r from-accent-teal to-accent-violet text-white font-medium hover:opacity-90 active:scale-95 disabled:opacity-40 disabled:scale-100 disabled:cursor-not-allowed transition-all flex items-center justify-center cursor-pointer flex-shrink-0"
        >
          <Send className="w-4 h-4 sm:w-5 sm:h-5" />
        </button>
      </div>
    </form>
  );
}
