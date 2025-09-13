from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database

app = Flask(__name__)
# Troque essa chave por algo secreto quando for subir em produção / repo público
app.secret_key = "troque_essa_chave_para_uma_aleatoria"

db = Database()

@app.route("/")
def index():
    filtro = request.args.get("filtro", "todos")  # 'todos' | 'ativos' | 'inativos'
    restaurantes = db.obter_restaurantes()
    if filtro == "ativos":
        restaurantes = [r for r in restaurantes if r["ativo"] == 1]
    elif filtro == "inativos":
        restaurantes = [r for r in restaurantes if r["ativo"] == 0]
    return render_template("index.html", restaurantes=restaurantes, filtro=filtro)

@app.route("/add", methods=["POST"])
def add_restaurante():
    nome = request.form.get("nome", "").strip()
    categoria = request.form.get("categoria", "").strip()
    if not nome or not categoria:
        flash("Nome e categoria são obrigatórios.", "danger")
        return redirect(url_for("index"))
    db.cadastrar_restaurante(nome, categoria)
    flash(f"Restaurante '{nome}' cadastrado com sucesso.", "success")
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_restaurante(id):
    restaurante = db.obter_por_id(id)
    if not restaurante:
        flash("Restaurante não encontrado.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        categoria = request.form.get("categoria", "").strip()
        if not nome or not categoria:
            flash("Nome e categoria são obrigatórios.", "danger")
            return redirect(url_for("edit_restaurante", id=id))
        db.atualizar_restaurante(id, nome, categoria)
        flash("Restaurante atualizado com sucesso.", "success")
        return redirect(url_for("index"))

    return render_template("editar.html", r=restaurante)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_restaurante(id):
    r = db.obter_por_id(id)
    if r:
        db.excluir_restaurante(id)
        flash("Restaurante excluído.", "success")
    else:
        flash("Registro não encontrado.", "danger")
    return redirect(url_for("index"))

@app.route("/toggle/<int:id>", methods=["POST"])
def toggle_restaurante(id):
    r = db.obter_por_id(id)
    if not r:
        flash("Registro não encontrado.", "danger")
    else:
        novo_estado = 0 if r["ativo"] == 1 else 1
        db.alterar_estado(id, novo_estado == 1)
        flash("Estado alterado com sucesso.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
