import os
import shutil
import urllib.request
import urllib.parse
import zipfile

def send_acc(acc):
    svc_ip = os.getenv("svc_ip")
    model_id = os.getenv("model_id")

    data = {'modelId': model_id, "acc": acc}
    data = urllib.parse.urlencode(data).encode('utf-8')
    address = "http://" + svc_ip + ":8080/train/addAcc"
    req = urllib.request.Request(url=address, data=data, method='POST')
    response = urllib.request.urlopen(req)
    # 根据需要，你可以添加处理响应或错误的代码。


def save_result(*source_files):
    model_id = os.getenv("model_id")
    destination_path = '/result'
    zip_filename = f"/download/{model_id}/results.zip"

    # 确保/download/model_id目录存在
    model_id_path = os.path.join('/download', model_id)
    if not os.path.exists(model_id_path):
        os.makedirs(model_id_path)

    # 创建一个新的zip文件
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for source_file in source_files:
            # 将文件复制到/result目录
            shutil.copy2(source_file, destination_path)
            # 将文件加入到zip包中
            zipf.write(os.path.join(destination_path, os.path.basename(source_file)), os.path.basename(source_file))
