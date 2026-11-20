/**
 * API client — calls the CAP backend which proxies to the Python agent.
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export async function fetchCustomers() {
  let res = await fetch(`${BASE_URL}/customers`);
  if (!res.ok && res.status === 404) {
    res = await fetch(`${BASE_URL}/customers()`);
  }
  if (!res.ok) throw new Error(`Failed to load customers: ${res.status}`);
  const data = await res.json();
  // CAP wraps function results in { value: [...] }
  return Array.isArray(data) ? data : data.value ?? [];
}

export async function sendChatMessage({ message, history, customerId, customerName }) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      history,
      customer_id: customerId || undefined,
      customer_name: customerName || undefined,
    }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Agent request failed (${res.status}): ${err}`);
  }
  return res.json();
}
