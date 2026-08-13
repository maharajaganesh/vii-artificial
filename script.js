// ---------------------------------------------------------------
// GOOGLE SIGN-IN SETUP
// ---------------------------------------------------------------
// To make real "Sign in with Google" work you need a free OAuth
// Client ID from Google Cloud Console:
//   1. Go to https://console.cloud.google.com/apis/credentials
//   2. Create an "OAuth client ID" -> Application type: Web application
//   3. Add your site URL (e.g. http://localhost:5000) under
//      "Authorized JavaScript origins"
//   4. Copy the Client ID and paste it below.
// Until you do that, use the "Guest ah try pannunga" button to test
// the chat UI without real login.
const GOOGLE_CLIENT_ID = "PASTE_YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com";

function loadGoogleScript(callback) {
  const script = document.createElement("script");
  script.src = "https://accounts.google.com/gsi/client";
  script.async = true;
  script.onload = callback;
  document.head.appendChild(script);
}

function decodeJwt(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
  } catch (e) {
    return null;
  }
}

function handleGoogleCredential(response) {
  const profile = decodeJwt(response.credential);
  if (!profile) return;
  localStorage.setItem("vii_user_name", profile.given_name || profile.name || "Nanba");
  localStorage.setItem("vii_user_email", profile.email || "");
  window.location.href = "chat.html";
}

function initGoogleSignIn() {
  if (GOOGLE_CLIENT_ID.startsWith("PASTE_")) {
    // No real client ID configured yet — button falls back to a
    // clear message instead of silently failing.
    document.getElementById("google-btn").addEventListener("click", () => {
      alert("Google sign-in innum set up aagala. app.py / script.js la unga GOOGLE_CLIENT_ID podunga, illana keezha 'Guest ah try pannunga' click pannunga.");
    });
    return;
  }
  window.google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: handleGoogleCredential
  });
  window.google.accounts.id.renderButton(
    document.getElementById("google-btn"),
    { theme: "outline", size: "large", width: 320 }
  );
}

loadGoogleScript(initGoogleSignIn);

document.getElementById("guest-btn").addEventListener("click", () => {
  localStorage.setItem("vii_user_name", "Nanba");
  localStorage.setItem("vii_user_email", "");
  window.location.href = "chat.html";
});
