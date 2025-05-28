document.addEventListener('DOMContentLoaded', function() {
    // Botão que abre o modal
    const openModalBtn = document.getElementById('openModalBtnEP');
    // O modal
    const modal = document.getElementById('ModalEnviaProposta');
    // Botão de fechar (caso exista)
    const closeBtn = modal.querySelector('.close-btn');
    // Select de produtos
    const selectProduto = document.getElementById('anexar_produto');

    // Função para buscar e renderizar produtos
    function carregarProdutos() {
        fetch('/api/produto/')
            .then(response => response.json())
            .then(data => {
                // Limpa o select
                selectProduto.innerHTML = '';
                // Adiciona opção padrão
                const optDefault = document.createElement('option');
                optDefault.value = '';
                optDefault.textContent = 'Selecione um produto';
                selectProduto.appendChild(optDefault);

                // Adiciona opções dos produtos
                if (data.produtos && data.produtos.length > 0) {
                    data.produtos.forEach(produto => {
                        const opt = document.createElement('option');
                        opt.value = produto.id;
                        opt.textContent = produto.titulo;
                        selectProduto.appendChild(opt);
                    });
                } else {
                    const opt = document.createElement('option');
                    opt.value = '';
                    opt.textContent = 'Nenhum produto cadastrado';
                    selectProduto.appendChild(opt);
                }
            });
    }

    // Abrir modal ao clicar no botão
    if (openModalBtn && modal) {
        openModalBtn.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
            carregarProdutos(); // Busca produtos ao abrir o modal
        });
    }

    // Fechar modal ao clicar no botão de fechar
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    // Fechar modal ao clicar fora do conteúdo
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});