

chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
   if (changeInfo.status == 'complete' && tab.url.startsWith('https://twitter.com')) {
      chrome.tabs.query({active: true, currentWindow: true}, async function(tabs){
         const end_route_split = tab.url.split("/")
         const end_route = end_route_split[end_route_split.length - 1]
         if (end_route.length > 1 && end_route !== "home") {
            const response = await fetch(`http://0.0.0.0:5000/username/${end_route}`);
            console.log(response)
            chrome.tabs.sendMessage(tab.id, {action: "SendIt"}, function(response) {
            });
         }
      });
   }
});
