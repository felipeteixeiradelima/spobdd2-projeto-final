/*
Formatador de campos como CPF, telefone e CEP
*/


// CPF
IMask(document.getElementById('cpf'), {mask: '000.000.000-00'});

// Telefone (aceita 8 ou 9 dígitos)
IMask(document.getElementById('telefone'), {mask: ['(00) 0000-0000', '(00) 00000-0000']});

// CEP
IMask(document.getElementById('cep'), {mask: '00000-000'});
