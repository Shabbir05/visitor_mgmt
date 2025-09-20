// login.js
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const phone = document.getElementById("phone").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      document.getElementById("message").innerText =
        data.detail || "Login failed!";
      return;
    }

    // Save token
    localStorage.setItem("token", data.access_token);

    // Decode JWT to get role (lowercase-safe)
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    const role = payload.role.toLowerCase();

    // Redirect based on role
    if (role === "resident") {
      window.location.href = "resident_dashboard.html";
    } else if (role === "security") {
      window.location.href = "security_dashboard.html";
    } else {
      alert("Unknown role. Please contact admin.");
    }
  } catch (err) {
    console.error(err);
    document.getElementById("message").innerText = "Server error. Try again.";
  }
});
