document.querySelectorAll('.chat-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const chatContainer = this.closest('.blog-card').querySelector('.chat-container');
      chatContainer.classList.toggle('show-chat');
    });
  });