import React from "react";
import { marked } from "marked";
import styles from "./MessageBubble.module.css";

// Configure marked to be safe and clean
marked.setOptions({
  breaks: true,
  gfm: true,
});

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className={styles.userRow}>
        <div className={styles.userBubble}>
          <p className={styles.userText}>{message.content}</p>
          <span className={styles.time}>{formatTime(message.timestamp)}</span>
        </div>
        <div className={styles.userAvatar}>You</div>
      </div>
    );
  }

  // Parse markdown for assistant messages
  const html = marked.parse(message.content || "");

  return (
    <div className={styles.assistantRow}>
      <div className={styles.agentAvatar}>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <circle cx="8" cy="8" r="8" fill="#0070f2"/>
          <path d="M5 10.5l2-4.5 1.5 3 1.5-2 2 3.5H5z" fill="white" opacity="0.9"/>
        </svg>
      </div>
      <div className={styles.assistantBubble}>
        <div
          className={styles.markdown}
          dangerouslySetInnerHTML={{ __html: html }}
        />
        <span className={styles.time}>{formatTime(message.timestamp)}</span>
      </div>
    </div>
  );
}
