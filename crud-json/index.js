const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json()); // Permite receber JSON no body das requisições

let items = []; // Banco de dados temporário de itens
let users = []; // Banco de dados temporário de usuários

// Rota de teste
app.get("/", (req, res) => {
    res.send("API funcionando!");
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});

// =================== CRUD DE ITENS ===================

// Listar todos os itens (GET)
app.get("/items", (req, res) => {
    res.json(items);
});

// Adicionar um novo item (POST)
app.post("/items", (req, res) => {
    const { name } = req.body;
    if (!name) {
        return res.status(400).json({ error: "Nome é obrigatório" });
    }

    const newItem = { id: items.length + 1, name };
    items.push(newItem);
    res.status(201).json(newItem);
});

// Atualizar um item pelo ID (PUT)
app.put("/items/:id", (req, res) => {
    const { id } = req.params;
    const { name } = req.body;

    const item = items.find((i) => i.id == id);
    if (!item) {
        return res.status(404).json({ error: "Item não encontrado" });
    }

    item.name = name || item.name;
    res.json(item);
});

// Deletar um item pelo ID (DELETE)
app.delete("/items/:id", (req, res) => {
    const { id } = req.params;
    items = items.filter((i) => i.id != id);
    res.json({ message: "Item removido com sucesso" });
});

// =================== AUTENTICAÇÃO ===================

// Rota para listar todos os usuários cadastrados (GET)
app.get("/users", (req, res) => {
    res.json(users);
});

// Rota de cadastro de usuário (POST)
app.post("/register", (req, res) => {
    const { name, matricula, senha } = req.body;

    if (!name || !matricula || !senha) {
        return res.status(400).json({ error: "Todos os campos são obrigatórios!" });
    }

    // Verificar se já existe um usuário com essa matrícula
    const userExists = users.find(user => user.matricula === matricula);
    if (userExists) {
        return res.status(400).json({ error: "Matrícula já cadastrada!" });
    }

    // Criar usuário e salvar no array
    const newUser = { id: users.length + 1, name, matricula, senha };
    users.push(newUser);

    res.status(201).json({ message: "Usuário cadastrado com sucesso!" });
});

// Rota de login de usuário (POST)
app.post("/login", (req, res) => {
    const { matricula, senha } = req.body;

    const user = users.find(user => user.matricula === matricula && user.senha === senha);

    if (!user) {
        return res.status(401).json({ error: "Matrícula ou senha incorretos!" });
    }

    res.json({ message: "Login bem-sucedido!", user });
});
