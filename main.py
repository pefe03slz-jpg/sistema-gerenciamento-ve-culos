import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkfont
import json
import os

# Arquivo para salvar os dados
DATA_FILE = "carros_data.json"
VENDEDORES_FILE = "vendedores_data.json"

class SistemaCarros:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Carros")
        self.root.geometry("1200x600")
        self.root.configure(bg='black')
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores: preto e amarelo
        self.style.configure('Yellow.TButton', background='yellow', foreground='black', 
                           font=('Arial', 10, 'bold'))
        self.style.map('Yellow.TButton', background=[('active', '#ffcc00')])
        
        self.style.configure('Yellow.Treeview', background='black', foreground='yellow',
                           fieldbackground='black', font=('Arial', 10))
        self.style.configure('Yellow.Treeview.Heading', background='yellow', 
                           foreground='black', font=('Arial', 10, 'bold'))
        
        # Carregar dados
        self.carregar_dados()
        self.carregar_vendedores()
        
        # Criar interface
        self.criar_menu_superior()
        self.criar_tabela()
        self.criar_barra_pesquisa()
        self.criar_botoes_inferiores()
        
        # Atualizar tabela
        self.atualizar_tabela()
    
    def carregar_dados(self):
        """Carregar dados dos carros do arquivo"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.carros = json.load(f)
            except:
                self.carros = []
        else:
            # Dados de exemplo
            self.carros = [
                {
                    'placa': 'ABC1234',
                    'modelo': 'Fiat Uno',
                    'cliente': 'João Silva',
                    'vendedor': 'Carlos Santos',
                    'status': 'em serviço',
                    'descricao': 'Troca de óleo e filtros'
                },
                {
                    'placa': 'DEF5678',
                    'modelo': 'VW Gol',
                    'cliente': 'Maria Oliveira',
                    'vendedor': 'Ana Costa',
                    'status': 'aguardando',
                    'descricao': 'Aguardando peças'
                },
                {
                    'placa': 'GHI9012',
                    'modelo': 'Chevrolet Onix',
                    'cliente': 'Pedro Souza',
                    'vendedor': 'Carlos Santos',
                    'status': 'finalizado',
                    'descricao': 'Revisão completa'
                }
            ]
    
    def carregar_vendedores(self):
        """Carregar lista de vendedores"""
        if os.path.exists(VENDEDORES_FILE):
            try:
                with open(VENDEDORES_FILE, 'r', encoding='utf-8') as f:
                    self.vendedores = json.load(f)
            except:
                self.vendedores = ['Carlos Santos', 'Ana Costa', 'Roberto Lima']
        else:
            self.vendedores = ['Carlos Santos', 'Ana Costa', 'Roberto Lima']
    
    def salvar_dados(self):
        """Salvar dados dos carros"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.carros, f, ensure_ascii=False, indent=2)
    
    def salvar_vendedores(self):
        """Salvar lista de vendedores"""
        with open(VENDEDORES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.vendedores, f, ensure_ascii=False, indent=2)
    
    def criar_menu_superior(self):
        """Criar menu superior com opções de vendedores"""
        menu_frame = tk.Frame(self.root, bg='black', height=40)
        menu_frame.pack(fill='x', padx=10, pady=5)
        
        # Botão de opções (canto superior esquerdo)
        self.btn_opcoes = tk.Button(menu_frame, text="⚙️ Opções", bg='yellow', fg='black',
                                   font=('Arial', 10, 'bold'), command=self.abrir_gestao_vendedores)
        self.btn_opcoes.pack(side='left', padx=5)
        
        # Título centralizado
        titulo = tk.Label(menu_frame, text="Sistema de Gerenciamento de Carros", 
                         bg='black', fg='yellow', font=('Arial', 14, 'bold'))
        titulo.pack(side='left', expand=True)
    
    def criar_tabela(self):
        """Criar tabela para exibir os carros"""
        # Frame para a tabela
        tabela_frame = tk.Frame(self.root, bg='black')
        tabela_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Criar Treeview
        colunas = ('placa', 'modelo', 'cliente', 'vendedor', 'status', 'descricao')
        self.tree = ttk.Treeview(tabela_frame, columns=colunas, show='headings', 
                                style='Yellow.Treeview', height=20)
        
        # Configurar cabeçalhos
        self.tree.heading('placa', text='Placa')
        self.tree.heading('modelo', text='Modelo')
        self.tree.heading('cliente', text='Cliente/Empresa')
        self.tree.heading('vendedor', text='Vendedor')
        self.tree.heading('status', text='Status')
        self.tree.heading('descricao', text='Descrição')
        
        # Configurar largura das colunas
        self.tree.column('placa', width=100)
        self.tree.column('modelo', width=150)
        self.tree.column('cliente', width=200)
        self.tree.column('vendedor', width=150)
        self.tree.column('status', width=100)
        self.tree.column('descricao', width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabela_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind de clique
        self.tree.bind('<ButtonRelease-1>', self.ao_clicar_carro)
        
        # Pack elementos
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def criar_barra_pesquisa(self):
        """Criar barra de pesquisa no canto superior direito"""
        pesquisa_frame = tk.Frame(self.root, bg='black')
        pesquisa_frame.pack(fill='x', padx=10, pady=5)
        
        # Label de pesquisa
        lbl_pesquisa = tk.Label(pesquisa_frame, text="🔍 Pesquisar:", 
                               bg='black', fg='yellow', font=('Arial', 10))
        lbl_pesquisa.pack(side='right', padx=5)
        
        # Campo de pesquisa
        self.pesquisa_entry = tk.Entry(pesquisa_frame, bg='yellow', fg='black', 
                                       font=('Arial', 10), width=30)
        self.pesquisa_entry.pack(side='right', padx=5)
        self.pesquisa_entry.bind('<KeyRelease>', self.filtrar_carros)
    
    def criar_botoes_inferiores(self):
        """Criar botões na parte inferior"""
        botoes_frame = tk.Frame(self.root, bg='black')
        botoes_frame.pack(fill='x', padx=10, pady=10)
        
        # Botão de adicionar (+)
        btn_adicionar = tk.Button(botoes_frame, text="+ Adicionar Carro", 
                                 bg='yellow', fg='black', font=('Arial', 10, 'bold'),
                                 command=self.adicionar_carro)
        btn_adicionar.pack(side='left', padx=5)
        
        # Botão de remover finalizados
        btn_remover = tk.Button(botoes_frame, text="🗑️ Remover Finalizados", 
                               bg='yellow', fg='black', font=('Arial', 10, 'bold'),
                               command=self.remover_finalizados)
        btn_remover.pack(side='left', padx=5)
    
    def atualizar_tabela(self, carros_filtrados=None):
        """Atualizar a tabela com os dados atuais"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Usar carros filtrados ou todos os carros
        dados = carros_filtrados if carros_filtrados is not None else self.carros
        
        # Adicionar dados à tabela
        for carro in dados:
            self.tree.insert('', 'end', values=(
                carro['placa'],
                carro['modelo'],
                carro['cliente'],
                carro['vendedor'],
                carro['status'],
                carro['descricao']
            ))
    
    def filtrar_carros(self, event=None):
        """Filtrar carros baseado na pesquisa"""
        termo = self.pesquisa_entry.get().lower()
        
        if not termo:
            self.atualizar_tabela()
            return
        
        carros_filtrados = []
        for carro in self.carros:
            if (termo in carro['placa'].lower() or 
                termo in carro['vendedor'].lower() or 
                termo in carro['status'].lower()):
                carros_filtrados.append(carro)
        
        self.atualizar_tabela(carros_filtrados)
    
    def ao_clicar_carro(self, event):
        """Ação ao clicar em um carro"""
        selecao = self.tree.selection()
        if not selecao:
            return
        
        # Obter dados do carro selecionado
        item = self.tree.item(selecao[0])
        placa = item['values'][0]
        
        # Encontrar o carro no array
        carro = None
        for c in self.carros:
            if c['placa'] == placa:
                carro = c
                break
        
        if carro:
            self.abrir_edicao_carro(carro)
    
    def abrir_edicao_carro(self, carro):
        """Abrir janela para editar status, descrição e vendedor"""
        edicao_win = tk.Toplevel(self.root)
        edicao_win.title(f"Editar Carro - {carro['placa']}")
        edicao_win.geometry("500x400")
        edicao_win.configure(bg='black')
        
        # Título
        titulo = tk.Label(edicao_win, text=f"Editar Carro: {carro['placa']} - {carro['modelo']}",
                         bg='black', fg='yellow', font=('Arial', 12, 'bold'))
        titulo.pack(pady=10)
        
        # Status
        tk.Label(edicao_win, text="Status:", bg='black', fg='yellow', 
                font=('Arial', 10)).pack(pady=5)
        status_var = tk.StringVar(value=carro['status'])
        status_combo = ttk.Combobox(edicao_win, textvariable=status_var, 
                                    values=['em serviço', 'aguardando', 'finalizado'],
                                    state='readonly', width=30)
        status_combo.pack(pady=5)
        
        # Vendedor
        tk.Label(edicao_win, text="Vendedor:", bg='black', fg='yellow', 
                font=('Arial', 10)).pack(pady=5)
        vendedor_var = tk.StringVar(value=carro['vendedor'])
        vendedor_combo = ttk.Combobox(edicao_win, textvariable=vendedor_var, 
                                      values=self.vendedores, state='readonly', width=30)
        vendedor_combo.pack(pady=5)
        
        # Descrição
        tk.Label(edicao_win, text="Descrição:", bg='black', fg='yellow', 
                font=('Arial', 10)).pack(pady=5)
        descricao_text = tk.Text(edicao_win, height=5, width=40, bg='yellow', fg='black')
        descricao_text.insert('1.0', carro['descricao'])
        descricao_text.pack(pady=5)
        
        # Botões
        btn_frame = tk.Frame(edicao_win, bg='black')
        btn_frame.pack(pady=20)
        
        def salvar():
            carro['status'] = status_var.get()
            carro['vendedor'] = vendedor_var.get()
            carro['descricao'] = descricao_text.get('1.0', 'end-1c')
            self.salvar_dados()
            self.atualizar_tabela()
            self.filtrar_carros()  # Reaplicar filtro
            edicao_win.destroy()
            messagebox.showinfo("Sucesso", "Carro atualizado com sucesso!")
        
        tk.Button(btn_frame, text="Salvar", command=salvar, 
                 bg='yellow', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Cancelar", command=edicao_win.destroy, 
                 bg='yellow', fg='black', font=('Arial', 10)).pack(side='left', padx=10)
    
    def abrir_gestao_vendedores(self):
        """Abrir janela para gerenciar vendedores"""
        gestao_win = tk.Toplevel(self.root)
        gestao_win.title("Gerenciar Vendedores")
        gestao_win.geometry("400x500")
        gestao_win.configure(bg='black')
        
        # Título
        tk.Label(gestao_win, text="Gerenciar Vendedores", 
                bg='black', fg='yellow', font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Lista de vendedores
        lista_frame = tk.Frame(gestao_win, bg='black')
        lista_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        lista_vendedores = tk.Listbox(lista_frame, bg='yellow', fg='black', 
                                      font=('Arial', 10), height=15)
        lista_vendedores.pack(fill='both', expand=True)
        
        # Carregar vendedores na lista
        for vendedor in self.vendedores:
            lista_vendedores.insert('end', vendedor)
        
        # Frame para botões de adicionar/remover
        btn_frame = tk.Frame(gestao_win, bg='black')
        btn_frame.pack(pady=10)
        
        def adicionar_vendedor():
            novo_vendedor = simpledialog.askstring("Adicionar Vendedor", 
                                                   "Digite o nome do novo vendedor:")
            if novo_vendedor and novo_vendedor.strip():
                novo_vendedor = novo_vendedor.strip()
                if novo_vendedor not in self.vendedores:
                    self.vendedores.append(novo_vendedor)
                    self.salvar_vendedores()
                    lista_vendedores.insert('end', novo_vendedor)
                    messagebox.showinfo("Sucesso", "Vendedor adicionado com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Vendedor já existe!")
        
        def remover_vendedor():
            selecao = lista_vendedores.curselection()
            if selecao:
                vendedor = lista_vendedores.get(selecao[0])
                if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover {vendedor}?"):
                    self.vendedores.remove(vendedor)
                    self.salvar_vendedores()
                    lista_vendedores.delete(selecao[0])
                    messagebox.showinfo("Sucesso", "Vendedor removido com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Selecione um vendedor para remover!")
        
        tk.Button(btn_frame, text="+ Adicionar", command=adicionar_vendedor,
                 bg='yellow', fg='black', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="- Remover", command=remover_vendedor,
                 bg='yellow', fg='black', font=('Arial', 10)).pack(side='left', padx=5)
    
    def adicionar_carro(self):
        """Adicionar novo carro"""
        add_win = tk.Toplevel(self.root)
        add_win.title("Adicionar Novo Carro")
        add_win.geometry("500x500")
        add_win.configure(bg='black')
        
        # Título
        tk.Label(add_win, text="Adicionar Novo Carro", 
                bg='black', fg='yellow', font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Campos
        campos = {}
        campos_frame = tk.Frame(add_win, bg='black')
        campos_frame.pack(pady=10)
        
        labels = ['Placa:', 'Modelo:', 'Cliente/Empresa:', 'Vendedor:', 'Status:', 'Descrição:']
        entries = {}
        
        for i, label in enumerate(labels):
            tk.Label(campos_frame, text=label, bg='black', fg='yellow', 
                    font=('Arial', 10)).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            
            if label == 'Vendedor:':
                entry = ttk.Combobox(campos_frame, values=self.vendedores, width=30)
                entry.grid(row=i, column=1, padx=5, pady=5)
            elif label == 'Status:':
                entry = ttk.Combobox(campos_frame, values=['em serviço', 'aguardando', 'finalizado'],
                                    width=30, state='readonly')
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.set('aguardando')
            elif label == 'Descrição:':
                entry = tk.Text(campos_frame, height=4, width=30, bg='yellow', fg='black')
                entry.grid(row=i, column=1, padx=5, pady=5)
            else:
                entry = tk.Entry(campos_frame, bg='yellow', fg='black', width=30)
                entry.grid(row=i, column=1, padx=5, pady=5)
            
            entries[label] = entry
        
        def salvar_novo():
            # Validar campos obrigatórios
            placa = entries['Placa:'].get().strip().upper()
            modelo = entries['Modelo:'].get().strip()
            cliente = entries['Cliente/Empresa:'].get().strip()
            vendedor = entries['Vendedor:'].get()
            status = entries['Status:'].get()
            descricao = entries['Descrição:'].get('1.0', 'end-1c').strip()
            
            if not all([placa, modelo, cliente, vendedor, status]):
                messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
                return
            
            # Verificar se placa já existe
            for carro in self.carros:
                if carro['placa'] == placa:
                    messagebox.showwarning("Aviso", "Placa já cadastrada!")
                    return
            
            # Adicionar novo carro
            novo_carro = {
                'placa': placa,
                'modelo': modelo,
                'cliente': cliente,
                'vendedor': vendedor,
                'status': status,
                'descricao': descricao
            }
            
            self.carros.append(novo_carro)
            self.salvar_dados()
            self.atualizar_tabela()
            add_win.destroy()
            messagebox.showinfo("Sucesso", "Carro adicionado com sucesso!")
        
        # Botões
        btn_frame = tk.Frame(add_win, bg='black')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Salvar", command=salvar_novo,
                 bg='yellow', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Cancelar", command=add_win.destroy,
                 bg='yellow', fg='black', font=('Arial', 10)).pack(side='left', padx=10)
    
    def remover_finalizados(self):
        """Remover todos os carros com status finalizado"""
        if not self.carros:
            messagebox.showinfo("Info", "Não há carros cadastrados!")
            return
        
        finalizados = [c for c in self.carros if c['status'] == 'finalizado']
        
        if not finalizados:
            messagebox.showinfo("Info", "Não há carros finalizados para remover!")
            return
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover {len(finalizados)} carro(s) finalizado(s)?"):
            self.carros = [c for c in self.carros if c['status'] != 'finalizado']
            self.salvar_dados()
            self.atualizar_tabela()
            self.filtrar_carros()
            messagebox.showinfo("Sucesso", f"{len(finalizados)} carro(s) removido(s) com sucesso!")

def main():
    root = tk.Tk()
    app = SistemaCarros(root)
    root.mainloop()

if __name__ == "__main__":
    main()