import {
  useEffect,
  useRef,
  useState,
} from "react";

import ReactMarkdown from "react-markdown";
import { Sparkles, Send, Loader2, Bot, User } from "lucide-react";
import { streamChat } from "../api/chat";

function ChatPanel({ statementId }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tool, setTool] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading, tool]);

  useEffect(() => {
    setMessages([]);
    setError(null);
    setInput("");
    setTool(null);
  }, [statementId]);

  async function handleSubmit(event) {
    event.preventDefault();
    const userMessage = input.trim();
    if (!userMessage || loading) return;

    setInput("");
    setError(null);
    setLoading(true);
    setTool(null);

    setMessages((previous) => [
      ...previous,
      { role: "user", content: userMessage, timestamp: new Date() },
    ]);

    let assistantMessage = "";

    try {
      await streamChat(
        statementId,
        userMessage,
        (streamEvent) => {
          if (streamEvent.type === "tool_call") {
            setTool(streamEvent.tool);
          }
          if (streamEvent.type === "tool_result") {
            setTool(null);
          }
          if (streamEvent.type === "message") {
            assistantMessage = streamEvent.content || "";
            setMessages((previous) => {
              const filtered = previous.filter(m => m.role !== "assistant-stream");
              return [...filtered, { role: "assistant-stream", content: assistantMessage }];
            });
          }
          if (streamEvent.type === "done") {
            setMessages((previous) => {
              const filtered = previous.filter(m => m.role !== "assistant-stream");
              return [...filtered, { role: "assistant", content: assistantMessage, timestamp: new Date() }];
            });
            setTool(null);
          }
          if (streamEvent.type === "error") {
            setError(streamEvent.message || "Something went wrong.");
            setMessages((previous) => previous.filter(m => m.role !== "assistant-stream"));
            setTool(null);
          }
        }
      );
    } catch (error) {
      console.error(error);
      setMessages((previous) => previous.filter(m => m.role !== "assistant-stream"));
      setError(error.message || "Unable to connect to Cashora AI.");
    } finally {
      setLoading(false);
      setTool(null);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  }

  function formatToolName(name) {
    if (!name) return "";
    const nameMap = {
      "calculate_spending": "Calculating monthly spending...",
      "search_statement": "Searching statement transactions...",
      "calculate_income": "Calculating income...",
      "get_transactions": "Fetching transactions..."
    };
    return nameMap[name] || `Running ${name.replace(/_/g, ' ')}...`;
  }

  function useSuggestion(question) {
    setInput(question);
  }

  const suggestions = [
    "How much did I spend in total?",
    "What was my largest transaction?",
    "Show spending by category",
    "Did I have any salary or EMI transactions?",
    "Show my top expenses"
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-[600px]">
      
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-white shrink-0">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-gray-900">Cashora AI</h2>
            <div className="flex items-center text-xs text-emerald-600 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
              Online & Ready
            </div>
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50">
        
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
            <div className="w-16 h-16 bg-white rounded-2xl shadow-sm border border-gray-100 flex items-center justify-center text-indigo-500 mb-2">
              <Sparkles className="w-8 h-8" />
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900">Ask Cashora AI</h3>
              <p className="text-sm text-gray-500 mt-1 max-w-sm mx-auto">
                I can help you understand your spending patterns, find specific transactions, and analyze your financial health.
              </p>
            </div>
            
            <div className="flex flex-wrap justify-center gap-2 max-w-lg mt-4">
              {suggestions.map((sugg, idx) => (
                <button
                  key={idx}
                  onClick={() => useSuggestion(sugg)}
                  className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-600 hover:border-indigo-300 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
                >
                  {sugg}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              
              <div className="shrink-0 mx-3">
                {message.role === 'user' ? (
                  <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600">
                    <User className="w-4 h-4" />
                  </div>
                ) : (
                  <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white shadow-sm">
                    <Bot className="w-4 h-4" />
                  </div>
                )}
              </div>
              
              <div className={`flex flex-col ${message.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`px-4 py-3 rounded-2xl ${
                  message.role === 'user' 
                    ? 'bg-indigo-600 text-white rounded-tr-sm' 
                    : 'bg-white border border-gray-200 text-gray-800 rounded-tl-sm shadow-sm'
                }`}>
                  {message.role === 'user' ? (
                    <div className="whitespace-pre-wrap text-sm">{message.content}</div>
                  ) : (
                    <div className="text-sm prose prose-sm max-w-none prose-indigo">
                      <ReactMarkdown
                        components={{
                          table: ({node, ...props}) => <div className="overflow-x-auto my-4"><table className="min-w-full divide-y divide-gray-200" {...props} /></div>,
                          th: ({node, ...props}) => <th className="px-3 py-2 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" {...props} />,
                          td: ({node, ...props}) => <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-600 border-t border-gray-100" {...props} />,
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                  )}
                </div>
                {message.timestamp && (
                  <span className="text-xs text-gray-400 mt-1 mx-1">
                    {message.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}

        {tool && (
          <div className="flex justify-start">
            <div className="flex items-center space-x-2 px-4 py-2 bg-indigo-50 border border-indigo-100 rounded-full text-indigo-700 text-sm ml-14">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>{formatToolName(tool)}</span>
            </div>
          </div>
        )}

        {loading && !tool && (
          <div className="flex justify-start">
            <div className="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-200 shadow-sm rounded-full text-gray-500 text-sm ml-14">
              <span className="flex space-x-1">
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
              </span>
            </div>
          </div>
        )}

        {error && (
          <div className="flex justify-center">
            <div className="px-4 py-2 bg-rose-50 border border-rose-200 rounded-lg text-rose-700 text-sm flex items-center shadow-sm">
              <span className="font-medium mr-2">Error:</span> {error}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-gray-200 shrink-0">
        <form onSubmit={handleSubmit} className="relative flex items-end max-w-4xl mx-auto">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            placeholder="Ask a question about your finances..."
            className="w-full resize-none bg-gray-50 border border-gray-300 rounded-xl py-3 pl-4 pr-12 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white transition-colors max-h-32 min-h-[50px] text-sm text-gray-900 disabled:opacity-50"
            rows={1}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2 bottom-2 p-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-gray-300 disabled:text-gray-500 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="text-center mt-2">
          <span className="text-[10px] text-gray-400">Cashora AI analyzes your local statement data only.</span>
        </div>
      </div>
    </div>
  );
}

export default ChatPanel;