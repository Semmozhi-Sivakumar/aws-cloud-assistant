import { useState } from "react";
import { Bot, Send, Sparkles, User } from "lucide-react";

function Assistant() {
  const [question, setQuestion] = useState("");

  const handleSend = () => {
    if (!question.trim()) return;

    // For now, we are only testing the UI
    console.log(question);

    setQuestion("");
  };

  return (
    <>
      {/* Header */}
      <header className="header assistant-header">
        <div>
          <p className="eyebrow">AI CLOUD ASSISTANT</p>
          <h1>Ask your environment</h1>
          <p className="subtitle">
            Ask questions about your AWS resources, security, and environment.
          </p>
        </div>

        <div className="ai-status">
          <span className="ai-status-dot"></span>
          AI Ready
        </div>
      </header>

      {/* Assistant Container */}
      <section className="assistant-page">
        {/* Top Information */}
        <div className="assistant-intro">
          <div className="assistant-intro-icon">
            <Sparkles size={22} />
          </div>

          <div>
            <h2>AWS Cloud Intelligence</h2>
            <p>
              Ask questions in natural language and get insights based on your
              AWS environment.
            </p>
          </div>
        </div>

        {/* Chat Area */}
        <div className="chat-area">
          {/* AI Welcome Message */}
          <div className="message-row assistant-message">
            <div className="message-avatar bot-avatar">
              <Bot size={18} />
            </div>

            <div className="message-content">
              <p>
                Hello! I'm your AWS Cloud Assistant. I can help you understand
                your resources, security findings, and environment health.
              </p>
            </div>
          </div>

          {/* Sample User Message */}
          <div className="message-row user-message">
            <div className="message-content">
              <p>What security issues should I review?</p>
            </div>

            <div className="message-avatar user-avatar">
              <User size={18} />
            </div>
          </div>

          {/* Sample AI Response */}
          <div className="message-row assistant-message">
            <div className="message-avatar bot-avatar">
              <Bot size={18} />
            </div>

            <div className="message-content">
              <p>
                Your environment currently has three findings to review,
                including public S3 access, broad S3 permissions, and disabled
                S3 versioning.
              </p>
            </div>
          </div>
        </div>

        {/* Chat Input */}
        <div className="chat-input-area">
          <input
            type="text"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleSend();
              }
            }}
            placeholder="Ask about your AWS environment..."
          />

          <button onClick={handleSend}>
            <span>Send</span>
            <Send size={18} />
          </button>
        </div>
      </section>
    </>
  );
}

export default Assistant;