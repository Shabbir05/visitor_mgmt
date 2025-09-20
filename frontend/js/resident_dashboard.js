const token = localStorage.getItem("token");

// Load all visitors for this resident
async function loadVisitors() {
  const res = await fetch("http://127.0.0.1:8000/resident/visitors", {
    headers: { Authorization: `Bearer ${token}` }
  });

  const pendingDiv = document.getElementById("pending-visitors");
  const allDiv = document.getElementById("all-visitors");

  pendingDiv.innerHTML = "";
  allDiv.innerHTML = "";

  if(!res.ok){
    pendingDiv.innerText = "Failed to load visitors";
    allDiv.innerText = "Failed to load visitors";
    return;
  }

  const visitors = await res.json();

  // Pending approvals
  visitors.filter(v => v.status === "pending").forEach(v => {
    const row = document.createElement("div");
    row.innerHTML = `
      ${v.name} (${v.phone})
      <button onclick="approveVisitor(${v.visit_id})">Approve</button>
      <button onclick="denyVisitor(${v.visit_id})">Deny</button>
    `;
    pendingDiv.appendChild(row);
  });

  // All visitors
  visitors.forEach(v => {
    const row = document.createElement("div");
    row.innerText = `${v.name} (${v.phone}) - Status: ${v.status}`;
    allDiv.appendChild(row);
  });
}

// Approve a visitor
async function approveVisitor(visitId) {
  const res = await fetch(`http://127.0.0.1:8000/approvals/approve/${visitId}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });

  if(!res.ok){
    alert("Failed to approve");
  }
  loadVisitors();
}

// Deny a visitor
async function denyVisitor(visitId) {
  const res = await fetch(`http://127.0.0.1:8000/approvals/deny/${visitId}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });

  if(!res.ok){
    alert("Failed to deny");
  }
  loadVisitors();
}

// Initial load
loadVisitors();
