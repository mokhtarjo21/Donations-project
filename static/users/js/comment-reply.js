
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

function getComments(){
    fetch(`/interactions`)
    .then(response => response.json())
    .then(data => {
        console.log('Comments:', data);
        const commentsList = document.getElementById('comments-list');
        commentsList.innerHTML = ''; // Clear the existing comments
    
        data.forEach(comment => {
          
        });
    })
    .catch(error => console.error('Error fetching comments:', error));
}