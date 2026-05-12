-- Script de criação do banco de dados para o Sistema de Notas de Alunos
-- Disciplina: Desenvolvimento Rápido de Aplicações em Python

CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    nota1 REAL DEFAULT 0,
    nota2 REAL DEFAULT 0,
    nota3 REAL DEFAULT 0,
    nota4 REAL DEFAULT 0,
    media REAL DEFAULT 0
);