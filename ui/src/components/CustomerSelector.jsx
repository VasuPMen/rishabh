import React, { useEffect, useState } from "react";
import { fetchCustomers } from "../api.js";
import styles from "./CustomerSelector.module.css";

export default function CustomerSelector({ onStartReview }) {
  const [customers, setCustomers] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [manualName, setManualName] = useState("");
  const [inputMode, setInputMode] = useState("select"); // "select" | "manual"
  const [loading, setLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchCustomers()
      .then((data) => {
        setCustomers(data);
        if (data.length > 0) setSelectedId(data[0].id);
      })
      .catch((err) => setFetchError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleStart = () => {
    if (inputMode === "select" && selectedId) {
      const c = customers.find((x) => x.id === selectedId);
      onStartReview({ customerId: selectedId, customerName: c?.name });
    } else if (inputMode === "manual" && manualName.trim()) {
      onStartReview({ customerName: manualName.trim() });
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.icon}>
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="16" fill="#e8f1fc"/>
            <path d="M16 10a3 3 0 100 6 3 3 0 000-6zm-6 10c0-2.21 2.69-4 6-4s6 1.79 6 4v1H10v-1z" fill="#0070f2"/>
          </svg>
        </div>
        <div>
          <h2 className={styles.title}>Start a Billing Review</h2>
          <p className={styles.subtitle}>Select a customer or enter a name to begin</p>
        </div>
      </div>

      <div className={styles.toggle}>
        <button
          className={`${styles.toggleBtn} ${inputMode === "select" ? styles.active : ""}`}
          onClick={() => setInputMode("select")}
        >
          Choose from list
        </button>
        <button
          className={`${styles.toggleBtn} ${inputMode === "manual" ? styles.active : ""}`}
          onClick={() => setInputMode("manual")}
        >
          Enter name
        </button>
      </div>

      {inputMode === "select" ? (
        <div className={styles.field}>
          <label className={styles.label}>Customer</label>
          {fetchError ? (
            <p className={styles.error}>Could not load customers. The agent service may be offline.</p>
          ) : loading ? (
            <p className={styles.hint}>Loading customers…</p>
          ) : (
            <select
              className={styles.select}
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
            >
              {customers.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.id})
                </option>
              ))}
            </select>
          )}
        </div>
      ) : (
        <div className={styles.field}>
          <label className={styles.label}>Customer Name or ID</label>
          <input
            className={styles.input}
            type="text"
            placeholder="e.g. Horizon Tech GmbH or C001"
            value={manualName}
            onChange={(e) => setManualName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleStart()}
          />
        </div>
      )}

      <button
        className={styles.startBtn}
        onClick={handleStart}
        disabled={
          (inputMode === "select" && !selectedId) ||
          (inputMode === "manual" && !manualName.trim())
        }
      >
        Review Account
      </button>

      <div className={styles.customerGrid}>
        <p className={styles.hint}>Available demo customers:</p>
        {customers.map((c) => (
          <button
            key={c.id}
            className={`${styles.customerChip} ${selectedId === c.id && inputMode === "select" ? styles.selectedChip : ""}`}
            onClick={() => { setInputMode("select"); setSelectedId(c.id); }}
          >
            <span className={styles.chipId}>{c.id}</span>
            <span>{c.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
