(function(){
  emailjs.init("cDocXB4KP9DiXceV9");
})();

function sendCode(to_email, secure_code) {
  const templateParams = {
    to_email: to_email,
    secure_code: secure_code
  };

  emailjs.send("service_oyr30np", "template_vuqjrhf", templateParams)
    .then(() => {
      console.log("✅ Email sent successfully");
    }, (error) => {
      console.error("❌ Failed to send email:", error);
    });
}
