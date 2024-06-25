const user= document.getElementById("user1").value;
console.log(user)
function valid(){
    const email1= document.getElementById("email").value
    const user2= document.getElementById("user1").value
    const phone= document.getElementById("phone-no").value
    const pass= document.getElementById("pass").value
    const cpass = document.getElementById("c-pass").value
    var mail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var phoneno = /^\d{10}$/;
    var passw=  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;;

    //const user2= document.getElementById("user1").value

    if(document.getElementById("email").value.trim().length<1){
        alert("Please Enter the Email");
        document.getElementById("email").focus()
        return false
    }
    if(!(email1.match(mail))){
        alert("Please Enter a valid Email");
        document.getElementById("email").focus()
        return false
    }

    if(document.getElementById("user1").value.trim().length<1 ){
        alert("Please Enter the UserName");
        document.getElementById("user1").focus()
        return false
    }
    if(user2.length<5){
        alert("Please Enter the UserName");
        document.getElementById("user1").focus()
        return false
    }
    
    if(document.getElementById("phone-no").value.trim().length<1){
        alert("Please Enter the Phone No");
        document.getElementById("phone-no").focus()
        return false
    }
    

    if(!(phone.match(phoneno))){
        alert("Please Enter a valid Phone No");
        document.getElementById("phone-no").focus()
        return false
    }
    if(document.getElementById("pass").value.trim().length<1){
        alert("Please Enter the Password");
        document.getElementById("pass").focus()
        return false
    }
    if(!(pass.match(passw))){
        alert(" the password should be8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character");
        document.getElementById("pass").focus()
        return false
      }
    if(document.getElementById("c-pass").value.trim().length<1){
        alert("Please Enter the Confirm Password");
        document.getElementById("c-pass").focus()
        return false
    }
    if(!(cpass.match(passw))){
        alert(" the password should be8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character");
        document.getElementById("c-pass").focus()
        return false
      }
    
    if(pass!=cpass){
        alert("Password and Confirm Password must be same");
        document.getElementById("c-pass").focus()
        return false
    }
    
    
    return true
}
function valid1(){
    const user = document.getElementById("username").value
    const pass = document.getElementById("password").value
    //const user1 = 
    if(user.trim().length<1 ){
        alert("Please Enter the user Name ");
        document.getElementById("username").focus()
        return false
    }
    if(user.length<5 ){
        alert("Please Enter the user Name ");
        document.getElementById("username").focus()
        return false
    }

    if(pass.trim().length<1){
        alert("Please Enter the  Password");
        document.getElementById("password").focus()
        return false
    }
    return true
}