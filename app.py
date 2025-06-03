from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuração do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Contexto do cardápio para a IA
CARDAPIO_CONTEXT = """
Você é o atendente virtual da Burger Mania, uma hamburgueria premium. 
Aqui está o cardápio completo:

HAMBÚRGUERES:
- Clássico Mania: Pão brioche, hambúrguer 180g, queijo cheddar, alface, tomate, cebola roxa, maionese especial - R$28
- Burger Duplo Sabor: 2 hambúrgueres 120g, queijo prato duplo, bacon, molho barbecue - R$35
- Veggie Delícia: Hambúrguer de grão de bico, mussarela, rúcula, tomate seco - R$30
- Frango Crocante: Filé de frango empanado, provolone, alface, honey mustard - R$29
- Picanha Supreme: Picanha 200g, queijo coalho, cebola caramelizada - R$42
- Mega Bacon Blast: Bacon em tiras, queijo prato, picles, maionese de alho - R$38
- Chef's Especial: Blend de carnes, gorgonzola, pera caramelizada - R$40
- Kids Burger: Mini hambúrguer 80g, cheddar, batata frita - R$20
- Monte Seu Burger: Base + ingredientes à escolha - R$25 (base)

ACOMPANHAMENTOS:
- Batata Frita Tradicional - R$12
- Batata com Cheddar e Bacon - R$18
- Anéis de Cebola - R$15

BEBIDAS:
- Refrigerantes (lata) - R$7
- Água mineral - R$5
- Sucos naturais - R$10

Sempre responda de forma amigável e informal, como um jovem atendente de hamburgueria. 
Se perguntarem sobre ingredientes ou preparo, seja detalhista. 
Para pedidos, confirme item por item.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        response = model.generate_content(CARDAPIO_CONTEXT + "Mensagem do Usuário: "+ user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)