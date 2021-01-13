!function () {

    // const BACKENDHOST = 'http://192.168.43.66:8000'
    // const FRONTHOST = 'http://192.168.43.144'
    const BACKENDHOST = 'http://127.0.0.1:8000'
    const FRONTHOST = 'http://127.0.0.1'

    $('#play_run_btn').click(function () {

        const formData = $('#customFile')
        const filename = formData[0].files[0].name
        var form = new FormData();
        // form.append("name",filename)
        form.append("file", formData[0].files[0]);


        var requestOptions = {
            method: 'POST',
            body: form,
            redirect: 'follow'
        };

        var settings = {
            "url": `${BACKENDHOST}/v1/ml/files`,
            "method": "POST",
            "timeout": 0,
            "processData": false,
            "mimeType": "multipart/form-data",
            "contentType": false,
            "data": form,
            "responseType": "arraybuffer"
        };

        $.ajax(settings).done(function (res) {
            // const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
            // // 兼容不同浏览器的URL对象
            // const url = window.URL || window.webkitURL || window.moxURL
            // // 创建下载链接
            // const downloadHref = url.createObjectURL(blob)
            // // 创建a标签并为其添加属性
            // let downloadLink = document.createElement('a')
            // downloadLink.href = downloadHref
            // downloadLink.download = '结果汇总.xlsx'
            // // 触发点击事件执行下载
            // downloadLink.click()

            // saveFile(new Blob([res]), 'result.xlsx')
            

            let { data,excel } = JSON.parse(res)
            let failingMember = {}
            data.forEach((item, index) => {
                index = index + 1
                if (!item) return failingMember[index] = item
            })

            upload_main_right.style.display = 'block'

            let template = ''

            for (const row in failingMember) {
                template += `<tr>
                                <td>${row}</td>
                            </tr>`
            }
            tBody.innerHTML = template
            var div = document.createElement("div")
            div.setAttribute('style', "text-align: center;margin-top: 1rem;")
            div.innerHTML = '<button class="btn btn-success" id="play_run_btn_export">导出Excel</button>'

            tBody.append(div)
            play_run_btn_export.onclick = ()=>{
                let downloadLink = document.createElement('a')
                downloadLink.href = BACKENDHOST + excel
                downloadLink.download = '结果汇总.xlsx'
                downloadLink.click()
            }
            
            
        });

        

    })
    


    play_run_btn_export.onclick =


    play_run_btn_export.click(function(){

    })



    function parseDom(arg) {

        objE.innerHTML = arg
        return objE.childNodes
    }

    function saveFile(url, filename) {
        var a = document.createElement('a');
        a.href = URL.createObjectURL(url);
        a.download = filename;
        var e = document.createEvent("MouseEvents");
        e.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        a.dispatchEvent(e);
    }
}()