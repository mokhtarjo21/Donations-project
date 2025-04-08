

function addComment(id) {
 const contents = document.getElementById('commentv').value;

 if (contents.trim() === '') {
     alert('Comment content cannot be empty');
     return;
 }

 fetch(`/interactions`, {
     method: 'POST',
     headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken, 
     },
     body: JSON.stringify({contents, id }),
 })
 .then(response => response.json())
 .then(data => {
     console.log('Comment added:', data);
     document.getElementById('commentv').value = ''; 
     getComments(id_project); // Clear the input field
 })
 .catch(error => console.error('Error adding comment:', error));
}
function addReply(id) {
 const contents = document.getElementById('reply'+id).value;

 if (contents.trim() === '') {
     alert('Reply content cannot be empty');
     return;
 }

 fetch(`/interactions/reply`, {
     method: 'POST',
     headers: {
         'Content-Type': 'application/json',
         'X-CSRFToken': csrfToken, 
     },
     body: JSON.stringify({contents, id }),
 })
 .then(response => response.json())
 .then(data => {
     console.log('Reply added:', data);
     document.getElementById('reply'+id).value = ''; 
     getComments(id_project); // Clear the input field
 })
 .catch(error => console.error('Error adding reply:', error));
}

var id_project=0;
function getComments(id) {
    id_project = id;
    fetch(`/interactions/${id}`)
    .then(response => response.json())
    .then(data => {
        console.log('Comments:', data);
        const commentsList = document.getElementById('comments-all');
        commentsList.innerHTML = `
         <div class="d-flex flex-start mt-4">
            <img class="rounded-circle shadow-1-strong me-3" id="comment-user" src="${data[0][0]}" alt="avatar" width="65" height="65" />
            <div class="flex-grow-1 flex-shrink-1">
                <input type="text" id="commentv" class="form-control col-6 " rows="3" placeholder="Write your comment..."/>
                <button  onclick="addComment(${id}) " class="btn btn-primary mt-2">Post Comment</button>
            </div>
         </div>
        `;

        // Loop through top-level comments and display them
        data[1].filter(comment => comment.parent === null).forEach(comment => {
            commentsList.innerHTML += `
                <div class="d-flex flex-start mt-4">
                    <img class="rounded-circle shadow-1-strong me-3" src="${comment.user_photo}" alt="avatar" width="65" height="65" />
                    <div class="flex-grow-1 flex-shrink-1">
                        <div class="d-flex justify-content-between align-items-center">
                            <p class="mb-1">
                                ${comment.fname || "Admin"} <span class="small">- ${comment.created_at.slice(0, 10)}</span>
                            </p>
                        </div>
                        <p class="small mb-0">${comment.content}</p>
                    </div>
                </div>
                <button onclick="toggleReplies(${comment.id})" class="btn btn-primary mt-2">Show Replies</button>
                <button onclick="togglereplyinput(${comment.id})" class="btn btn-primary mt-2"> Reply</button>
            `;

            // Create a container for replies with initial visibility hidden
            const repliesContainerId = `replies-${comment.id}`;
            commentsList.innerHTML += `
                <div id="${repliesContainerId}" style="display: none;">
                </div>
            `;

            // Loop through replies to this comment and display them
            data[1].filter(reply => reply.parent === comment.id).forEach(reply => {
                document.getElementById(repliesContainerId).innerHTML += `
                    <div class="d-flex flex-start mt-4 ms-5">
                        <img class="rounded-circle shadow-1-strong me-3" src="${reply.user_photo}" alt="avatar" width="65" height="65" />
                        <div class="flex-grow-1 flex-shrink-1">
                            <div class="d-flex justify-content-between align-items-center">
                                <p class="mb-1">
                                    ${reply.fname || "Admin"} <span class="small">- ${reply.created_at.slice(0, 10)}</span>
                                </p>
                            </div>
                            <p class="small mb-0">${reply.content}</p>
                        </div>
                    </div>
                `;
            });

            // Add a button to toggle replies visibility
            const repliesboxId = `repy-box-${comment.id}`;
            commentsList.innerHTML += `
                <div id="${repliesboxId}" style="display: none;">
                </div>
            `;
            document.getElementById(repliesboxId).innerHTML += `
                
                <div class="d-flex flex-start mt-4 ms-5">
                    <img class="rounded-circle shadow-1-strong me-3" src="${data[0][0]}" alt="avatar" width="65" height="65" />
                    <div class="flex-grow-1 flex-shrink-1">
                        <input type="text" id="reply${comment.id}" class="form-control" rows="3" placeholder="Write your reply..."/>
                        <button onclick="addReply(${comment.id})" class="btn btn-primary mt-2">Post Reply</button>
                    </div>
                </div>
            `;
        });
        
    })
    .catch(error => console.error('Error fetching comments:', error));
}

function toggleReplies(commentId) {
    const repliesContainer = document.getElementById(`replies-${commentId}`);
    const button = event.target;
    
    if (repliesContainer.style.display === "none") {
        repliesContainer.style.display = "block";
        button.innerText = "Hide Replies";
    } else {
        repliesContainer.style.display = "none";
        button.innerText = "Show Replies";
    }
}
function togglereplyinput(commentId) {
    const repliesbox = document.getElementById(`repy-box-${commentId}`);
    const button = event.target;
    
    if (repliesbox.style.display === "none") {
        repliesbox.style.display = "block";
        button.innerText = "cancel";
    } else {
        repliesbox.style.display = "none";
        button.innerText = "Reply";
    }
}


function addRate(id, rate) {
    
    console.log(id, rate);
    fetch(`/interactions/rate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, 
        },
        body: JSON.stringify({id, rate }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Rate added:', data);
        getRates(id_project)
         // Clear the input field
    })
    .catch(error => console.error('Error adding rate:', error));
}

function getRates(id) {
    fetch(`/interactions/rate/${id}`)
    .then(response => response.json())
    .then(data => {
        console.log('Rates:', data);
        const ratesList = document.getElementById('rates-all');
        ratesList.innerHTML =''
        data.forEach(rate => {
            console.log(rate);
            // rate ={user_photo: 'path/to/photo', rate: 5,fname: 'John Doe'}
            ratesList.innerHTML += `
            <div class="d-flex flex-start mt-4">
                <img class="rounded-circle shadow-1-strong me-3" id="comment-user" src="${rate.user_photo}" alt="avatar" width="65" height="65" />
                <div class="flex-grow-1 flex-shrink-1">
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="fw-bold">${rate.fname ||"Admin"}</span>
                        <span class="text-muted">${rate.rate} ⭐</span>
                    </div>
                </div>
            </div>
        `;
        });
         // Clear the existing comments
    });}