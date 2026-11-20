import React, { useState, useRef, useEffect } from "react";
import { sendChatMessage } from "../api.js";
import MessageBubble from "./MessageBubble.jsx";
import styles from "./ChatPanel.module.css";

const QUICK_ACTIONS = [
  { label: "Full billing review", message: "Please run a full billing review for this customer and provide a Customer Billing Review Summary." },
  { label: "Show billing details", message: "Show me the detailed billing information including all invoices and payment history." },
  { label: "Show contract terms", message: "What are the contract terms and credit limit for this customer?" },
  { label: "Identify discrepancies", message: "Compare the customer's payment behaviour against their contract terms and highlight any discrepancies." },
];

export default function ChatPanel({ customerId, customerName, onBack }) {
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [inputText, setInputText] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  const customerLabel = customerName || customerId || "Unknown Customer";

  // Welcome message
  useEffect(() => {
    setMessages([
      {
        id: "welcome",
        role: "assistant",
        content: `Hello! I'm ready to help you review the account for **${customerLabel}**.\n\nYou can ask me to run a full billing review, check outstanding invoices, review contract terms, or identify any payment discrepancies. What would you like to know?`,
        timestamp: new Date(),
      },
    ]);
  }, [customerLabel]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (text) => {
    const trimmed = text.trim();
    if (!trimmed || sending) return;

    const userMsg = {
      id: Date.now(),
      role: "user",
      content: trimmed,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputText("");
    setSending(true);
    setError(null);

    try {
      const result = await sendChatMessage({
        message: trimmed,
        history,
        customerId,
        customerName,
      });

      const assistantMsg = {
        id: Date.now() + 1,
        role: "assistant",
        content: result.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      // Update history (only keep user and assistant messages with text content)
      setHistory(
        (result.history || [])
          .filter((m) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.trim())
          .map((m) => ({ role: m.role, content: m.content }))
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send(inputText);
    }
  };

  return (
    <div className={styles.panel}>
      {/* Header */}
      <div className={styles.header}>
        <button className={styles.backBtn} onClick={onBack} title="Back">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M11 4L6 9l5 5" stroke="#0070f2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
        <div className={styles.customerInfo}>
          <div className={styles.avatar}>
            {customerLabel.charAt(0).toUpperCase()}
          </div>
          <div>
            <div className={styles.customerName}>{customerLabel}</div>
            {customerId && customerName && (
              <div className={styles.customerId}>ID: {customerId}</div>
            )}
          </div>
        </div>
        <button
          className={styles.newReviewBtn}
          onClick={() => {
            setHistory([]);
            setMessages([
              {
                id: "welcome-" + Date.now(),
                role: "assistant",
                content: `Conversation cleared. I'm still reviewing **${customerLabel}** — how can I help?`,
                timestamp: new Date(),
              },
            ]);
          }}
        >
          Clear chat
        </button>
      </div>

      {/* Quick actions */}
      <div className={styles.quickActions}>
        {QUICK_ACTIONS.map((qa) => (
          <button
            key={qa.label}
            className={styles.quickBtn}
            onClick={() => send(qa.message)}
            disabled={sending}
          >
            {qa.label}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div className={styles.messages}>
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {sending && (
          <div className={styles.typingIndicator}>
            <span></span><span></span><span></span>
          </div>
        )}
        {error && (
          <div className={styles.errorBanner}>
            <strong>Error:</strong> {error}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className={styles.inputArea}>
        <textarea
          ref={textareaRef}
          className={styles.textarea}
          placeholder="Ask about invoices, payment terms, discrepancies… (Enter to send)"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
          disabled={sending}
        />
        <button
          className={styles.sendBtn}
          onClick={() => send(inputText)}
          disabled={sending || !inputText.trim()}
          title="Send"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M17.5 2.5L2.5 8.75l5.833 1.667L10.833 17.5l6.667-15z" fill="white"/>
          </svg>
        </button>
      </div>
    </div>
  );
}
