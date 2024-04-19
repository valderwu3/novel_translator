import os
import deepl
import zipfile
import re
import gradio
import logging as log


# level=logging.DEBUG 、INFO 、WARNING、ERROR、CRITICAL
log.basicConfig(filename='log.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s', level='INFO')


def starts_with_one_of(line, *tags):
    for tag in tags:
        if re.match(tag, line.lstrip()):
            return True
    return False


def translate(origin, auth_key, target_lang='EN-US'):
    translator = deepl.Translator(auth_key)
    try:
        result = translator.translate_text(origin, target_lang=target_lang)
    except deepl.exceptions.QuotaExceededException:
        gradio.Error("DEEPL API 已消耗完!")
        raise Exception("DEEPL API 已消耗完!")
    return result.text


def split_chapters(novel_file, seps, translate_from_chapter, translate_chapter_count=3):
    # Gradio会传递一个有关上传文件的字典，你可以使用以下方式来获取它的内容
    if novel_file is not None:
        chapters = []
        chapter = ''
        start_flag = False
        end_flag = False
        count = 0
        with open(novel_file.name, encoding="gbk") as f:
            for line in f:
                if not start_flag and translate_from_chapter in line:
                    start_flag = True
                if start_flag and starts_with_one_of(line, *seps):
                    if chapter:
                        count += 1
                        chapters.append(chapter)
                        chapter = ''
                        if count == translate_chapter_count:
                            end_flag = True
                            break
                    if start_flag:
                        chapter += line
                    if not end_flag:
                        chapters.append(chapter)
            return chapters


def zip_txt_files(translated_chapters, zip_name):
    # 使用'w'参数打开zip文件以创建并写入
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        # 遍历文件列表并写入每个文件到zip
        for file_name, content in translated_chapters.items():
            # 添加文件到zip包，并使用basename作为文件在zip中的名字
            zipf.writestr(file_name, content)
    print(f"Created zip file at: {zip_name}")


def translate_chapters(chapters, auth_key):
    translated_chapters = {}
    for chapter in chapters:
        if not chapter.strip():
            continue
        file_name = chapter.split('\n', maxsplit=1)[0].strip()+'.en.txt'
        log.info(f"translating {file_name} ...")
        translated_chapters[file_name] = translate(chapter, auth_key)
    return translated_chapters


def translate_novel(novel_file, seps, translate_from_chapter, translate_chapter_count, api_type, auth_key):
    seps = seps.strip().replace('，', ',').replace('*', '.*').split(',')
    seps = [sep.strip() for sep in seps]
    chapters = split_chapters(novel_file, seps, translate_from_chapter, translate_chapter_count)
    translated_chapters = translate_chapters(chapters, auth_key.strip())
    zip_name = novel_file.name + '.en.zip'
    zip_txt_files(translated_chapters, zip_name)
    log.info(f"zip {zip_name} ...")
    return zip_name


def check_split(novel_file, seps, translate_from_chapter, translate_chapter_count):
    seps = seps.strip().replace('，', ',').replace('*', '.*').split(',')
    seps = [sep.strip() for sep in seps]
    chapters = split_chapters(novel_file, seps, translate_from_chapter, translate_chapter_count)
    chapter_info = ' |  '.join([chapter.split(maxsplit=1)[0] for chapter in chapters])
    log.info(f"split {chapter_info} ...")
    return chapter_info


if __name__ == '__main__':
    AUTH_KEY = ""  # Replace with your key
    NOVEL = 'D:/SecondaryJob/小说爆文出海/古咒亡灵/63《亡灵古咒》作者：轩辕波.txt'
    SEPS = ['内容简介', '第.*章', '第.*卷']
    TRANSLATE_TO_CHAPTER = '第五章'
    translate_novel(NOVEL, SEPS, TRANSLATE_TO_CHAPTER, AUTH_KEY)
    # lst = split_chapters(NOVEL, SEPS, "第一十章", 8)
    # print([item.split()[0] for item in lst])