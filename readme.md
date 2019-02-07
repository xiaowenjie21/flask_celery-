celery异步并发处理任务后，使用下列代码获取task id
task = long_time_def.apply_async()
return jsonify({}),202,{'task_id':task.id} 	

AsyncResult 方法获取任务状态信息 
state 状态信息
info.get('i') 获取meta信息

update_state 用于更新进度信息并添加附加信息
参考地址: http://www.ziyoubaba.com/archives/732
注意: broker_url 与 backend_url 应同为一个服务器, 如此则可提高并发速度，如果是另外服务器，在获取状态的时候会操作数据库提取任务完成状态信息
导致耗时, 运行较慢