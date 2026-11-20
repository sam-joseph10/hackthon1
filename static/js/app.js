document.addEventListener('DOMContentLoaded', () => {
  // File upload input change & drag-and-drop
  document.querySelectorAll('.drop-zone').forEach(dropZone => {
    const input = dropZone.querySelector('input[type=file]');
    const previewEl = dropZone.querySelector('.file-name-preview');
    if (!input) return;

    const updateLabel = (files) => {
      if (files && files.length > 0) {
        if (previewEl) previewEl.textContent = 'Selected: ' + files[0].name;
        dropZone.classList.add('selected');
      } else {
        if (previewEl) previewEl.textContent = '';
        dropZone.classList.remove('selected');
      }
    };

    input.addEventListener('change', () => {
      updateLabel(input.files);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('selected');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (eventName === 'dragleave') dropZone.classList.remove('selected');
      });
    });

    dropZone.addEventListener('drop', (e) => {
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        input.files = e.dataTransfer.files;
        updateLabel(input.files);
      }
    });
  });

  // Form submit state
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      const button = form.querySelector('button[type=submit]');
      if (button) {
        button.style.opacity = '0.7';
        button.textContent = 'Analyzing Forensic Evidence…';
      }
    });
  });
});
