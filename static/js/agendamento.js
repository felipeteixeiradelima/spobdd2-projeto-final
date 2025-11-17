document.addEventListener("DOMContentLoaded", () => {
    const cpf = localStorage.getItem("cpfLogado");
    const logoutBtn = document.getElementById("logoutBtn");

    if (!cpf) {
    alert("Você precisa estar logado para acessar esta página.");
    window.location.href = "login.html";
    } else {
    logoutBtn.classList.remove("d-none");
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("cpfLogado");
        window.location.href = "index.html";
    });
    }

    const form = document.getElementById("formAgendamento");
    const msg = document.getElementById("mensagemSucesso");

    form.addEventListener("submit", (e) => {
    e.preventDefault();
    form.reset();
    msg.classList.remove("d-none");
    setTimeout(() => msg.classList.add("d-none"), 4000);
    });
});