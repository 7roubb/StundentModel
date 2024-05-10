let aside = document.getElementById("aside");
let user = document.getElementById("user");
let aside_texts = document.querySelectorAll(".text");

user.addEventListener("click", () => {
  aside.classList.toggle("active");
  aside.classList.value.indexOf("active") != -1
    ? aside_texts.forEach((e, i) =>
        setTimeout(() => e.classList.add("active"), 100 * (i + 1))
      )
    : aside_texts.forEach((e) => e.classList.remove("active"));
});

let add = document.getElementById("add").onclick = () => {
  console.log("xclick")
}


const email = document.getElementById("email")
const message = document.getElementById("message")

function ValidateEmail(mail) 
{
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(myForm.emailAddr.value))
  {
    return (true)
  }
    alert("You have entered an invalid email address!")
    return (false)
}

