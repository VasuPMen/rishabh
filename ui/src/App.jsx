import React, { useState } from "react";
import ShellBar from "./components/ShellBar.jsx";
import CustomerSelector from "./components/CustomerSelector.jsx";
import ChatPanel from "./components/ChatPanel.jsx";
import styles from "./App.module.css";

export default function App() {
  const [review, setReview] = useState(null); // { customerId?, customerName? }

  const handleStartReview = (params) => {
    setReview(params);
  };

  const handleBack = () => {
    setReview(null);
  };

  return (
    <div className={styles.app}>
      <ShellBar />
      <main className={styles.main}>
        {!review ? (
          <CustomerSelector onStartReview={handleStartReview} />
        ) : (
          <ChatPanel
            customerId={review.customerId}
            customerName={review.customerName}
            onBack={handleBack}
          />
        )}
      </main>
    </div>
  );
}
