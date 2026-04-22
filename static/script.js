/**
 * Pens Dashboard - Client-side utilities and interactivity
 */

const API_BASE = "/api";

/**
 * Fetch all players from the roster API
 */
async function fetchRoster(position = null, limit = 100) {
  const params = new URLSearchParams();
  if (position) params.append("pos", position);
  params.append("limit", limit);

  const response = await fetch(`${API_BASE}/roster?${params}`);
  if (!response.ok) throw new Error("Failed to fetch roster");
  return response.json();
}

/**
 * Fetch player statistics
 */
async function fetchStats(position = null, limit = 100) {
  const params = new URLSearchParams();
  if (position) params.append("pos", position);
  params.append("limit", limit);

  const response = await fetch(`${API_BASE}/stats?${params}`);
  if (!response.ok) throw new Error("Failed to fetch stats");
  return response.json();
}

/**
 * Fetch top scorers
 */
async function fetchTopScorers(limit = 10) {
  const response = await fetch(`${API_BASE}/top-scorers?limit=${limit}`);
  if (!response.ok) throw new Error("Failed to fetch top scorers");
  return response.json();
}

/**
 * Fetch data for a specific player
 */
async function fetchPlayerDetail(playerName) {
  const response = await fetch(`${API_BASE}/players/${encodeURIComponent(playerName)}`);
  if (!response.ok) throw new Error("Player not found");
  return response.json();
}

/**
 * Search players by name and position
 */
async function searchPlayers(query = "", position = "") {
  const roster = await fetchRoster(position || null, 200);

  if (!query) {
    return roster;
  }

  const queryLower = query.toLowerCase();
  return roster.filter((player) =>
    player.player.toLowerCase().includes(queryLower)
  );
}

/**
 * Dynamically render top scorers table (for client-side enhancement)
 */
async function renderTopScorers(containerId, limit = 10) {
  const container = document.getElementById(containerId);
  if (!container) return;

  try {
    const scorers = await fetchTopScorers(limit);

    let html =
      "<table><thead><tr><th>Player</th><th>Pos</th><th>GP</th><th>G</th><th>A</th><th>P</th></tr></thead><tbody>";

    scorers.forEach((scorer) => {
      html += `<tr>
        <td><a href="/players/${encodeURIComponent(scorer.player)}">${scorer.player}</a></td>
        <td>${scorer.pos || "-"}</td>
        <td>${scorer.gp || "-"}</td>
        <td>${scorer.goals || "-"}</td>
        <td>${scorer.assists || "-"}</td>
        <td>${scorer.points || "-"}</td>
      </tr>`;
    });

    html += "</tbody></table>";
    container.innerHTML = html;
  } catch (error) {
    console.error("Error rendering top scorers:", error);
    container.innerHTML = "<p>Error loading top scorers</p>";
  }
}

/**
 * Dynamically render roster table (for client-side enhancement)
 */
async function renderRoster(containerId, position = "") {
  const container = document.getElementById(containerId);
  if (!container) return;

  try {
    const players = await fetchRoster(position || null);

    let html =
      "<table><thead><tr><th>Player</th><th>#</th><th>Pos</th><th>Sh</th><th>Ht</th><th>Wt</th></tr></thead><tbody>";

    players.forEach((player) => {
      html += `<tr>
        <td><a href="/players/${encodeURIComponent(player.player)}">${player.player}</a></td>
        <td>${player.number || "-"}</td>
        <td>${player.pos || "-"}</td>
        <td>${player.sh || "-"}</td>
        <td>${player.ht || "-"}</td>
        <td>${player.wt || "-"}</td>
      </tr>`;
    });

    html += "</tbody></table>";
    container.innerHTML = html;
  } catch (error) {
    console.error("Error rendering roster:", error);
    container.innerHTML = "<p>Error loading roster</p>";
  }
}

/**
 * Set up live search functionality
 */
function setupLiveSearch(inputSelector, tableSelector, apiCall) {
  const searchInput = document.querySelector(inputSelector);
  const tableBody = document.querySelector(tableSelector);

  if (!searchInput || !tableBody) return;

  searchInput.addEventListener("input", async (e) => {
    const query = e.target.value.trim();

    if (query.length === 0) {
      await apiCall();
      return;
    }

    try {
      const results = await searchPlayers(query);
      renderTableRows(tableBody, results);
    } catch (error) {
      console.error("Search error:", error);
    }
  });
}

/**
 * Helper: render table rows from player data
 */
function renderTableRows(tableBody, players) {
  tableBody.innerHTML = "";

  players.forEach((player) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><a href="/players/${encodeURIComponent(player.player)}">${player.player}</a></td>
      <td>${player.number || "-"}</td>
      <td>${player.pos || "-"}</td>
      <td>${player.sh || "-"}</td>
      <td>${player.ht || "-"}</td>
      <td>${player.wt || "-"}</td>
    `;
    tableBody.appendChild(row);
  });

  if (players.length === 0) {
    tableBody.innerHTML =
      '<tr><td colspan="6" style="text-align: center;">No players found</td></tr>';
  }
}

/**
 * Filter players by position
 */
async function filterByPosition(position) {
  if (!position) {
    return fetchRoster();
  }
  return fetchRoster(position);
}

/**
 * Check API health
 */
async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    return response.ok;
  } catch (error) {
    console.error("Health check failed:", error);
    return false;
  }
}

/**
 * Initialize on page load
 */
document.addEventListener("DOMContentLoaded", () => {
  // Optional: Add any initialization logic here
  console.log("Pens Dashboard loaded");

  // Check API health
  checkHealth().then((isHealthy) => {
    if (!isHealthy) {
      console.warn("API is not responding");
    }
  });
});
