document.addEventListener("DOMContentLoaded", function() {
    var toggleInput = document.getElementById('toggle');

    toggleInput.addEventListener('change', function() {
        var pageBody = document.body;
        if (this.checked) {
            // Toggle is checked (Bar Owner)
            pageBody.classList.remove('customer-theme');
            pageBody.classList.add('bar-owner-theme');
        } else {
            // Toggle is unchecked (Customer)
            pageBody.classList.remove('bar-owner-theme');
            pageBody.classList.add('customer-theme');
        }
    });
    
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        // Add your login validation logic here
        // For now, let's just log the entered username and password
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        console.log('Username:', username);
        console.log('Password:', password);
    });
});
