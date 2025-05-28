let btn_cotacao = document.getElementById('Hcotacao');
let btn_participacao = document.getElementById('Hparticipacao');
let btn_acesso = document.getElementById('Hacesso');
console.log(btn_cotacao, btn_participacao, btn_acesso);

const historicoP = document.getElementById('historicoP');
const historicoC = document.getElementById('HistoricoC');
const historicoA = document.getElementById('historicoA');
console.log(historicoP, historicoC, historicoA);

btn_cotacao.addEventListener('click', function() {
    historicoC.classList.remove('displayNone');
    historicoC.classList.add('displayFlex');
    historicoP.classList.remove('displayFlex');
    historicoP.classList.add('displayNone'); 
    historicoA.classList.remove('displayFlex');
    historicoA.classList.add('displayNone');
});

btn_participacao.addEventListener('click', function() {
    historicoP.classList.remove('displayNone');
    historicoP.classList.add('displayFlex');
    historicoC.classList.remove('displayFlex');
    historicoC.classList.add('displayNone');
    historicoA.classList.remove('displayFlex');
    historicoA.classList.add('displayNone');
});

btn_acesso.addEventListener('click', function() {
    historicoA.classList.remove('displayNone');
    historicoA.classList.add('displayFlex');
    historicoP.classList.remove('displayFlex');
    historicoP.classList.add('displayNone');
    historicoC.classList.remove('displayFlex');
    historicoC.classList.add('displayNone');
});