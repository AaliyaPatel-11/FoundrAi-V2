import React from 'react';
import { Lightbulb, Rocket, CheckCircle, ShieldAlert } from 'lucide-react';

export default function WelcomeScreen({ onSelectStarter }) {
  const starters = [
    {
      text: "I have a startup idea",
      icon: <Lightbulb className="w-5 h-5 text-amber-400" />,
      description: "Refine and structure your rough startup concept."
    },
    {
      text: "I want to build an app",
      icon: <Rocket className="w-5 h-5 text-sky-400" />,
      description: "Define MVP features, roadmap, and tech stack."
    },
    {
      text: "Help me validate an idea",
      icon: <CheckCircle className="w-5 h-5 text-emerald-400" />,
      description: "Devise validation steps and user testing plans."
    },
    {
      text: "Challenge my startup idea",
      icon: <ShieldAlert className="w-5 h-5 text-rose-400" />,
      description: "Stress test assumptions, risks, and competitors."
    }
  ];

  return (
    <div className="flex flex-col items-center justify-center max-w-2xl mx-auto px-4 py-8 text-center select-none">
      <div className="mb-6 relative">
        <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-accent-teal to-accent-violet opacity-75 blur-lg animate-pulse"></div>
        <div className="relative bg-[#0f172a] p-4 rounded-full border border-slate-700">
          <Rocket className="w-12 h-12 text-accent-teal" />
        </div>
      </div>
      
      <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400 mb-2">
        FondrAI
      </h1>
      <p className="text-lg sm:text-xl font-medium text-accent-teal mb-4">
        Turn an idea into a startup.
      </p>
      <p className="text-slate-400 max-w-md mb-10 text-sm sm:text-base leading-relaxed">
        Your AI co-founder for turning rough ideas into real, structured, and actionable startup plans.
      </p>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        {starters.map((starter, index) => (
          <button
            key={index}
            onClick={() => onSelectStarter(starter.text)}
            className="glass-card p-5 rounded-2xl text-left flex items-start space-x-4 outline-none focus:ring-2 focus:ring-accent-teal/50 cursor-pointer"
          >
            <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700/50 flex-shrink-0">
              {starter.icon}
            </div>
            <div>
              <h3 className="font-semibold text-slate-200 text-sm sm:text-base mb-0.5">
                {starter.text}
              </h3>
              <p className="text-xs text-slate-400 leading-normal">
                {starter.description}
              </p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
