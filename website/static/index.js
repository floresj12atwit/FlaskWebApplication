function deleteNote1(noteId){      //This takes the note id we pass  
    fetch('/delete-note', {       //sends a post request to the delete note endpoint
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {             //Once it gets a response it's going to reload the video with the a GET request
        window.location.href = "/";     //redirect us to the home page (refresh the page)
    });
}

/**
 * This is how you send a basic request to the backend from javascript
 */

function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }