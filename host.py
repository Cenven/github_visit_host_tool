import copy
import os
import socket
import subprocess
import re
import shutil
import requests

subprocess.Popen("runas /savecred /user:Administrator cmd", shell=True)


# 是否联网
def  isConnected():
  try:
   html = requests.get("http://www.baidu.com",timeout=2)
  except:
   return False
  return True

# 获取ip列表
def get_ip_list(domain): # 获取域名解析出的IP列表
  ip_list = []
  try:
    addrs = socket.getaddrinfo(domain, None)
    for item in addrs:
      if item[4][0] not in ip_list:
        ip_list.append(item[4][0])
  except Exception as e:
    print(str(e))
    pass
  return ip_list

# 获取ip地址
def getIP(domain):
  process = subprocess.Popen(["nslookup", domain], stdout=subprocess.PIPE)
  output = str(process.communicate()[0]).split('\\r\\n')
  print(domain+' => ',output)
  address = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",output[5])
  if not address:
      address = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", output[4])

  if address:
    return address[0]
  else:
    return ''

domain_list={
    'github_domain':'github.com',
    'github_gist':'gist.github.com',
    'github_raw':'raw.githubusercontent.com',
    'github_cloud':'cloud.githubusercontent.com',
    'github_camo':'camo.githubusercontent.com',
    'github_fastly':'github.global.ssl.fastly.net',
    'github_assets':'assets-cdn.github.com',
    'github_avatars0':'avatars0.githubusercontent.com',
    'github_avatars1':'avatars1.githubusercontent.com',
    'github_avatars2':'avatars2.githubusercontent.com',
    'github_avatars3':'avatars3.githubusercontent.com',
    'github_avatars4':'avatars4.githubusercontent.com',
    'github_avatars5':'avatars5.githubusercontent.com',
    'github_avatars6':'avatars6.githubusercontent.com',
    'github_avatars7':'avatars7.githubusercontent.com',
    'github_avatars8':'avatars8.githubusercontent.com',
}
ip_list={}
domain_exit_res = {}
# 获取系统盘
drive = os.getenv("SystemDrive")
print("获取系统盘",drive)

# 源文件地址
host_path = drive + '\\Windows\\System32\\drivers\\etc\\hosts'
# 新文件地址
new_host_path = 'hosts'
# 新文件存储地址
target_path = drive + '\\Windows\\System32\\drivers\\etc\\hosts'
# 新文件存储目录
target_col = drive+ '\\Windows\\System32\\drivers\\etc'

if not os.path.exists(host_path):
    print("源hosts文件不存在自动创建")
    subprocess.Popen('type nul> ' + host_path, shell=True)

for element in domain_list:
    ip_list[element] = getIP(domain_list[element])
    print(element + ' => ' +getIP(domain_list[element]))
    domain_exit_res[element] = 0

def updateStr():
    # host文件不存在创建
    if os.path.exists(host_path):
        # 备份原host文件
        if os.path.exists('host'):
            print("备份host已存在")
        else:
            shutil.copy(host_path, 'host_backup')

    file = open(host_path, 'r', encoding="utf-8")  # 以读方式打开

    # 源文件数组
    list = file.readlines()

    file.close()

    # 需要修改的数组节点信息
    node_list = {}
    # 新文件数组
    origin_file = copy.deepcopy(list)

    # for循环源文件数组正则验证是否存在domain_list中的域名
    for index,line in enumerate(list):
        # print("list => ",line)
        for item in domain_list:
            if re.search(r' ' + domain_list[item], line) is not None:
                # 非注释的修改
                if re.search('#', line) is None:
                    domain_exit_res[item] = 1
                    # ip_list中当前domain_list项中存在ip
                    if ip_list[item]:
                        copy_line = re.sub(r"[\s\S]+", ip_list[item] + ' ' + domain_list[item]+'\n', line)
                        # if re.search('\n', line) is not None:
                        #     copy_line = copy_line+'\n'

                        node_list[index] = {
                            'lineNum':index,
                            'record':copy_line
                        }

    # print('node_list => ',list)

    # 循环节点信息修改新文件数组
    for idx,item in enumerate(node_list):
        # print(node_list[item])
        origin_file[item] = node_list[item]['record']

    # 追加没有的host
    for item in domain_exit_res:
        if domain_exit_res[item] == 0:
            copy_line = ip_list[item] + ' ' + domain_list[item] + '\n'
            origin_file.append(copy_line)

    file_w = open(new_host_path, 'w', encoding="utf-8")
    for line in origin_file:
        file_w.write(line)

    print("hosts新文件生成")
    file_w.close()

if isConnected():
    updateStr()

    if os.path.exists(target_path):
        print("hosts文件已存在强制覆盖")
        os.remove(target_path)
        # os.rename(new_host_path, target_path)
        subprocess.Popen('move '+new_host_path+' '+target_col, shell=True)
    else:
        # os.rename(new_host_path, target_path)
        subprocess.Popen('move ' + new_host_path + ' ' + target_col, shell=True)

    result =os.popen("ipconfig/flushdns")
    print(result.read())