const API = "/api/items";
const PAGE_SIZE = 5;

const state = { page: 1, totalPages: 1, search: "" };

const $ = (sel) => document.querySelector(sel);

function showMessage(text, kind) {
  const el = $("#message");
  el.textContent = text;
  el.className = kind;
}

async function request(url, options = {}) {
  const res = await fetch(url, options);
  if (res.status === 204) return null;
  const body = await res.json();
  if (!res.ok) throw new Error(body.error || `Request failed (${res.status})`);
  return body;
}

async function loadItems() {
  const params = new URLSearchParams({ page: state.page, limit: PAGE_SIZE });
  if (state.search) params.set("search", state.search);

  const result = await request(`${API}?${params}`);
  state.totalPages = Math.max(result.total_pages, 1);
  renderItems(result.data);
  $("#page-info").textContent = `Page ${result.page} of ${state.totalPages}`;
  $("#prev").disabled = state.page <= 1;
  $("#next").disabled = state.page >= state.totalPages;
}

function renderItems(items) {
  const tbody = $("#items");
  tbody.innerHTML = "";
  for (const item of items) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.id}</td>
      <td>${escapeHtml(item.name)}</td>
      <td>${escapeHtml(item.category)}</td>
      <td>$${item.price.toFixed(2)}</td>
      <td class="${item.quantity < 10 ? "low" : ""}">${item.quantity}</td>
      <td><button data-id="${item.id}">Delete</button></td>`;
    tbody.appendChild(row);
  }
}

async function loadStats() {
  const s = await request(`${API}/stats`);
  $("#stats").innerHTML = `
    <div class="stat">Items<b>${s.total_items}</b></div>
    <div class="stat">Units<b>${s.total_units}</b></div>
    <div class="stat">Stock value<b>$${s.total_value.toFixed(2)}</b></div>
    <div class="stat">Avg price<b>$${s.average_price.toFixed(2)}</b></div>
    <div class="stat">Low stock<b>${s.low_stock.length}</b></div>`;
}

async function refresh() {
  try {
    await Promise.all([loadItems(), loadStats()]);
  } catch (err) {
    showMessage(err.message, "error");
  }
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

$("#search").addEventListener("input", (e) => {
  state.search = e.target.value.trim();
  state.page = 1;
  refresh();
});

$("#prev").addEventListener("click", () => { state.page -= 1; refresh(); });
$("#next").addEventListener("click", () => { state.page += 1; refresh(); });

$("#items").addEventListener("click", async (e) => {
  const id = e.target.dataset.id;
  if (!id) return;
  try {
    await request(`${API}/${id}`, { method: "DELETE" });
    showMessage(`Deleted item ${id}`, "ok");
    await refresh();
  } catch (err) {
    showMessage(err.message, "error");
  }
});

$("#add-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const payload = {
    name: form.name.value,
    category: form.category.value,
    price: parseFloat(form.price.value),
    quantity: parseInt(form.quantity.value, 10),
  };
  try {
    const item = await request(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    showMessage(`Added "${item.name}"`, "ok");
    form.reset();
    await refresh();
  } catch (err) {
    showMessage(err.message, "error");
  }
});

refresh();
