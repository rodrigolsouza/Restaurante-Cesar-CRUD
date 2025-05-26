const apiUrl = "http://127.0.0.1:8000/cardapio";

document.getElementById('form-item').addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('id').value;
    const item = {
        nome: document.getElementById('nome').value,
        descricao: document.getElementById('descricao').value,
        ingredientes: document.getElementById('ingredientes').value,
        preco: parseFloat(document.getElementById('preco').value),
        categoria: document.getElementById('categoria').value,
        foto: document.getElementById('foto').value
    };

    let url = apiUrl;
    let method = 'POST';

    if (id) {
        url += `/${id}`;
        method = 'PUT';
    }

    const response = await fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(item)
    });

    if (response.ok) {
        alert(id ? 'Item atualizado com sucesso!' : 'Item adicionado com sucesso!');
        document.getElementById('form-item').reset();
        document.getElementById('id').value = '';
        carregarCardapio();
    } else {
        alert('Erro ao adicionar/atualizar item.');
    }
});

async function carregarCardapio() {
    const resposta = await fetch(apiUrl);
    const dados = await resposta.json();

    const div = document.getElementById('cardapio');
    div.innerHTML = '';

    dados.forEach((item) => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <img src="${item.foto}" alt="Foto de ${item.nome}">
            <div class="info">
                <h3>${item.nome}</h3>
                <p><strong>Descrição:</strong> ${item.descricao}</p>
                <p><strong>Ingredientes:</strong> ${item.ingredientes}</p>
                <p><strong>Categoria:</strong> ${item.categoria}</p>
                <p class="preco">R$ ${item.preco.toFixed(2)}</p>
                <button class="edit" onclick="editarItem(${item.id})">Editar</button>
                <button class="delete" onclick="excluirItem(${item.id})">Excluir</button>
            </div>
        `;

        div.appendChild(card);
    });
}

async function editarItem(id) {
    const resposta = await fetch(`${apiUrl}`);
    const itens = await resposta.json();
    const item = itens.find(i => i.id === id);

    document.getElementById('id').value = item.id;
    document.getElementById('nome').value = item.nome;
    document.getElementById('descricao').value = item.descricao;
    document.getElementById('ingredientes').value = item.ingredientes;
    document.getElementById('preco').value = item.preco;
    document.getElementById('categoria').value = item.categoria;
    document.getElementById('foto').value = item.foto;
}

async function filtrarPorCategoria() {
    const categoria = document.getElementById('filtroCategoria').value;

    if (!categoria) {
        alert('Selecione uma categoria para filtrar.');
        return;
    }

    const resposta = await fetch(`${apiUrl}/categoria/${categoria}`);
    const dados = await resposta.json();

    const div = document.getElementById('cardapio');
    div.innerHTML = '';

    if (dados.length === 0 || dados.mensagem) {
        div.innerHTML = `<p>Nenhum item encontrado na categoria "${categoria}".</p>`;
        return;
    }

    dados.forEach((item) => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <img src="${item.foto}" alt="Foto de ${item.nome}">
            <div class="info">
                <h3>${item.nome}</h3>
                <p><strong>Descrição:</strong> ${item.descricao}</p>
                <p><strong>Ingredientes:</strong> ${item.ingredientes}</p>
                <p><strong>Categoria:</strong> ${item.categoria}</p>
                <p class="preco">R$ ${item.preco.toFixed(2)}</p>
                <button class="edit" onclick="editarItem(${item.id})">Editar</button>
                <button class="delete" onclick="excluirItem(${item.id})">Excluir</button>
            </div>
        `;

        div.appendChild(card);
    });
}



async function excluirItem(id) {
    const confirmar = confirm('Tem certeza que deseja excluir este item?');

    if (confirmar) {
        const resposta = await fetch(`${apiUrl}/${id}`, {
            method: 'DELETE'
        });

        if (resposta.ok) {
            alert('Item excluído com sucesso!');
            carregarCardapio();
        } else {
            alert('Erro ao excluir item.');
        }
    }
}

carregarCardapio();
