import React from 'react';
import { User, Cpu } from 'lucide-react';

export default function ChatMessage({ message, selectedRole }) {
  const isAssistant = message.role === 'assistant';

  return (
    <div className={`flex w-full my-4 ${isAssistant ? 'justify-start' : 'justify-end'}`}>
      <div className={`flex items-start max-w-[85%] sm:max-w-[75%] space-x-3 ${isAssistant ? '' : 'flex-row-reverse space-x-reverse'}`}>
        
        {/* Avatar */}
        <div className={`p-2 rounded-xl flex-shrink-0 ${
          isAssistant 
            ? 'bg-gradient-to-br from-accent-teal to-accent-violet text-white' 
            : 'bg-slate-800 text-slate-300 border border-slate-700'
        }`}>
          {isAssistant ? <Cpu className="w-5 h-5" /> : <User className="w-5 h-5" />}
        </div>

        {/* Message Bubble */}
        <div className={`p-4 rounded-2xl text-sm sm:text-base leading-relaxed ${
          isAssistant
            ? 'bg-[#1e293b]/60 border border-slate-800 text-slate-200 rounded-tl-none'
            : 'bg-[#132238] border border-accent-teal/30 text-slate-100 rounded-tr-none'
        }`}>
          {/* Sender indicator */}
          <div className="text-[10px] uppercase tracking-wider text-slate-400 font-bold mb-1 select-none">
            {isAssistant
              ? (selectedRole === 'cfo' ? 'CFO' : 'FondrAI Co-founder')
              : 'You'}
          </div>
          
          {/* Message Content */}
          <div className="whitespace-pre-wrap break-words">
            {message.content}
          </div>
        </div>

      </div>
    </div>
  );
}
