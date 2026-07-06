$(document).ready(function () {
$("#submitBtn").click(function(){
    let name = $("#name").val()
    let phone = $("#phone").val()
    let email = $("#email").val()
    let category = $("#category").val()

    if(name.trim() === ""){
        console.log("Name cannot be empty");
        return;
    }
    if(!/^\d{10}$/.test(phone)){
        console.log("Invalid phone");
        return;
    }
    let emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    if(!emailPattern.test(email)){
        console.log("Invalid email")
        return
    }
    console.log({name,phone,email,category});
});
})
