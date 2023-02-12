import asyncio

import filetools.fstructs as fstructs
import filetools.ftools as ftools
from classify import FileClassifier
from config.config import Config
from filetools.FileToText import FileToText
from listener.filemonitor import ListenForFiles


def listen_daemon():
    listen = ListenForFiles(r"D:\dev\hacknotts\23\Filerize\test_files")
    listen.run()


async def label_folder(folder: fstructs.Folder):
    files = [file for file in folder.files if file.ext == 'pdf']
    tasks: dict[fstructs.File, asyncio.Task] = {}
    for file in files:
        # PDF to text
        test_pdf: str = FileToText.pdf_to_text(
            f'{file.path}', CUT_STR=True, max_output_length=1000)
        # Classify text
        tasks[file] = asyncio.create_task(
            FileClassifier.classify(test_pdf, Config.labels))

    for file in tasks:
        file.label = await tasks[file]


async def sort(path):

    folder = fstructs.Folder(path=path)
    await ftools.recursive_visit(folder=folder, visit=label_folder)

    ftools.recursive_move(folder=folder)

async def listen():
    pass