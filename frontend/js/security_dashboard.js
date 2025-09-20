const token = localStorage.getItem("token"); // stored at login

// Fetch residents for dropdown
async function loadResidents() {
  const res = await fetch("http://127.0.0.1:8000/visitors/resident/all", {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    console.error("Failed to load residents");
    return;
  }

  const residents = await res.json();
  const select = document.getElementById("residentSelect");
  select.innerHTML = ""; // clear existing options

  residents.forEach(r => {
    const option = document.createElement("option");
    option.value = r.id;
    option.text = r.name;
    select.appendChild(option);
  });
}

// Create visitor
document.getElementById("createVisitorForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("visitorName").value;
  const phone = document.getElementById("visitorPhone").value;
  const visitor_type = document.getElementById("visitorType").value;
  const resident_id = document.getElementById("residentSelect").value;

  const res = await fetch("http://127.0.0.1:8000/visitors/", {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ name, phone, visitor_type, resident_id })
  });

  if (res.ok) {
    alert("Visitor created successfully!");
    loadVisitors(); // refresh the visitors table
  } else {
    const error = await res.json();
    alert(error.detail || "Failed to create visitor");
  }
});

// Fetch today's visitors (existing code)
async function loadVisitors() {
  const res = await fetch("http://127.0.0.1:8000/security/visits", {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    document.getElementById("visitors-today").innerText = "Failed to load visitors";
    return;
  }

  const visits = await res.json();
  const div = document.getElementById("visitors-today");
  div.innerHTML = "";

  visits.forEach(v => {
    const row = document.createElement("div");
    row.innerHTML = `
      ${v.visitor_name} (${v.phone}) - Status: ${v.status}
      ${v.status === "approved" ? `<button onclick="checkIn(${v.id})">Check In</button>` : ""}
      ${v.status === "checked_in" ? `<button onclick="checkOut(${v.id})">Check Out</button>` : ""}
    `;
    div.appendChild(row);
  });
}

// Check-in/out functions (existing)
async function checkIn(id) {
  await fetch(`http://127.0.0.1:8000/visits/checkin/${id}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });
  loadVisitors();
}

async function checkOut(id) {
  await fetch(`http://127.0.0.1:8000/visits/checkout/${id}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });
  loadVisitors();
}

// Initial load
loadResidents();
loadVisitors();
