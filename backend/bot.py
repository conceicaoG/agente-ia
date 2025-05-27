import cohere
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# Inicialize o cliente Cohere
co = cohere.Client("E0mHO1ZXzYYozABc4G1hdKu5JO1KKyZBeCCexco1")  # substitua pela sua chave

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou um bot com IA da Cohere. Pode falar comigo!")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    # Envia a mensagem do usuário para a IA da Cohere
    resposta = co.chat(
        message=texto,
        model="command-r-plus"
    )

    # Responde com o texto gerado
    await update.message.reply_text(resposta.text)

def main():
    application = ApplicationBuilder().token("7728004955:AAGRd7wHLCBjjDKMusfttNU8VJUHf2ywSYE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    application.run_polling()

if __name__ == "__main__":
    main()
