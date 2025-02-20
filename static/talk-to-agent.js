(function() {
  function initializeCopilot() {
    // Create container for the widget
    const container = document.createElement('div');
    container.id = 'chatsimple-container';
    container.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 1000;';
    
    // Create and configure co-pilot element
    const copilot = document.createElement('co-pilot');
    copilot.setAttribute('platform-id', 'bd9f05ba-f269-4dfa-9745-426fbcdbebda');
    copilot.setAttribute('user-id', 'e506b545-ea93-4814-9596-9b885699e3aa');
    copilot.setAttribute('chatbot-id', '851bcc6e-873d-4361-a5a7-558ed9aec43f');
    copilot.setAttribute('is-local', 'false');
    copilot.setAttribute('base-url', 'https://chatsimple.ai');
    
    container.appendChild(copilot);
    document.body.appendChild(container);

    // Load the ChatSimple script
    const script = document.createElement('script');
    script.src = 'https://cdn.chatsimple.ai/ai-loader.js';
    script.defer = true;
    script.onload = function() {
      // Initialize widget after script loads
      if (window.ChatSimple) {
        window.ChatSimple.init({
          container: '#chatsimple-container',
          enableLiveChat: true,
          position: 'bottom-right',
          theme: {
            primaryColor: '#753CFF',
            textColor: '#ffffff'
          },
        });
      }
    };
    script.onerror = function() {
      console.error('Failed to load ChatSimple script');
    };
    document.body.appendChild(script);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCopilot);
  } else {
    initializeCopilot();
  }
})();
