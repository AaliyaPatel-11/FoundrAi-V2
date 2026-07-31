import React from 'react';
import { Cpu } from 'lucide-react';

export default function TypingIndicator() {
  return (
    <div className="flex w-full justify-start my-4">
      <div className="flex items-start max-w-[85%] sm:max-w-[75%] space-x-3">
        {/* Avatar */}
        <div className="p-2 rounded-xl bg-gradient-to-br from-accent-teal to-accent-violet text-white flex-shrink-0">
          <Cpu className="w-5 h-5" />
        </div>

        {/* Typing bubble */}
        <div className="p-4 rounded-2xl bg-[#1e293b]/60 border border-slate-800 rounded-tl-none flex items-center space-x-1.5 select-none">
          <div className="w-2 h-2 rounded-full bg-accent-teal animate-pulse-dot" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 rounded-full bg-accent-teal animate-pulse-dot" style={{ animationDelay: '200ms' }}></div>
          <div className="w-2 h-2 rounded-full bg-accent-teal animate-pulse-dot" style={{ animationDelay: '400ms' }}></div>
        </div>
      </div>
    </div>
  );
}
