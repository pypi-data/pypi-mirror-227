import jreqai

# 1. 从远程服务器获取模型
model = jreqai.pull("http://127.0.0.1:8181", "qihuo")
print(model)


# 2. 将模型推送到远程服务器
resp = jreqai.push("http://127.0.0.1:8181", "qihuo", model)
print(resp['code'])


# 3. 获取模型全部版本号
resp = jreqai.versions("http://127.0.0.1:8181", "qihuo")
print(resp)
