

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
        commentsList.innerHTML = `<div class="d-flex align-items-start mb-4">
            <img src="${data[0][0]}" alt="avatar" class="rounded-circle me-3" width="48" height="48">
            <div class="flex-grow-1">
                <input type="text" id="commentv" class="form-control rounded-pill" placeholder="Write a comment...">
                <div class="mt-2">
                    <button onclick="addComment(${id})" class="btn btn-sm btn-outline-primary">Post</button>
                </div>
            </div>
        </div>
        `;

        // Loop through top-level comments and display them
        data[1].filter(comment => comment.parent === null).forEach(comment => {
            commentsList.innerHTML += `<div class="d-flex align-items-start mb-4">
            <img src="${comment.user_photo}" alt="avatar" class="rounded-circle me-3" width="48" height="48">
            <div class="flex-grow-1 bg-light p-3 rounded shadow-sm">
                <div class="d-flex justify-content-between">
                    <strong>${comment.fname || "Admin"}</strong>
                    <small class="text-muted">${comment.created_at.slice(0, 10)}</small>
                </div>
                <p class="mb-1">${comment.content}</p>
                <div class="d-flex gap-2">
                    <button onclick="toggleReplies(${comment.id})" class="btn btn-sm btn-link p-0">View Replies</button>
                    <button onclick="togglereplyinput(${comment.id})" class="btn btn-sm btn-link p-0">Reply</button>
                </div>
            </div>
        </div>   `;

            // Create a container for replies with initial visibility hidden
            const repliesContainerId = `replies-${comment.id}`;
            commentsList.innerHTML += `
                <div id="${repliesContainerId}" style="display: none;">
                </div>
            `;

            // Loop through replies to this comment and display them
            data[1].filter(reply => reply.parent === comment.id).forEach(reply => {
                document.getElementById(repliesContainerId).innerHTML += `
                   <div class="d-flex align-items-start mb-3 ms-5">
            <img src="${reply.user_photo}" alt="avatar" class="rounded-circle me-3" width="40" height="40">
            <div class="flex-grow-1 bg-white border p-2 rounded">
                <div class="d-flex justify-content-between">
                    <strong>${reply.fname || "Admin"}</strong>
                    <small class="text-muted">${reply.created_at.slice(0, 10)}</small>
                </div>
                <p class="mb-1">${reply.content}</p>
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
                 <div class="d-flex align-items-start ms-5 mb-4">
            <img src="${data[0][0]}" alt="avatar" class="rounded-circle me-3" width="40" height="40">
            <div class="flex-grow-1">
                <input type="text" id="reply${comment.id}" class="form-control rounded-pill" placeholder="Write a reply...">
                <div class="mt-2">
                    <button onclick="addReply(${comment.id})" class="btn btn-sm btn-outline-primary">Post</button>
                </div>
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
        button.innerText = "Rply";
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