document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, phone, email, password, role }),
    });

    if (res.ok) {
      alert("Registration successful! Redirecting to login...");
      window.location.href = "login.html"; // Redirect after successful signup
    } else {
      const error = await res.json();
      alert(error.detail || "Registration failed!");
    }
  } catch (err) {
    console.error(err);
    alert("Server error. Please try again later.");
  }
});
