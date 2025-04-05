
        user = {};
        user_info = document.getElementById('user_info');


        fetch('/users/who')
            .then(response => {
                // Check if the response is successful
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // Convert the response to a JSON object
            })
            .then(data => {
                user=data;
                console.log(user)
                if (user.response.state) {
                    user_info.innerHTML = `
                    <div class="dropdown"></div>
                        <img src="${user.response.pciture}" alt="${user.response.fname}" class="rounded-circle" style="width: 40px; height: 40px; cursor: pointer;" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                            <li><a class="dropdown-item" href="/profile">View Profile</a></li>
                            <li><a class="dropdown-item" >${user.response.fname}</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{% url 'logout' %}">Log Out</a></li>
                        </ul>
                    `;
                } else {
                    user_info.innerHTML = `
                        <a href="/users" class="btn btn-outline-light btn-sm my-2">Log In</a>
                    <a href="/users/register" class="btn btn-outline-light btn-sm">Sign Up</a>
                    `;
                }


            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
   