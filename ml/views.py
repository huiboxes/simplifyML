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
                # x = user_data.drop(['成绩'], axis=1)
                model = joblib.load('static/scoreWarning-rf-2.pkl')
                predict = model.predict(user_data)

                # user_data.loc[:, '成绩（True为合格，False为不合格）'] = predict

                filename = 'static/result' + str(uuid.uuid1()) + '.xlsx'

                pd.DataFrame(predict).to_excel(filename)

                # predict.to_excel(filename)
                # response = StreamingHttpResponse(file_iterator(filename))
                # response['Content-Type'] = 'application/octet-stream'
                # response['Content-Disposition'] = 'attachment; filename="{}" '.format("result.xlsx")
                # return response

                result = {'code': 200, 'data': predict.tolist(), 'excel': '/' + filename}
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
