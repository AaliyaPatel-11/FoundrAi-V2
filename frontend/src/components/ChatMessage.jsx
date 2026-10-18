
import React from 'react';
import { User, Cpu } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const agentLabels = {
  founder: 'FondrAI Founder',
  cfo: 'FondrAI CFO',
  cto: 'FondrAI CTO',
  cmo: 'FondrAI CMO',
  product: 'FondrAI Product',
};

export default function ChatMessage({ message, selectedRole }) {
  const isAssistant = message.role === 'assistant';

  const senderLabel = isAssistant
    ? agentLabels[message.agentRole || selectedRole || 'founder'] ||
      'FondrAI Co-founder'
    : 'You';

  return (
    <div
      className={`flex w-full my-4 ${
        isAssistant ? 'justify-start' : 'justify-end'
      }`}
    >
      <div
        className={`flex items-start max-w-[85%] sm:max-w-[75%] space-x-3 ${
          isAssistant ? '' : 'flex-row-reverse space-x-reverse'
        }`}
      >
        <div
          className={`p-2 rounded-xl flex-shrink-0 ${
            isAssistant
              ? 'bg-gradient-to-br from-accent-teal to-accent-violet text-white'
              : 'bg-slate-800 text-slate-300 border border-slate-700'
          }`}
        >
          {isAssistant ? (
            <Cpu className="w-5 h-5" />
          ) : (
            <User className="w-5 h-5" />
          )}
        </div>

        <div
          className={`p-4 rounded-2xl text-sm sm:text-base leading-relaxed ${
            isAssistant
              ? 'bg-[#1e293b]/60 border border-slate-800 text-slate-200 rounded-tl-none'
              : 'bg-[#132238] border border-accent-teal/30 text-slate-100 rounded-tr-none'
          }`}
        >
          <div className="text-[10px] uppercase tracking-wider text-slate-400 font-bold mb-1 select-none">
            {senderLabel}
          </div>

          <div className="break-words min-w-0">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className="text-xl font-bold mt-4 mb-2">
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="text-lg font-bold mt-4 mb-2">
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="text-base font-bold mt-3 mb-2">
                    {children}
                  </h3>
                ),
                p: ({ children }) => (
                  <p className="mb-3 last:mb-0">{children}</p>
                ),
                ul: ({ children }) => (
                  <ul className="list-disc pl-6 mb-3 space-y-1">
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal pl-6 mb-3 space-y-1">
                    {children}
                  </ol>
                ),
                strong: ({ children }) => (
                  <strong className="font-bold text-white">
                    {children}
                  </strong>
                ),
                table: ({ children }) => (
                  <div className="overflow-x-auto my-3 max-w-full">
                    <table className="w-full min-w-[480px] text-sm border-collapse">
                      {children}
                    </table>
                  </div>
                ),
                th: ({ children }) => (
                  <th className="border border-slate-600 px-3 py-2 text-left font-bold">
                    {children}
                  </th>
                ),
                td: ({ children }) => (
                  <td className="border border-slate-700 px-3 py-2 align-top">
                    {children}
                  </td>
                ),
                hr: () => <hr className="my-4 border-slate-600" />,
                a: ({ href, children }) => (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-teal-300 underline"
                  >
                    {children}
                  </a>
                ),
              }}
            >
              {message.content || ''}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
}
