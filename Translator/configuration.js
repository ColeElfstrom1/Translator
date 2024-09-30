document.addEventListener('DOMContentLoaded', function () {
    var button = document.getElementById('drawRectangle');
    button.addEventListener('click', function () {
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          function: drawRectangle
        });
      });
    });
  });