function loginUser() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;
  const error = document.getElementById("error-msg");

  if (!username || !password || !role) {
    error.textContent = "⚠️ Please fill in all fields!";
    return;
  }

  // Simple login check
  if (username === "admin" && password === "1234") {
    window.location.href = "dashboard.html";
  } else {
    error.textContent = "❌ Invalid username or password!";
  }
}
function submitBug() {
  const title = document.getElementById("bugTitle").value;
  const project = document.getElementById("projectName").value;
  const desc = document.getElementById("bugDesc").value;
  const severity = document.getElementById("severity").value;
  const assignTo = document.getElementById("assignTo").value;
  const date = document.getElementById("reportDate").value;
  const msg = document.getElementById("bug-msg");

  if (!title || !project || !desc || !severity || !assignTo || !date) {
    msg.style.color = "red";
    msg.textContent = "⚠️ Please fill in all fields!";
    return;
  }

  msg.style.color = "green";
  msg.textContent = "✅ Bug reported successfully!";

  // Clear form
  document.getElementById("bugTitle").value = "";
  document.getElementById("projectName").value = "";
  document.getElementById("bugDesc").value = "";
  document.getElementById("severity").value = "";
  document.getElementById("assignTo").value = "";
  document.getElementById("reportDate").value = "";
}