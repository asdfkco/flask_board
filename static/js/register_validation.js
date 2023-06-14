function validation(){
    a = document.form
    if(a.id.value == ''){
        alert("id를 입력해주세요")
        return false;
    }else if(a.password.value == ''){
        alert("password를 입력해주세요")
        return false;
    }else if(a.repassword.value == ''){
        alert("비밀번호 재입력을 입력해주세요")
        return false;
    }else if(a.password.value != a.repassword.value){
        alert("비밀번호를 일치시켜주세요")
        return false;
    }else if(a.email.value == ''){
        alert("email을 입력해주세요")
        return false;
    }else{
        return true;
    }
}