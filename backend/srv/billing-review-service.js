"use strict";

const cds = require("@sap/cds");

const AGENT_BASE_URL =
  process.env.AGENT_BASE_URL || "http://localhost:8000";

/**
 * Proxy helper — forwards a request to the Python agent service.
 */
async function callAgent(path, body) {
  const { default: fetch } = await import("node-fetch");
  const url = `${AGENT_BASE_URL}${path}`;
  const res = await fetch(url, {
    method: body ? "POST" : "GET",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Agent returned ${res.status}: ${text}`);
  }
  return res.json();
}

module.exports = cds.service.impl(async function (srv) {

  // ── POST /api/chat ────────────────────────────────────────────────────────
  srv.on("chat", async (req) => {
    const { message, history = [], customer_id, customer_name } = req.data;
    try {
      const result = await callAgent("/chat", {
        message,
        history,
        customer_id: customer_id || undefined,
        customer_name: customer_name || undefined,
      });
      return result;
    } catch (err) {
      req.error(502, `Agent service unavailable: ${err.message}`);
    }
  });

  // ── GET /api/customers ────────────────────────────────────────────────────
  srv.on("customers", async (req) => {
    try {
      const result = await callAgent("/customers");
      return result;
    } catch (err) {
      req.error(502, `Agent service unavailable: ${err.message}`);
    }
  });

  // ── GET /api/health ───────────────────────────────────────────────────────
  srv.on("health", async () => {
    return { status: "ok", service: "BillingReviewService" };
  });
});
