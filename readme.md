celery�첽�������������ʹ�����д����ȡtask id
task = long_time_def.apply_async()
return jsonify({}),202,{'task_id':task.id} 	

AsyncResult ������ȡ����״̬��Ϣ 
state ״̬��Ϣ
info.get('i') ��ȡmeta��Ϣ

update_state ���ڸ��½�����Ϣ����Ӹ�����Ϣ
�ο���ַ: http://www.ziyoubaba.com/archives/732
ע��: broker_url �� backend_url ӦͬΪһ��������, ��������߲����ٶȣ������������������ڻ�ȡ״̬��ʱ���������ݿ���ȡ�������״̬��Ϣ
���º�ʱ, ���н���