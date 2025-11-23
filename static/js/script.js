// document.addEventListener("DOMContentLoaded", () => {
//     const loginBtn = document.getElementById("loginBtn");
//     const cadastroBtn = document.getElementById("cadastroBtn");
//     const logoutBtn = document.getElementById("logoutBtn");

//     const usuarioLogado = localStorage.getItem("cpfLogado");

//     if (usuarioLogado) {
//     // Usuário logado
//     if (loginBtn) loginBtn.style.display = "none";
//     if (cadastroBtn) cadastroBtn.style.display = "none";
//     if (logoutBtn) logoutBtn.classList.remove("d-none");
//     } else {
//     // Usuário não logado
//     if (loginBtn) loginBtn.style.display = "inline-block";
//     if (cadastroBtn) cadastroBtn.style.display = "inline-block";
//     if (logoutBtn) logoutBtn.classList.add("d-none");
//     }

//     // Logout
//     if (logoutBtn) {
//     logoutBtn.addEventListener("click", () => {
//         localStorage.removeItem("cpfLogado");
//         if (loginBtn) loginBtn.style.display = "inline-block";
//         if (cadastroBtn) cadastroBtn.style.display = "inline-block";
//         if (logoutBtn) logoutBtn.classList.add("d-none");
//         alert("Você saiu da sua conta.");
//         window.location.href = "index.html";
//     });
//     }
// });