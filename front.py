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
    # print(raw_json)
    tmp = raw_json.replace('\\', '\\\\')
    # print(tmp)
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

def partition_points(question: str, answer: str) -> list:
    if not question or not answer:
        return []
    return patitor.partitioning_points(question, answer)


def address_question(question: str, solution: str,points: str,idx: int,prompt: str) -> str:
    """使用addresser处理用户问题"""
    if not isinstance(idx, int) or idx <= 0:
        return "请输入一个正整数(1-indexed)"
    return addresser.address(question,solution,points,idx,prompt)

def toggle_preview(content, current_visibility):
    """切换预览显示状态"""
    if current_visibility:
        return None, False
    else:
        return content, True

def show_sketch(keypoints, idx):
    """显示要点内容"""
    if not keypoints or idx < 1 or idx > len(keypoints):
        return "无效的索引"
    return keypoints[idx-1][0]

def show_origin(keypoints, idx):
    """显示原文内容"""
    if not keypoints or idx < 1 or idx > len(keypoints):
        return "无效的索引"
    return keypoints[idx-1][1]

css = """
.success-btn {
    background: #4CAF50 !important;  /* 绿色 */
    color: white !important;
}
"""

with gr.Blocks(title="RATS：集成式智能提示者", css=css) as app:
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
            gr.Markdown("### 1. 上传感兴趣的问题")
            question_mode_radio = gr.Radio(
                choices=[
                    ("上传问题文件", "upload"),
                    ("直接输入文本", "direct_input"),
                ],
                label="选择问题模式",
                value="upload"
            )
            question_upload = gr.File(
                file_types=[".pdf", ".png", ".txt", ".md", ".jpg", ".jpeg"],
                label="拖入问题文件，或点击选择文件（支持 .pdf, .png, .txt, .md, .jpg, .jpeg）",
                file_count="single",
                height=150,
                visible=True
            )
            question_text = gr.Textbox(
                label="输入问题文本",
                lines=5,
                placeholder="在此输入问题内容...",
                interactive=True,
                visible=False
            )
            question_preview_btn = gr.Button("预览问题（仅供参考）", visible=False)
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
                height=150,
                visible=True
            )
            answer_text = gr.Textbox(
                label="输入解答文本",
                lines=5,
                placeholder="在此输入解答内容...",
                interactive=True,
                visible=False
            )
            answer_preview_btn = gr.Button("预览解答（仅供参考）", visible=False)
            answer_preview = gr.Textbox(label="解答内容预览", lines=5, interactive=False, visible=False)

    with gr.Column():
        with gr.Row():
            process_btn = gr.Button("处理内容", variant="primary")
            partition_btn = gr.Button("分解要点", visible=False, variant="primary")
        with gr.Row():
            keypoints_preview_btn = gr.Button("预览分解（仅供参考）", visible=False)
            keypoints_preview = gr.JSON(label="要点分解结果", visible=False)

    # === Addresser 功能区 ===
    with gr.Row(variant="panel"):
        with gr.Column():
            gr.Markdown("### 3. 问题处理")
            with gr.Row():
                address_number = gr.Dropdown(
                    label="输入你关心的选项",
                    choices = [0,1,6,4],
                    interactive=True,
                    visible=False
                )
                address_sketch_btn = gr.Button("查看要点", variant="primary", visible=False)
                address_origin_btn = gr.Button("查看原文", variant="primary", visible=False)
                address_question_btn = gr.Button("提出问题", variant="primary", visible=False)
                question_submit_btn = gr.Button("确认提问", variant="primary", visible=False)
            address_question_input = gr.Textbox(
                    label="输入您的问题",
                    lines=3,
                    placeholder="在此输入您的问题...",
                    interactive=True,
                    visible=False
                )
            address_output = gr.Textbox(
                label="处理结果",
                lines=5,
                interactive=False,
                visible=False
            )
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
        fn=lambda: gr.Button(value="已处理√ 点击再次处理", interactive=True, elem_classes="success-btn"),
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
        fn=lambda: gr.Button(value="分解中...（较慢，请耐心等待）", interactive=False, variant="primary"),
        outputs=partition_btn
    ).then(
        fn=partition_points,
        inputs=[question_state, answer_state],
        outputs=[keypoints_state]
    ).then(
        fn=lambda keypoints: gr.update(choices=range(1,len(keypoints)+1)),
        inputs=keypoints_state,
        outputs=address_number
    ).then(
        fn=lambda: [gr.update(visible=True),gr.update(visible=True),gr.update(visible=True),gr.update(visible=True),gr.update(visible=True)],
        outputs=[keypoints_preview_btn,address_number,address_sketch_btn,address_origin_btn,address_question_btn]
    ).then(
        fn=lambda: gr.Button(value="已分解√ 点击重新分解", interactive=True, elem_classes="success-btn"),
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
    
    # === Addresser 处理事件 ===
    address_sketch_btn.click(
        fn=lambda: gr.Button(value="处理中...", interactive=False),
        outputs=address_sketch_btn
    ).then(
        fn=lambda: [gr.update(visible=False), gr.update(visible=True), gr.update(visible=False) , gr.update(visible=True)],
        outputs=[address_question_input, address_question_btn, question_submit_btn,address_output]
    ).then(
        fn=show_sketch,
        inputs=[keypoints_state, address_number],
        outputs=address_output
    ).then(
        fn=lambda: gr.Button(value="查看要点", interactive=True),
        outputs=address_sketch_btn
    )

    address_origin_btn.click(
        fn=lambda: gr.Button(value="处理中...", interactive=False),
        outputs=address_origin_btn
    ).then(
        fn=lambda: [gr.update(visible=False), gr.update(visible=True), gr.update(visible=False) , gr.update(visible=True)],
        outputs=[address_question_input, address_question_btn, question_submit_btn,address_output]
    ).then(
        fn=show_origin,
        inputs=[keypoints_state, address_number],
        outputs=address_output
    ).then(
        fn=lambda: gr.Button(value="查看原文", interactive=True),
        outputs=address_origin_btn
    )

    address_question_btn.click(
        fn=lambda: [gr.update(visible=True),gr.update(visible=False),gr.update(visible=True)],
        outputs=[address_question_input, address_question_btn, question_submit_btn]
    )

    question_submit_btn.click(
        fn=lambda: gr.Button(value="处理中...", interactive=False),
        outputs=question_submit_btn
    ).then(
        fn=address_question,
        inputs=[question_state, answer_state, keypoints_state, address_number, address_question_input],
        outputs=address_output
    ).then(
        fn=lambda: gr.update(visible=True),
        outputs=address_output
    ).then(
        fn=lambda: gr.Button(value="确认提问", interactive=True),
        outputs=question_submit_btn
    )

app.launch()
