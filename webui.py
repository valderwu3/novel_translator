"""
请帮我实现以下功能：
技术栈：python gradio
功能描述：
输入小说txt文件的路径。输出小说每个章节的翻译文件，后台功能已经做好，你只需要调佣translate 接口即可。
translate 接口需要以下参数：
novel：小说文件路径
seps：标识小说章节间隔字的符串，支持输入任意个数字符串。
translate_to_chapter：翻译到该章节后停止翻译。
auth_key：翻译API的api key。
界面上的控件可以输入以上参数。
请给出界面UI代码。
"""

from translate_novel import translate_novel, check_split
import gradio as gr


with gr.Blocks() as view:
    gr.Markdown("## 出海爆文章节翻译工具")
    # gr.Markdown("---")
    with gr.Column(min_width=100):
        with gr.Row():
            in1 = gr.inputs.File(type="file", label="上传小说txt文件")  # novel_file
            in2 = gr.inputs.Textbox(label="章节分割符, 多个字符串请用逗号隔开, 模糊匹配用*代替", default="内容简介, 第*章, 第*卷")  # seps
            in3 = gr.inputs.Textbox(label="从此章节开始翻译", default="第一章")  # translate_to_chapter
        with gr.Row():
            in4 = gr.inputs.Slider(minimum=1, maximum=10, step=1, label="翻译的章节数", default=3) # translate_to_chapter
            in5 = gr.inputs.Dropdown(choices=['DEEPL'], label="选择翻译引擎", default='DEEPL')  # translate_to_chapter
            in6 = gr.inputs.Textbox(label="翻译API的Key", default="")  # auth_key
    with gr.Column(min_width=100):
        with gr.Row():
            out1 = gr.outputs.Textbox(label="Processed Text")
            out2 = gr.outputs.File(label="Download Processed Text")
            # avatar = gr.outputs.Image(type='filepath', label="  ❤️")
            # with gr.Blocks():
            #     gr.Markdown("Created By: [](https://gradio.app/) for more information.")
            # with gr.Blocks():
            #     gr.Markdown("Check out the [Gradio website](https://gradio.app/) for more information.")
    inputs = [in1, in2, in3, in4, in5, in6]
    gr.Button("第一步: 检查章节分割是否正确").click(fn=check_split, inputs=inputs[:-2], outputs=out1)
    gr.Button("第二步: 开始翻译").click(fn=translate_novel, inputs=inputs, outputs=out2)
    gr.Button("❤️我是毛哥, AI+RPA副业探索中, 🌍 vx：wuvalder    ❤️")
view.title = "小说章节翻译工具"


view.launch(show_tips=True, show_error=True, share=True)