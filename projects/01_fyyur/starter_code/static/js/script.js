window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
console.log('Hey!!!');
// ARTIST VENUE EDIT BUTTON
const editButton = document.querySelector('.edit-button');
if(editButton){
  editButton.onclick = function(e) {
    const endpoint = e.target.name;
    const editItemId = e.target.dataset.id;
    location.href = '/' + endpoint + '/' + editItemId + '/edit';
  };
}
