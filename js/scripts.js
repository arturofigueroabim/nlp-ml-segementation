//
// Scripts
// 


window.addEventListener('DOMContentLoaded', event => {

    const submitButton = document.getElementById('submit');
    submitButton.addEventListener('click', printValues);

    // Activate Bootstrap scrollspy on the main nav element
    const sideNav = document.body.querySelector('#sideNav');
    if (sideNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#sideNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function(responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    function printValues(event) {
        event.preventDefault();

        const data = {
            text: document.getElementById('essay').value
        };
        console.log(data)
        console.log('Calling service');


        let response = fetch('https://nlp-ml-segementation.herokuapp.com/predict', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: "POST",
                body: JSON.stringify(data)
            })
            .then(function(response) {
                console.log("Response: " + response);
                return response.json();
            })
            .catch(function(error) {
                console.log("Error: " + error);
            });

        response.then(function(result) {

            for (let i = 0; i < result.predictions.length; i++) {

                var element = document.createElement("p");
                element.innerHTML = result.predictions[i][1];

                if (result.predictions[i][0] == 0) {
                    element.style.color = "red";
                } else {
                    element.style.color = "green";
                }

                //ATTACH TO <DIV>
                document.getElementById("demo").appendChild(element);

                //console.log(result.predictions[i])
            }


        })

    }



});