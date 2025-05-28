let notificationBell = document.querySelector('#badge');

console.log(notificationBell);
fetch('/notificacaoCount')
    .then(response => response.json())
    .then(data => {
        if (notificationBell && data && typeof data.notificacoes !== 'undefined') {
            notificationBell.textContent = data.notificacoes;
        }
    })
    .catch(error => {
        console.error('Erro ao buscar notificações:', error);
    });