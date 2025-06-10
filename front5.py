import gradio as gr
import json
from AI1 import AI1
from AI2 import AI2
from AI3 import AI3

identifier = AI1()
patitor = AI2()
addresser = AI3()

def loads_preserve_backslashes_v2(raw_json: str):
    # 把每个 '\' 先替换成 '\\'
    print(raw_json)
    tmp = raw_json.replace('\\', '\\\\')
    print(tmp)
    return tmp

def process_all(question_file, question_text, answer_file, answer_text, question_mode, answer_mode):
    """处理所有输入并生成解答（如果需要）"""

    if question_mode == "upload":
        question_content = identifier.identify_from_input(question_file)
    elif question_mode == "direct_input":
        question_content = identifier.polish_text(question_text)
    else:
        raise ValueError("Unsupported question mode. Please select 'upload' or 'direct_input'.")
    identifier.set_question(question_content)
    # print(f"Processed question: {identifier.question}")
    
    if answer_mode == "upload":
        answer_content = identifier.identify_from_input(answer_file)
        identifier.set_solution(answer_content)
    elif answer_mode == "direct_input":
        answer_text = identifier.polish_text(answer_text)
        identifier.set_solution(answer_text)
    elif answer_mode == "direct_generate":
        identifier.direct_generate()
    elif answer_mode == "search_and_generate":
        identifier.search_from_internet()

    # print(f"Processed answer: {identifier.solution}")

    return identifier.question, identifier.solution

def toggle_input_visibility(mode):
    """根据模式切换输入控件的可见性"""
    return [
        {"visible": mode == "upload", "__type__": "update"},
        {"visible": mode == "direct_input", "__type__": "update"}
    ]

def partition_points(question: str, answer: str) -> str:
    if not question or not answer:
        return '{"points": []}'
    return loads_preserve_backslashes_v2(patitor.partitioning_points(question, answer))



def toggle_preview(content, current_visibility):
    """切换预览显示状态"""
    if current_visibility:
        return None, False
    else:
        return content, True

with gr.Blocks(title="双文档分析系统") as app:
    # === 状态存储 ===
    question_state = gr.State()
    answer_state = gr.State()
    keypoints_state = gr.State()
    question_preview_visible = gr.State(False)
    answer_preview_visible = gr.State(False)
    keypoints_preview_visible = gr.State(False)
    
    # === 上传区 ===
        # === 上传区 ===
    with gr.Row():
        with gr.Column(variant="panel"):
            gr.Markdown("### 1. 问题输入")
            question_mode_radio = gr.Radio(
                choices=[
                    ("上传解答文件", "upload"),
                    ("直接输入文本", "direct_input"),
                ],
                label="选择问题模式",
                value="upload"
            )
            question_upload = gr.File(
                file_types=[".pdf", ".png", ".txt", ".md", ".jpg", ".jpeg"],
                label="拖放问题文件",
                height=50,
                visible=True
            )
            question_text = gr.Textbox(
                label="输入问题文本",
                lines=5,
                placeholder="在此输入问题内容...",
                interactive=True,
                visible=False
            )
            question_preview_btn = gr.Button("预览问题内容", visible=False)
            question_preview = gr.Textbox(label="问题内容预览", lines=5, interactive=False, visible=False)

        with gr.Column(variant="panel"):
            gr.Markdown("### 2. 解答选项")
            answer_mode_radio = gr.Radio(
                choices=[
                    ("上传解答文件", "upload"),
                    ("直接输入文本", "direct_input"),
                    ("自动生成解答", "direct_generate"),
                    ("联网搜索并生成", "search_and_generate")
                ],
                label="选择解答模式",
                value="upload"
            )
            answer_upload = gr.File(
                file_types=[".pdf", ".png", ".txt", ".md", ".jpg", ".jpeg"],
                label="拖放解答文件",
                height=50,
                visible=True
            )
            answer_text = gr.Textbox(
                label="输入解答文本",
                lines=5,
                placeholder="在此输入解答内容...",
                interactive=True,
                visible=False
            )
            answer_preview_btn = gr.Button("预览解答内容", visible=False)
            answer_preview = gr.Textbox(label="解答内容预览", lines=5, interactive=False, visible=False)

    with gr.Row():
        # === 分析按钮 ===
        process_btn = gr.Button("处理内容", variant="primary")
        
        # === 分解要点按钮 ===
        partition_btn = gr.Button("分解要点", visible=False, variant="primary")
        keypoints_preview_btn = gr.Button("预览要点分解结果", visible=False)
        keypoints_preview = gr.JSON(label="要点分解结果", visible=False)

    # === 模式切换事件 ===

    question_mode_radio.change(
        fn=toggle_input_visibility,
        inputs=question_mode_radio,
        outputs=[question_upload, question_text]
    )

    answer_mode_radio.change(
        fn=toggle_input_visibility,
        inputs=answer_mode_radio,
        outputs=[answer_upload, answer_text]
    )
    
    # === 文件处理事件 ===
    process_btn.click(
        fn=lambda: gr.Button(value="处理中...", interactive=False),
        outputs=process_btn
    ).then(
        fn=process_all,
        inputs=[question_upload, question_text, answer_upload, answer_text, question_mode_radio, answer_mode_radio],
        outputs=[question_state, answer_state]
    ).then(
        fn=lambda: [gr.Button(visible=True), gr.Button(visible=True), gr.Button(visible=True)],
        outputs=[question_preview_btn, answer_preview_btn, partition_btn]
    ).then(
        fn=lambda: gr.Button(value="处理内容", interactive=True),
        outputs=process_btn
    )
    
    # === 预览事件 ===
    question_preview_btn.click(
        fn=toggle_preview,
        inputs=[question_state, question_preview_visible],
        outputs=[question_preview, question_preview_visible]
    ).then(
        fn=lambda visible: gr.Textbox(visible=visible),
        inputs=question_preview_visible,
        outputs=question_preview
    )
    
    answer_preview_btn.click(
        fn=toggle_preview,
        inputs=[answer_state, answer_preview_visible],
        outputs=[answer_preview, answer_preview_visible]
    ).then(
        fn=lambda visible: gr.Textbox(visible=visible),
        inputs=answer_preview_visible,
        outputs=answer_preview
    )

    # === 分解要点事件 ===
    partition_btn.click(
        fn=lambda: gr.Button(value="分解中...", interactive=False, variant="primary"),
        outputs=partition_btn
    ).then(
        fn=partition_points,
        inputs=[question_state, answer_state],
        outputs=[keypoints_state]
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=[keypoints_preview_btn]
    ).then(
        fn=lambda: gr.Button(value="分解要点", interactive=True, variant="primary"),
        outputs=partition_btn
    )
    
    # === 要点预览事件 ===
    keypoints_preview_btn.click(
        fn=toggle_preview,
        inputs=[keypoints_state, keypoints_preview_visible],
        outputs=[keypoints_preview, keypoints_preview_visible]
    ).then(
        fn=lambda vis:gr.update(visible=vis),
        inputs=keypoints_preview_visible,
        outputs=keypoints_preview
    )

app.launch()
