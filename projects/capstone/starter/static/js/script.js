window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};
// ACTOR/MOVIE EDIT/DELETE BUTTON
const editButton = document.querySelector('.edit-button');
if(editButton){
  editButton.onclick = function(e) {
    const endpoint = e.target.name;
    const editItemId = e.target.dataset.id;
    location.href = '/' + endpoint + '/' + editItemId + '/edit';
  };
}
const editForm = document.querySelector('.edit-form');
if(editForm){
  // editForm.addEventListener('submit', (e) => {
  //   e.preventDefault();
  //   new FormData(editForm);
  // });
  // editForm.addEventListener('formdata', (e) => {
  //   const editItemId = e.target.dataset.id;
  //   let data = e.formData;
  //   // console.log(data);
  //   // for (var value of data.values()) {
  //   //   console.log(value);
  //   // }
  //   let object = {};
  //   data.forEach((v,k) => object[k] = v);
  //   let formData = JSON.stringify(object);
  //   fetch('/'+'actors'+'/'+editItemId+'/edit', {
  //     method: 'PATCH',
  //     body: formData,
  //     headers: {     
  //       'Content-Type': 'application/x-www-form-urlencoded'   
  //     } 
  //   })
  //   .then((r) => {
  //     // location.href = '/';
  //   })
  //   .catch((err) => {
  //     console.log(err);
  //   });
  // });
  editForm.onsubmit = function(e){
    e.preventDefault();
    console.log(e);
    // const endpoint = e.target.name;
    const editItemId = e.target.dataset.id;
    const formData = new FormData(this);
    // console.log(endpoint);
    let object = {};
    formData.forEach((v,k) => object[k] = v);
    let data = JSON.stringify(object);
    console.log('data',data);

    fetch('/'+'actors'+'/'+editItemId+'/edit', {
      method: 'PATCH',
      body: data,
      headers: {     
        'Content-Type': 'application/json'   
      } 
    })
    .then((r) => {
      // location.href = '/';
    })
    .catch((err) => {
      console.log(err);
    });
  };
}
// const editSubmitButton = document.querySelector('.edit-submit-button');
// if(editSubmitButton){
//   editSubmitButton.onclick = function(e) {
//     e.preventDefault();
//     const endpoint = e.target.name;
//     const editItemId = e.target.dataset.id;
//     fetch('/'+endpoint+'/'+editItemId, {
//       method: 'PATCH',
//       body: ,
//       headers: {     
//         'Content-Type': 'application/x-www-form-urlencoded'   
//       } 
//     })
//     .then((r) => {
//       location.href = '/';
//     })
//     .catch((err) => {
//       console.log(err);
//     });
//     // location.href = '/' + endpoint + '/' + editItemId + '/edit';
//   };
// }
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