import ast
from dotenv import load_dotenv
from pathlib import Path
import os
from time import sleep
import gradio as gr
from src.chat_module import ESGAIChat

esgaichat = ESGAIChat()
load_dotenv()


def button_anaimate():
    sleep(1)

def disable_btn():
    return gr.Button.update(interactive=False)

def enable_btn():
    return gr.Button.update(interactive=True)

def deselect_radio():
    return gr.Radio.update(value=None)

def reset_chatbot():
    return [["", "我是 ESG AI Chat\n有什麼能為您服務的嗎？"]]

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

def bot(chat_type, history):
    response = esgaichat.chat(query=history[-1][0], chain_category=chat_type)
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        yield history



css = """
#center {text-align: center}
footer {visibility: hidden}
a {color: rgb(255, 206, 10) !important}
"""
with gr.Blocks(css=css) as demo:

    gr.Markdown("# ESG AI Chat Test UI", elem_id="center")
    gr.Markdown("Made by `ESGToday`", elem_id="center")

    with gr.Tab("Chat"):
        with gr.Row():
            with gr.Column():
                chat_type = gr.Dropdown(
                    label="Chat Type",
                    choices=["qa", "summarize"],
                    value="qa",
                    scale=2,
                )
                chatbot = gr.Chatbot(
                    [(None, "我是 ESG AI Chat\n有什麼能為您服務的嗎？")],
                    elem_id="chatbot",
                    scale=1,
                    height=700,
                    bubble_full_width=False
                )
                with gr.Row():
                    chatbot_input = gr.Textbox(
                        scale=4,
                        show_label=False,
                        placeholder="Enter text and press enter, or upload an image",
                        container=False,
                    )
                    chat_btn = gr.Button("💬")

    with gr.Tab("Prompt Templates"):
        with gr.Row():
            with gr.Column():
                prompt_category = gr.Dropdown(
                    label="Prompt Category",
                    choices=["qa", "summarize"],
                    value="qa",
                    scale=2,
                )
                prompt_template = gr.Textbox(
                    label="Prompt Template",
                    placeholder="Enter prompt template",
                    scale=4,
                )
                prompt_btn = gr.Button("Update Prompt")

    chatbot_input.submit(
        add_text, [chatbot, chatbot_input], [chatbot, chatbot_input], queue=False
    ).then(
        bot, [chat_type, chatbot], chatbot, api_name="bot_response"
    ).then(
        lambda: gr.Textbox(interactive=True), None, [chatbot_input], queue=False
    )
    chat_btn.click(
        add_text, [chatbot, chatbot_input], [chatbot, chatbot_input], queue=False
    ).then(
        bot, [chat_type, chatbot], chatbot, api_name="bot_response"
    ).then(
        lambda: gr.Textbox(interactive=True), None, [chatbot_input], queue=False
    )
    chatbot.like(print_like_dislike, None, None)


if __name__ == "__main__":
    demo.queue().launch(
        server_name=os.environ.get("FRONTEND_HOST"),
        server_port=int(os.environ.get("FRONTEND_PORT")),
    )
