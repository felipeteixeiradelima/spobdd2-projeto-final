// Obtém o URL da página
const currentURL = window.location.href;

// ============================== AGENDAMENTO ==============================

if (currentURL.endsWith("/agendamento/")) {
    // AJAX que pega os Pontos de Coleta para a campanha selecionada pelo usuário

    document.addEventListener("DOMContentLoaded", function () {
        const campoCampanha = document.getElementById("id_campanha");
        const campoPonto = document.getElementById("id_ponto");

        campoCampanha.addEventListener("change", function () {
            const campanhaId = this.value;

            campoPonto.innerHTML = '<option>Carregando...</option>';

            fetch(`../ajax/pontos-por-campanha/${campanhaId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Erro ao carregar pontos");
                    }
                    return response.json();
                })
                .then(data => {
                    campoPonto.innerHTML = "";

                    if (!data.pontos || data.pontos.length === 0) {
                        campoPonto.innerHTML = '<option value="">Nenhum ponto disponível</option>';
                        return;
                    }

                    data.pontos.forEach(p => {
                        const opt = document.createElement("option");
                        opt.value = p.id_ponto;
                        opt.textContent = p.nome;
                        campoPonto.appendChild(opt);
                    });
                })
                .catch(() => {
                    campoPonto.innerHTML = '<option value="">Nenhum ponto disponível</option>';
                });
        });
    });
}


// ============================== LOGIN/CADASTRO ==============================

if (currentURL.endsWith("/login/") | currentURL.endsWith("/cadastro/")) {
    // ======== FORMATAÇÃO DE CAMPOS =========

    // CPF
    function formatarCPF() {
    const cpf = document.getElementById('cpf');
    if (cpf) {
        IMask(cpf, {mask: '000.000.000-00'});
    }
    }

    formatarCPF();

    // Telefone (aceita 8 ou 9 dígitos)
    function formatarTelefone () {
    const telefone = document.getElementById('telefone');
    if (telefone) {
        IMask(telefone, {mask: ['(00) 0000-0000', '(00) 00000-0000']});
    }
    }

    formatarTelefone();

    // CEP
    function formatarCEP () {
    const cep = document.getElementById('cep');
    if (cep) {
        IMask(cep, {mask: '00000-000'});
    }
    }

    formatarCEP();

    // ========= VALIDAÇÃO DE CAMPOS =========

    // ========= VALIDAÇÃO DE CPF =========
    const cpfInput = document.getElementById("cpf");

    function isCpfValido(cpf) {
    if (!cpf || cpf.length !== 11) return false;
    if (/^(\d)\1{10}$/.test(cpf)) return false; // evita todos os dígitos iguais

    let soma = 0;
    for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
    let resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    return resto === parseInt(cpf.charAt(10));
    }

    function validarCPF () {
    if (!cpfInput || !isCpfValido(cpfInput.value.replace(/\D/g, ""))) {
        cpfInput.setCustomValidity("CPF inválido.");
    } else {
        cpfInput.setCustomValidity("");
    }
    }

    // Adiciona EventListener para ativar validação

    document.addEventListener("DOMContentLoaded", validarCPF);
    if (cpfInput) {
    cpfInput.addEventListener("input", validarCPF);
    }

    // ========= VALIDAÇÃO DE TELEFONE =========
    const telefoneInput = document.getElementById("telefone");

    function validarTelefone () {
    const telefone = telefoneInput.value.trim();
    const regexTelefone = /^\(\d{2}\)\s?\d{4,5}-\d{4}$/;
    if (!regexTelefone.test(telefone)) {
        telefoneInput.setCustomValidity("Telefone inválido. Use o formato (00) 0000-0000 ou (00) 00000-0000.");
    } else {
        telefoneInput.setCustomValidity("");
    }
    }

    if (telefoneInput) {
    document.addEventListener("DOMContentLoaded", validarTelefone);
    telefoneInput.addEventListener("input", validarTelefone);
    }

    // ========= VALIDAÇÃO DE CEP =========
    const cepInput = document.getElementById("cep");

    function validarCEP () {
    const cep = cepInput.value.trim();
    const regexCEP = /^\d{5}-\d{3}$/;
    if (!regexCEP.test(cep)) {
        cepInput.setCustomValidity("CEP inválido. Use o formato 00000-000.");
    } else {
        cepInput.setCustomValidity("");
    }
    
    }
    if (cepInput) {
    document.addEventListener("DOMContentLoaded", validarCEP);
    cepInput.addEventListener("input", validarCEP);
    }

    // ======== VALIDAÇÃO DE SENHA =========
    const senhaInput = document.getElementById("senha");
    const confirmarSenhaInput = document.getElementById("confirmarSenha");
    const senhasDiferentes = document.getElementById("senhasDiferentes");
    const senhaInvalida = document.getElementById("senhaInvalida");

    function validarSenha() {
    if (!senhaInput | !confirmarSenhaInput) {
        return;
    }

    const regexSenha = /^[A-Za-z0-9@_\*\-\.\#!\$%&\+=\?\^~]{8,20}$/;
    const senhaValida = regexSenha.test(senhaInput.value);
    const senhasIguais = senhaInput.value === confirmarSenhaInput.value;

    // Valida se as senhas são iguais
    // Se não, mostra mensagem de senha inválida
    if (!senhaValida) {
        senhaInput.setCustomValidity("A senha deve ter entre 8 e 20 caracteres e pode conter apenas letras e os símbolos @, _ e *.");
        senhaInvalida.style.display = "block";
    } else if (!senhasIguais) {
        confirmarSenhaInput.setCustomValidity("As senhas não coincidem.");
        senhaInvalida.style.display = "none";
        senhasDiferentes.style.display = "block";
    } else {
        senhaInput.setCustomValidity("");
        confirmarSenhaInput.setCustomValidity("");
        senhasDiferentes.style.display = "none";
    }
    }

    if (senhaInput) {
    senhaInput.addEventListener("input", validarSenha);
    }
    if (confirmarSenhaInput) {
    confirmarSenhaInput.addEventListener("input", validarSenha);
    }
}


// ============================== CAMPANHAS ==============================

if (currentURL.endsWith("/campanhas/")) {


    document.addEventListener("DOMContentLoaded", function() {
        const tbody = document.getElementById("campanhas-table-body");

        fetch("ajax/campanhas-json")
            .then(response => response.json())
            .then(data => {
                const campanhas = data.campanhas;

                tbody.innerHTML = ""; // limpa "Carregando"

                if (campanhas.length === 0) {
                    tbody.innerHTML = `
                        <tr>
                        <td colspan="6" class="text-center text-muted py-3">
                            Não há campanhas disponíveis no momento.
                        </td>
                        </tr>`;
                    return;
                }

                campanhas.forEach(c => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${c.id}</td>
                            <td>${c.nome}</td>
                            <td>${c.data_inicio}</td>
                            <td>${c.data_fim}</td>
                            <td>
                                <span class="badge bg-warning text-dark">${c.status}</span>
                            </td>
                            <td>
                                <a href="${c.detail_url}" class="btn btn-outline-danger btn-sm">
                                    <i class="bi bi-calendar-heart"></i> Detalhes
                                </a>
                            </td>
                        </tr>
                    `;
                });
            })
            .catch(() => {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center text-danger py-3">
                            Erro ao carregar campanhas. Tente novamente mais tarde.
                        </td>
                    </tr>`;
            });
    });
}
