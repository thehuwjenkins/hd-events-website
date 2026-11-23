const enquiryForm = document.getElementById('enquiry');
document.querySelectorAll('[data-enquiry]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    enquiryForm.showModal();
  });
});
document.getElementById('close-enquiry').onclick = () => enquiryForm.close();
