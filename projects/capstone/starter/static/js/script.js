window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
// ARTIST VENUE EDIT BUTTON
const editButton = document.querySelector('.edit-button');
if(editButton){
  editButton.onclick = function(e) {
    const endpoint = e.target.name;
    const editItemId = e.target.dataset.id;
    location.href = '/' + endpoint + '/' + editItemId + '/edit';
  };
}
const deleteBtn = document.querySelector('.delete-button');
if(deleteBtn){
  deleteBtn.onclick = function(e) {
    const endpoint = e.target.name;
    const editItemId = e.target.dataset.id;
    fetch('/'+endpoint+'/'+editItemId, {
      method: 'DELETE'
    })
    .then((r) => {
      location.href = '/';
    })
    .catch((err) => {
      console.log(err);
    });
    
  };
}