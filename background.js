

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
   if (changeInfo.status == 'complete' && tab.url.startsWith('https://twitter.com')) {
      console.log('sendig message now')
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
      console.log({tabs})
         chrome.tabs.sendMessage(tab.id, {action: "SendIt"}, function(response) {});
      });
   }
});
