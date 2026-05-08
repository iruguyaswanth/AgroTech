/* =============================================
   AgroTech - Main JavaScript
   Simple and purposeful — no bloat
   ============================================= */

// Toggle mobile menu
function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  if (menu) {
    menu.classList.toggle('open');
  }
}

// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  const flashMessages = document.querySelectorAll('.flash');
  flashMessages.forEach(function (flash) {
    setTimeout(function () {
      flash.style.opacity = '0';
      flash.style.transform = 'translateX(30px)';
      flash.style.transition = 'all 0.4s ease';
      setTimeout(function () { flash.remove(); }, 400);
    }, 4000);
  });
});

// Role picker: highlight selected role card
document.addEventListener('DOMContentLoaded', function () {
  const roleInputs = document.querySelectorAll('.role-option input[type="radio"]');
  roleInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      document.querySelectorAll('.role-option').forEach(function (option) {
        option.style.borderColor = '';
        option.style.background = '';
      });
      if (this.checked) {
        this.closest('.role-option').style.borderColor = '#2e7d32';
        this.closest('.role-option').style.background = '#e8f5e9';
      }
    });
  });
});

// Confirm before deleting or blocking
document.addEventListener('DOMContentLoaded', function () {
  const confirmLinks = document.querySelectorAll('[data-confirm]');
  confirmLinks.forEach(function (link) {
    link.addEventListener('click', function (e) {
      const message = this.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });
});

// Preview image before upload
document.addEventListener('DOMContentLoaded', function () {
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      const file = this.files[0];
      if (!file || !file.type.startsWith('image/')) return;

      let preview = this.parentElement.querySelector('.upload-preview');
      if (!preview) {
        preview = document.createElement('img');
        preview.className = 'upload-preview';
        preview.style.cssText = 'width:80px;height:80px;object-fit:cover;border-radius:8px;margin-top:8px;';
        this.parentElement.appendChild(preview);
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        preview.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  });
});
