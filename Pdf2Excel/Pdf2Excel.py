# -*- coding: utf-8 -*-
import argparse
import os
import time

from Pdf2Excel.AbbyyOnlineSdk import *

processor = AbbyyOnlineSdk()

class Pdf2Excel(object):
    """
    build ABBYY OCR into a Pdf2Excel apckage,
    Environment Demands: argparse, AbbyyOnlineSdk
    """
    
    processor = AbbyyOnlineSdk()

    def setup_processor(self):
    	if "ABBYY_APPID" in os.environ:
    		processor.ApplicationId = os.environ["ABBYY_APPID"]

    	if "ABBYY_PWD" in os.environ:
    		processor.Password = os.environ["ABBYY_PWD"]

    	# Proxy settings
    	if "http_proxy" in os.environ:
    		proxy_string = os.environ["http_proxy"]
    		print("Using http proxy at {}".format(proxy_string))
    		processor.Proxies["http"] = proxy_string

    	if "https_proxy" in os.environ:
    		proxy_string = os.environ["https_proxy"]
    		print("Using https proxy at {}".format(proxy_string))
    		processor.Proxies["https"] = proxy_string


    # Recognize a file at filePath and save result to resultFilePath
    def recognize_file(self,file_path, result_file_path, language, output_format):
        print("Uploading..")
        settings = ProcessingSettings()
        settings.Language = language
        settings.OutputFormat = output_format
        task = processor.process_image(file_path, settings)
        if task is None:
            print("Error")
            return
        if task.Status == "NotEnoughCredits":
            print("Not enough credits to process the document. Please add more pages to your application's account.")
            return

        print("Id = {}".format(task.Id))
        print("Status = {}".format(task.Status))

        # Wait for the task to be completed
        print("Waiting..")
        # Note: it's recommended that your application waits at least 2 seconds
        # before making the first getTaskStatus request and also between such requests
        # for the same task. Making requests more often will not improve your
        # application performance.
        # Note: if your application queues several files and waits for them
        # it's recommended that you use listFinishedTasks instead (which is described
        # at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).

        while task.is_active():
            time.sleep(5)
            print(".")
            task = processor.get_task_status(task)

        print("Status = {}".format(task.Status))

        if task.Status == "Completed":
            if task.DownloadUrl is not None:
                processor.download_result(task, result_file_path)
                print("Result was written to {}".format(result_file_path))
        else:
            print("Error processing task")

    def create_parser():
        parser = argparse.ArgumentParser(description="Recognize a file via web service")
        parser.add_argument('source_file')
        parser.add_argument('target_file')

        parser.add_argument('-l', '--language', default='English', help='Recognition language (default: %(default)s)')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-txt', action='store_const', const='txt', dest='format', default='txt')
        group.add_argument('-pdf', action='store_const', const='pdfSearchable', dest='format')
        group.add_argument('-rtf', action='store_const', const='rtf', dest='format')
        group.add_argument('-docx', action='store_const', const='docx', dest='format')
        group.add_argument('-xml', action='store_const', const='xml', dest='format')

        return parser

    #from process import *
    #这一步即可以，相当于加载上述函数，上面函数本来就是从process.py摘抄出来一步步run的
    def __init__(self,result="myworkbook.xlsx",Language="English",typefile="xlsx"):
        """
        Language input can be found here:https://ocrsdk.com/documentation/specifications/recognition-languages/ 
        typefile input can be found here:https://ocrsdk.com/documentation/specifications/export-formats/ 
        """
        self.setup_processor()
        
        path=input("Your Pdf file path:  like'C:/data/1.pdf'")
        start=time.time()
        self.recognize_file(path, result, Language, typefile)#能识别中文简体ChinesePRC繁体ChineseTaiwan；中英文混合的怎么设置？？？？
        #https://ocrsdk.com/documentation/specifications/recognition-languages/      语言列表
        #https://ocrsdk.com/documentation/specifications/export-formats/         输出格式列表
        T1=time.time()-start
        print('Total time spend %d seconds for 22 page pdf'%T1)
        #About 5 seconds per page
        #22 pages 都在一个sheet里，差评
        
if __name__ == '__main__':
    main()
