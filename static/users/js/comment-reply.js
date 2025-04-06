
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
