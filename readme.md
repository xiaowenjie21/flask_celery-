celery异步并发处理任务后，使用下列代码获取task id
task = long_time_def.apply_async()
return jsonify({}),202,{'task_id':task.id} 	

AsyncResult 方法获取任务状态信息 
state 状态信息
info.get('i') 获取meta信息

update_state 用于更新进度信息并添加附加信息
参考地址: http://www.ziyoubaba.com/archives/732