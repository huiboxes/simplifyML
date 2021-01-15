from django.http import JsonResponse, StreamingHttpResponse
import pandas as pd
import joblib
import uuid
import json
from tools.logging_dec import logging_check


# 10300-10399 errorCode

def files(request):
    if request.method == 'POST':
        # 根据模型选择分析结果，暂时只有一个模型
        # m = request.POST.get('scoreWaraning')
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[1]
        if excel_type in ['csv']:
            user_data = pd.read_csv(f, index_col=0)
            try:
                # 删除姓名和学号列
                user_data_copy = user_data.drop(['姓名', '学号'], axis=1)
                # 加载随机森林模型
                model = joblib.load('static/scoreWarning-rf.pkl')
                # 预测
                predict = model.predict(user_data_copy)
                # 将预测结果作为新字段，最终表字段有：姓名、学号、预测结果
                newField = '成绩（True为合格，False为不合格）'
                user_data.loc[:, newField] = predict
                user_data = user_data[['姓名', '学号', newField]]
                # 将结果转为excel存储
                filename = 'static/result' + str(uuid.uuid1()) + '.xlsx'
                user_data.to_excel(filename)

                res_data = {
                    'name': user_data['姓名'].to_list(),
                    'sid': user_data['学号'].to_list(),
                    'predict': predict.tolist(),
                }
                # predict.to_excel(filename)
                # response = StreamingHttpResponse(file_iterator(filename))
                # response['Content-Type'] = 'application/octet-stream'
                # response['Content-Disposition'] = 'attachment; filename="{}" '.format("result.xlsx")
                # return response

                result = {'code': 200, 'data': res_data, 'excel': '/' + filename}
                return JsonResponse(result, charset='utf-8')

            except Exception as e:
                print(e)
                result = {'code': 10302, 'error': '分析数据现时出错误，请重试'}
                return JsonResponse(result, charset='utf-8')

        else:
            result = {'code': 10303, 'error': '上传文件类型错误'}
            return JsonResponse(result, charset='utf-8')


def file_iterator(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
