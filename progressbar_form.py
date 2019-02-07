from flask import Flask,jsonify,render_template
from celery import Celery


app = Flask(__name__)

from celery import platforms  #如果你不是linux的root用户，这两行没必要
platforms.C_FORCE_ROOT=True   #允许root权限运行celery

def make_celery(app):
    celery = Celery("progressbar_form",  # 此处官网使用app.import_name，因为这里将所有代码写在同一个文件flask_celery.py,所以直接写名字。
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND']
                    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL='amqp://admin:2955112@192.168.247.130/',
    CELERY_RESULT_BACKEND='db+mysql://root:123456@192.168.247.130/py3code'
)

celery = make_celery(app)

@celery.task(bind = True)
def long_time_def(self):
    for i in range(100):
        print('start number: ', i)
        self.update_state(state = 'PROGRESS', meta = {'i': i})
    return 'finished'

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/run', methods=['POST','GET'])
def count():
    # 长时间的任务
    task = long_time_def.apply_async()
    return jsonify({}),202,{'task_id':task.id}    # 将task_id 写入到返回头之中 ，前端可以通过这种方式来获取 task_id 的值：resp.getResponseHeader('task_id');

@app.route('/status/<task_id>')
def task_status(task_id):
    # 获取celery之中 task_id的状态信息
    the_task = long_time_def.AsyncResult(task_id)   # 获取状态信息
    print("任务：{0} 当前的 state 为：{1}".format(task_id,the_task.state))
    if  the_task.state=='PROGRESS':
        resp = {'state':'progress','progress':the_task.info.get('i',0)}
    elif  the_task.state=='SUCCESS':
        resp = {'state':"success",'progress':100}
    elif the_task.state == 'PENDING':   # 任务处于排队之中
        resp = {'state':'waitting','progress':0}
    else:
        resp = {'state':the_task.state,'progress':the_task.info.get('i',0)}
    return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port = 5000)