# github_visit_host_tool
这是一个github访问的小工具，会自动修改host文件，仅适用于window系统，此工具使用一次解决不了长期的问题，失效了在重新运行即可


This is a GitHub access tool that will automatically modify the host file. It is only applicable to the window system. This tool cannot solve the long-term problem once it is used

## 导出依赖
   - pipreqs ./ --encoding=utf8 --force
## 安装依赖
   - pip3 install -r requirements.txt
### Build to exe
   - pyinstaller -F host.py 