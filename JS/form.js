document.addEventListener("DOMContentLoaded", function() {
    // Bind event listener to form submit event
    document.querySelector("form").addEventListener("submit", function(event) {
        // Prevent default form submission behavior
        event.preventDefault();
        
        // Call the validateForm function to validate the form fields
        validateForm();
    });
});

function validateForm() {
    let salutation = document.getElementById("salutation").value;
    let firstName = document.getElementById("firstName").value;
    let lastName = document.getElementById("lastName").value;
    let email = document.getElementById("email").value;
    let birthDate = document.getElementById("birthDate").value;
    let address = document.getElementById("address").value;
    let country = document.getElementById("country").value;
    let profilePic = document.getElementById("profilePic").value;
    let cv = document.getElementById("cv").value;
    
    // Validation for salutation
    if (salutation === "") {
        alert("Please select a salutation.");
        return false;
    }
    
    // Validation for first name
    if (firstName === "") {
        alert("Please enter your first name.");
        return false;
    }
    
    // Validation for last name
    if (lastName === "") {
        alert("Please enter your last name.");
        return false;
    }

    // Validation for email
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    // Validation for birth date
    if (birthDate === "") {
        alert("Please enter your date of birth.");
        return false;
    }

    // Validation for address
    if (address === "") {
        alert("Please enter your address.");
        return false;
    }

    // Validation for country
    if (country === "") {
        alert("Please select your country.");
        return false;
    }

    // Validation for profile picture
    if (profilePic === "") {
        alert("Please upload your profile picture.");
        return false;
    }

    // Validation for CV
    if (cv === "") {
        alert("Please upload your CV.");
        return false;
    }

    // Success message if all validations pass
    alert("Success!");
    return true;
}
