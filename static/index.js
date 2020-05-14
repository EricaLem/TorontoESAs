
// When the DOM content is loaded (EVENT #1), run this function....
document.addEventListener('DOMContentLoaded', () => {
    // FORM: When the currency field is submitted....
    document.querySelector('#form').onsubmit = () => {

        // XMLHttpRequest() = AJAX request to some other web server (i.e. fixer.io)
        // to get information
        const request = new XMLHttpRequest();
        // define new JS variable 'currency' to retrieve value of
        // #currency, which is whatever the user typed into the text input field
        const currency = document.querySelector('#currency').value;
        // Initialize new request
        // Use URL defined in application.py
        request.open('POST', '/convertcurrency');

        // Callback function for when request is complete (onload)
        request.onload = () => {
            // Extract JSON data from request
            // data is a variable equal to the JSON object that is
            // returned to us from request to fixer.io
            // request.responseText = attribute of request we can use to get text of response
            // JSON.parse = built-in JS fxn to parse/access text from a JSON object
            const data = JSON.parse(request.responseText);
            // Update the result div
            // Recall that in the @app.route in application.py, the success key from the JSON object could be true or false.
            if (data.success) {
                // ${data.rate} = comes back in the responseText
                const contents = `1 EUR is equal to ${data.rate} ${currency}.`;
                document.querySelector('#result').innerHTML = contents;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error. :(';
            }
        }

        // Now we need to render this info to the web server........
        // Add data to send with request
        const data = new FormData();
        data.append('currency', currency);

        // Send request to the @app.route in application.py
        request.send(data);
        return false;
    };
});