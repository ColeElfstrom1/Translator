chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: drawRectangle
    });
  });
  
  function drawRectangle() {
    const rect = document.createElement('div');
    rect.style.position = 'fixed';
    rect.style.top = '100px';
    rect.style.left = '100px';
    rect.style.width = '100px';
    rect.style.height = '100px';
    rect.style.backgroundColor = 'red';
    rect.style.zIndex = '9999';
    document.body.appendChild(rect);
  }