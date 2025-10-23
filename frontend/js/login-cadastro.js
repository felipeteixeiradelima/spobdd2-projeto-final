// ======== FORMATAÇÃO DE CAMPOS =========

// CPF
function formatarCPF() {
  const cpf = document.getElementById('cpf')
  if (cpf) {
    IMask(cpf, {mask: '000.000.000-00'});
  }
}

formatarCPF();

// Telefone (aceita 8 ou 9 dígitos)
function formatarTelefone () {
  const telefone = document.getElementById('telefone')
  if (telefone) {
    IMask(telefone, {mask: ['(00) 0000-0000', '(00) 00000-0000']});
  }
}

formatarTelefone();

// CEP
function formatarCEP () {
  const cep = document.getElementById('cep')
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
  const cpf = cpfInput.value.replace(/\D/g, ""); // só números
  console.log(cpf)
  if (!isCpfValido(cpf)) {
    cpfInput.setCustomValidity("CPF inválido.");
  } else {
    cpfInput.setCustomValidity("");
  }
}

document.addEventListener("DOMContentLoaded", validarCPF);
if (cpfInput) {
  console.log("cpf detectado")
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
  const regexSenha = /^[A-Za-z0-9@_\*\-\.\#!\$%&\+=\?\^~]{8,20}$/;
  const senhaValida = regexSenha.test(senhaInput.value);
  const senhasIguais = senhaInput.value === confirmarSenhaInput.value;


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

