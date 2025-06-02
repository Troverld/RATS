import gradio as gr
from AI1 import AI1
from AI2 import AI2

identifier = AI1()
patitor = AI2()

def process_single_file(file) -> str:
    """统一处理单个文件（带空文件检查）"""
    if file is None:
        return None
    return identifier.identify_from_input(file)

def generate_answer(question_content, mode):
    """根据选择的模式生成解答"""
    if mode == "upload":
        return None  # 需要用户上传文件
    elif mode == "direct_generate":
        return identifier.direct_generate(question_content)
    elif mode == "search_and_generate":
        return identifier.search_from_internet(question_content)
    return None

def process_all(question_file, answer_file, mode):
    """处理所有文件并生成解答（如果需要）"""
    question_content = process_single_file(question_file) if question_file else None
    answer_content = None
    
    if mode != "upload":
        answer_content = generate_answer(question_content, mode)
    elif answer_file:
        answer_content = process_single_file(answer_file)
    
    return question_content, answer_content

def toggle_answer_upload_visibility(mode):
    return {"visible": mode == "upload", "__type__": "update"}

def toggle_question_preview(content, current_visibility):
    """切换问题预览显示状态"""
    if current_visibility:
        return None, False
    else:
        return content, True

def toggle_answer_preview(content, current_visibility):
    """切换解答预览显示状态"""
    if current_visibility:
        return None, False
    else:
        return content, True

with gr.Blocks(title="双文档分析系统") as app:
    # === 状态存储 ===
    question_state = gr.State()
    answer_state = gr.State()
    question_preview_visible = gr.State(False)
    answer_preview_visible = gr.State(False)
    
    # === 上传区 ===
    with gr.Row():
        with gr.Column(variant="panel"):
            gr.Markdown("### 1. 问题文件")
            question_upload = gr.File(
                file_types=[".pdf", ".png", ".txt", ".md"],
                label="拖放问题文件",
                height=50
            )
            question_preview_btn = gr.Button("预览问题文件", visible=False)
            question_preview = gr.Textbox(label="问题文件预览", lines=5, interactive=False, visible=False)

        with gr.Column(variant="panel"):
            gr.Markdown("### 2. 解答选项")
            mode_radio = gr.Radio(
                choices=[
                    ("上传解答文件", "upload"),
                    ("自动生成解答", "direct_generate"),
                    ("联网搜索并生成", "search_and_generate")
                ],
                label="选择解答模式",
                value="upload"
            )
            answer_upload = gr.File(
                file_types=[".pdf", ".png", ".txt", ".md"],
                label="拖放解答文件",
                height=50,
                visible=True
            )
            answer_preview_btn = gr.Button("预览解答内容", visible=False)
            answer_preview = gr.Textbox(label="解答内容预览", lines=5, interactive=False, visible=False)

    # === 分析按钮 ===
    process_btn = gr.Button("处理文件", variant="primary")
    
    # === 模式切换事件 ===
    mode_radio.change(
        fn=toggle_answer_upload_visibility,
        inputs=mode_radio,
        outputs=answer_upload
    )
    
    # === 文件处理事件 ===
    process_btn.click(
        fn=lambda: gr.Button(value="处理中...", interactive=False),
        outputs=process_btn
    ).then(
        fn=process_all,
        inputs=[question_upload, answer_upload, mode_radio],
        outputs=[question_state, answer_state]
    ).then(
        fn=lambda: [gr.Button(visible=True), gr.Button(visible=True)],
        outputs=[question_preview_btn, answer_preview_btn]
    ).then(
        fn=lambda: gr.Button(value="处理文件", interactive=True),
        outputs=process_btn
    )
    
    # === 预览事件 ===
    question_preview_btn.click(
        fn=toggle_question_preview,
        inputs=[question_state, question_preview_visible],
        outputs=[question_preview, question_preview_visible]
    ).then(
        fn=lambda visible: gr.Textbox(visible=visible),
        inputs=question_preview_visible,
        outputs=question_preview
    )
    
    answer_preview_btn.click(
        fn=toggle_answer_preview,
        inputs=[answer_state, answer_preview_visible],
        outputs=[answer_preview, answer_preview_visible]
    ).then(
        fn=lambda visible: gr.Textbox(visible=visible),
        inputs=answer_preview_visible,
        outputs=answer_preview
    )

app.launch()