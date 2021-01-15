!function () {

    // const BACKENDHOST = 'http://192.168.43.66:8000'
    // const FRONTHOST = 'http://192.168.43.144'
    const BACKENDHOST = 'http://127.0.0.1:8000'
    const FRONTHOST = 'http://127.0.0.1'

    // 注册
    $('#register-btn').click(function (e) {
        e.preventDefault()

        const username = $('#user_name').val()
        const email = $('#exampleInputEmail1').val()
        const password = $('#exampleInputPassword1').val()
        const phone = $('#number').val()


        var settings = {
            "url": `${BACKENDHOST}/v1/users`,
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Content-Type": "application/json"
            },
            "data": JSON.stringify({ username, email, password, phone }),
        };

        $.ajax(settings).done(function (res) {
            if (res.code == 200){
                const username = res.username
                const token = res.data.token
                
                window.localStorage.setItem(username,token)
                location.href = FRONTHOST
                alert('注册成功，请稍后进入邮箱激活账号')
            }
        });
    })

    // 登录
    $('#login-btn').click(function (e) {
        e.preventDefault()

        const username = $('#user_name2').val()
        const password = $('#exampleInputPassword2').val()
        var settings = {
            "url": `${BACKENDHOST}/v1/tokens`,
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Content-Type": "application/json"
            },
            "data": JSON.stringify({ username, password}),
        };

        $.ajax(settings).done(function (res) {
            if (res.code == 200){
                const username = res.username
                const token = res.data.token
                
                window.localStorage.setItem(username,token)
                location.href = `${FRONTHOST}/after_login/index.html`
            }
        });
    })

    

}()