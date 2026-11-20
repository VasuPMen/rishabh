import React from "react";
import styles from "./ShellBar.module.css";

export default function ShellBar() {
  return (
    <header className={styles.shell}>
      <div className={styles.inner}>
        <div className={styles.left}>
          <div className={styles.logo}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <rect width="24" height="24" rx="4" fill="#0070f2"/>
              <path d="M6 17l3-6 3 4 2-3 4 5H6z" fill="white" opacity="0.9"/>
            </svg>
          </div>
          <span className={styles.appName}>Customer Billing Review Agent</span>
        </div>
        <div className={styles.right}>
          <span className={styles.badge}>Read-Only</span>
        </div>
      </div>
    </header>
  );
}
