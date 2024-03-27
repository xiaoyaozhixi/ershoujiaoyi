var error_name = false;
	var error_password = false;
	var error_check_password = false;

	$('#user').blur(function() {
		check_user_name();
	});

	$('#password').blur(function() {
		check_pwd();
	});

	$('#password2').blur(function() {
        check_pwd();
		check_cpwd();
	});

function check_user_name(){
	var len = $('#user').val().length;
	if(len<2||len>20)
	{
		$('#user').next().html('请输入2-20个字符的用户名')
		$('#user').next().show();
		error_name = true;
	}
	else
	{
		$('#user').next().hide();
		error_name = false;
	}
}

function check_pwd(){
var len = $('#password').val().length;
var len2 = $('#password2').val().length;
	if(len<6||len>20)
	{
		$('#password').next().html('密码最少6位,最长20位')
		$('#password').next().show();
		error_password = true;
	}
	else
	{
		$('#password').next().hide();
		error_password = false;
	}
    if(len2<6||len2>20)
	{
		$('#password2').next().html('密码最少6位,最长20位')
		$('#password2').next().show();
		error_password = true;
	}
	else
	{
		$('#password2').next().hide();
		error_password = false;
	}
}

function check_cpwd(){
	var pass = $('#password').val();
	var cpass = $('#password2').val();
	if(pass!=cpass)
	{
		$('#password2').next().html('两次输入的密码不一致')
		$('#password2').next().show();
		error_check_password = true;
	}
	else
	{
		$('#password2').next().hide();
		error_check_password = false;
	}
}

function yzmFun(selector,w,h){
    // 随机数的生成
    function randomNum(min,max){
        return parseInt(Math.random()*(max-min)+min)
    }
    //随机生成颜色的函数
    function randomColor(min,max) {
        let r = randomNum(min,max)
        let g = randomNum(min,max)
        let b = randomNum(min,max)
        return `rgb(${r},${g},${b})`
    }
    let canvas = document.querySelector(selector)
    let ctx = canvas.getContext('2d')
    //在canvas绘制背景颜色
    ctx.fillStyle = randomColor(180,230)
    ctx.fillRect(0,0,w,h)
    let pool = 'ABCDEFGHIGKLIMNOPQRSTUVWXYZabcdefghigklimnopqrstuvwxyz1234567890'
    let yzm = ''
    //生成随机的验证码
    for(let i = 0;i<4;i++){
        let c = pool[randomNum(0,pool.length)]
        //随机出字体大小
        let fs = randomNum(18,40)
        //随机字体角度
        let deg = randomNum(-30,30)
        ctx.font = fs + 'px Simhei'
        ctx.textBaseline = 'top'
        //设置字体颜色
        ctx.fillStyle = randomColor(80,150)
        //保存
        ctx.save()
        //位置
        ctx.translate(30*i+15,15)
        //旋转
        ctx.rotate(deg*Math.PI/180)
        ctx.fillText(c,-10,-10)
        ctx.restore()
        yzm+=c
    }
    //随机生成干扰线
    for(let i = 0;i<5;i++){
        ctx.beginPath()
        ctx.moveTo(randomNum(0,w),randomNum(0,h))
        ctx.lineTo(randomNum(0,w),randomNum(0,h))
        ctx.strokeStyle = randomColor(180,230)
        ctx.closePath()
        ctx.stroke()
    }
    //随机产生干扰圆点
    for(let i = 0;i<40;i++){
        ctx.beginPath()
        ctx.arc(randomNum(0,w),randomNum(0,h),1,0,2*Math.PI)
        ctx.fillStyle = randomColor(150,200)
        ctx.fill()
    }
    return yzm
    }
    //调用生成验证码
    let yzmStr = yzmFun('#canvas',120,40).toLowerCase()
    
    //验证验证码是否正确
    function validation(){
        //获取input的值转换为小写
        let yzmInput = document.getElementById('input').value.toLowerCase()
        if(yzmStr === yzmInput){
            window.location.href="/user/login.html"
            alert("成功")
            
        }else{
            alert("验证码错误")
            location.reload()
        }
        
    }
    //更换验证码
    function reload(){
        location.reload()
    }
    console.log(yzmStr)

//提交事件
$('.submit').on('click',function(){
    check_user_name();
		check_pwd();
		check_cpwd();
        validation();
		if(error_name == false && error_password == false && error_check_password == false && error_number == false)
		{
			return true;
		}
		else
		{
			return false;
		}
})
