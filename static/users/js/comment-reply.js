
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
     document.getElementById('commentv').value = '';  // Clear the input field
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
     document.getElementById('reply'+id).value = '';  // Clear the input field
 })
 .catch(error => console.error('Error adding reply:', error));
}

// function getComments(){
//     fetch(`/interactions`)
//     .then(response => response.json())
//     .then(data => {
//         console.log('Comments:', data);
//         const commentsList = document.getElementById('comments');
//         commentsList.innerHTML = `
//         <div class="d-flex flex-start mt-4">
// <img class="rounded-circle shadow-1-strong me-3" id="comment-user" src="${data[0][0]}" alt="avatar" width="65" height="65" />
// <div class="flex-grow-1 flex-shrink-1">
//   <textarea class="form-control" rows="3" placeholder="Write your comment..."></textarea>
//   <button  onclick="addComment(${data[0][1]}) " class="btn btn-primary mt-2">Post Comment</button>
// </div>
// </div>

//          <div class="container my-5 py-5">
//     <div class="row d-flex justify-content-center">
//       <div class="col-md-12 col-lg-10 col-xl-8">
//         <div class="card">
//           <div class="card-body p-4">   
//         `; // Clear the existing comments
        
//         data[1].filter(comment => comment.parent_id === null).forEach(comment => {
//             commentsList.innerHTML += `
            
//    <div class="d-flex flex-start mt-4">
//               <img class="rounded-circle shadow-1-strong me-3" src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(11).webp" alt="avatar" width="65" height="65" />
//               <div class="flex-grow-1 flex-shrink-1">
//                 <div>
//                   <div class="d-flex justify-content-between align-items-center">
//                     <p class="mb-1">
//                       Simona Disa <span class="small">- 3 hours ago</span>
//                     </p>
//                   </div>
//                   <p class="small mb-0">
//                     letters, as opposed to using 'Content here, content here', making it look like readable English.
//                   </p>
//                 </div>
//             `;
//             data[1].filter(reply => reply.parent_id === comment.id).forEach(reply => {
//                 commentsList.innerHTML += ` <div class="d-flex flex-start mt-4">
//                   <a class="me-3" href="#">
//                     <img class="rounded-circle shadow-1-strong" src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(32).webp" alt="avatar" width="65" height="65" />
//                   </a>
//                   <div class="flex-grow-1 flex-shrink-1">
//                     <div class="d-flex justify-content-between align-items-center">
//                       <p class="mb-1">
//                         John Smith <span class="small">- 4 hours ago</span>
//                       </p>
//                     </div>
//                     <p class="small mb-0">
//                       the majority have suffered alteration in some form, by injected humour, or randomised words.
//                     </p>
//                   </div>
//                 </div>`;

//             });
//             commentsList.innerHTML += `<div class="d-flex flex-start mt-4">
//                   <img class="rounded-circle shadow-1-strong me-3" src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(12).webp" alt="avatar" width="65" height="65" />
//                   <div class="flex-grow-1 flex-shrink-1">
//                     <textarea class="form-control" rows="3" placeholder="Write your reply..."></textarea>
//                     <button class="btn btn-primary mt-2">Post Reply</button>
//                   </div>
//                 </div>

//               </div>
//             </div>
//             `;
            
//         })
//         commentsList.innerHTML += ` </div>
//         </div>
//       </div>
//     </div>
//   </div>
// `;
//     })
//     .catch(error => console.error('Error fetching comments:', error));
// }
function getComments() {
    fetch(`/interactions`)
    .then(response => response.json())
    .then(data => {
        console.log('Comments:', data);
        const commentsList = document.getElementById('comments-all');
        commentsList.innerHTML = `
         <div class="d-flex flex-start mt-4">
 <img class="rounded-circle shadow-1-strong me-3" id="comment-user" src="${data[0][0]}" alt="avatar" width="65" height="65" />
 <div class="flex-grow-1 flex-shrink-1">
   <textarea class="form-control" rows="3" placeholder="Write your comment..."></textarea>
   <button  onclick="addComment(${data[0][1]}) " class="btn btn-primary mt-2">Post Comment</button>
 </div>
 </div>
        `; // Clear the existing comments

        // Loop through top-level comments and display them
        data[1].filter(comment => comment.parent_id === null).forEach(comment => {
            commentsList.innerHTML += `
                <div class="d-flex flex-start mt-4">
                    <img class="rounded-circle shadow-1-strong me-3" src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(11).webp" alt="avatar" width="65" height="65" />
                    <div class="flex-grow-1 flex-shrink-1">
                        <div class="d-flex justify-content-between align-items-center">
                            <p class="mb-1">
                                ${comment.username} <span class="small">- ${comment.created_at.slice(0, 10)}</span>
                            </p>
                        </div>
                        <p class="small mb-0">${comment.content}</p>
                    </div>
                </div>
            `;

            // Loop through replies to this comment and display them
            data[1].filter(reply => reply.parent_id === comment.id).forEach(reply => {
                data[2]
                commentsList.innerHTML += `
                    <div class="d-flex flex-start mt-4 ms-5">
                        <img class="rounded-circle shadow-1-strong me-3" src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(32).webp" alt="avatar" width="65" height="65" />
                        <div class="flex-grow-1 flex-shrink-1">
                            <div class="d-flex justify-content-between align-items-center">
                                <p class="mb-1">
                                    ${reply.username} <span class="small">- ${reply.created_at.slice(0, 10)}</span>
                                </p>
                            </div>
                            <p class="small mb-0">${reply.content}</p>
                        </div>
                    </div>
                `;
            });

            // Add a reply section below each comment
            commentsList.innerHTML += `
                <div class="d-flex flex-start mt-4 ms-5">
                    <img class="rounded-circle shadow-1-strong me-3" src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(12).webp" alt="avatar" width="65" height="65" />
                    <div class="flex-grow-1 flex-shrink-1">
                        <textarea class="form-control" rows="3" placeholder="Write your reply..."></textarea>
                        <button class="btn btn-primary mt-2">Post Reply</button>
                    </div>
                </div>
            `;
        });
        
    })
    .catch(error => console.error('Error fetching comments:', error));
}

getComments();
