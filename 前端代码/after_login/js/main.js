!(function () {
  // const BACKENDHOST = 'http://192.168.43.66:8000'
  // const FRONTHOST = 'http://192.168.43.144'
  const BACKENDHOST = 'http://127.0.0.1:8000'
  const FRONTHOST = 'http://127.0.0.1'

  // 上传文件，请求后台分析数据
  $('#play_run_btn').click(function () {
    const formData = $('#customFile')
    const filename = formData[0].files[0].name
    var form = new FormData()
    // form.append("name",filename)
    form.append('file', formData[0].files[0])

    var requestOptions = {
      method: 'POST',
      body: form,
      redirect: 'follow',
    }

    var settings = {
      url: `${BACKENDHOST}/v1/ml/files`,
      method: 'POST',
      timeout: 0,
      processData: false,
      mimeType: 'multipart/form-data',
      contentType: false,
      data: form,
      responseType: 'arraybuffer',
    }
    // 显示返回结果
    $.ajax(settings).done(function (res) {
      // saveFile(new Blob([res]，{ type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }), 'result.xlsx')

      // 从响应里解析出数据
      let { data, excel } = JSON.parse(res)
      let { name, sid, predict } = data

      // 创建存放未通过的名单
      let failureList = {}

      // 没通过的人员 {学号：姓名}
      predict.forEach((item, index) => {
        if (!item) {
          id = sid[index]
          failureList[id] = name[index]
        }
      })

      // 生成表格
      let template = ''
      for (const row in failureList) {
        template += `<tr>
                       <td>${row}</td>
                       <td>${failureList[row]}</td>
                     </tr>
                      `
      }

      tBody.innerHTML = template
      var div = document.createElement('div')
      div.setAttribute('style', 'text-align: center;margin-top: 1rem;')
      div.innerHTML =
        '<button class="btn btn-success" style="margin-left: 1rem;" id="play_run_btn_export">导出Excel</button>'

      failureTable.append(div)

      // 显示excel导出按钮
      upload_main_right.style.display = 'block'

      play_run_btn_export.onclick = () => {
        let downloadLink = document.createElement('a')
        downloadLink.href = BACKENDHOST + excel
        downloadLink.download = '结果汇总.xlsx'
        downloadLink.click()
      }
    })
  })

  function saveFile(url, filename) {
    var a = document.createElement('a')
    a.href = URL.createObjectURL(url)
    a.download = filename
    var e = document.createEvent('MouseEvents')
    e.initMouseEvent(
      'click',
      true,
      false,
      window,
      0,
      0,
      0,
      0,
      0,
      false,
      false,
      false,
      false,
      0,
      null
    )
    a.dispatchEvent(e)
  }
})()
