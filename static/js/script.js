// Obtém o URL da página
const currentURL = window.location.href;

// ============================== AGENDAMENTO ==============================

if (currentURL.endsWith("/agendamento/")) {

    document.addEventListener("DOMContentLoaded", function () {

        // AJAX que pega os Pontos de Coleta para a campanha selecionada pelo usuário
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

if (
    currentURL.endsWith("/login/")
    | currentURL.endsWith("/cadastro/")
    | currentURL.includes("/cadastro-colaborador/"
    | currentURL.includes("/pontos/cadastrar/")
)) {
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

    if (cpfInput) {
        document.addEventListener("DOMContentLoaded", validarCPF);
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

    // DataTables
    $("#campanhasTable").DataTable({
        ajax: {
            url: "/ajax/campanhas-json"
        },
        columns: [
            { data: "id" },
            { data: "nome" },
            { data: "data_inicio" },
            { data: "data_fim" },
            { 
                data: "status",
                render: function (data) {
                    let badgeClass = {
                        "Ativa": "success",
                        "Planejada": "primary",
                        "Cancelada": "danger",
                        "Finalizada": "secondary"
                    }[data] || "secondary";

                    return `<span class="badge bg-${badgeClass}">${data}</span>`;
                }
            },
            {
                data: "id",
                render: function (data) {
                    console.log(data)
                    return `
                        <a href="${data}" class="btn btn-outline-danger btn-sm">
                            <i class="bi bi-calendar-heart"></i> Detalhes
                        </a>`;
                }
            }
        ],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
        },
        responsive: true,
        autoWidth: false
    });
}

// ============================== MEUS AGENDAMENTOS ==============================
if (currentURL.endsWith("/meus-agendamentos/")) {
    document.addEventListener("DOMContentLoaded", function () {
        
        // DataTables
        $("#agendamentosTable").DataTable({
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            responsive: true,
            autoWidth: false
        });
    });
}

// ============================== COLABORADORES ==============================
if (currentURL.endsWith("/colaboradores/")) {
    document.addEventListener("DOMContentLoaded", function () {
        
        // DataTables
        $("#colaboradoresTable").DataTable({
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            responsive: true,
            autoWidth: false
        });
    });
}

// ============================== DOADORES ==============================
if (currentURL.endsWith("/doadores/")) {
    document.addEventListener("DOMContentLoaded", function () {
        
        // DataTables
        $("#doadoresTable").DataTable({
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            responsive: true,
            autoWidth: false
        });
    });
}

// ============================== AMOSTRAS DE SANGUE ==============================
if (currentURL.endsWith("/amostras/")) {
    document.addEventListener("DOMContentLoaded", function () {
        
        // DataTables
        $("#amostrasTable").DataTable({
            language: {
                url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            responsive: true,
            autoWidth: false
        });
    });
}

// ============================== PONTOS DE COLETA ==============================
if (currentURL.endsWith("/pontos/")) {
    document.addEventListener("DOMContentLoaded", function () {
        
        // DataTables
        $('#pontosTable').DataTable({
            language: {
                url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            responsive: true,
            autoWidth: false
        });
    });
}

// ============================== DOAÇÕES ==============================
if (currentURL.endsWith("/doacoes/")) {
    document.addEventListener("DOMContentLoaded", function () {
        
        // DataTables
        $('#doacoesTable').DataTable({
            language: {
                url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
            },
            responsive: true,
            autoWidth: false
        });
    });
}
