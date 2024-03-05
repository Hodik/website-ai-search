function preprocessString(str) {
    // Convert to lowercase, remove spaces, newlines, and other unwanted characters
    return str.toLowerCase().replace(/\s+/g, "");
}

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log(sender.tab ?
            "from a content script:" + sender.tab.url :
            "from the extension");
        if (request.type === "getHTML")
            sendResponse({ html: document.body.outerHTML });
        if (request.type === "searchResults") {
            const processedSearchResults = request.searchResults.map(result => preprocessString(result.text));
            console.log("processedSearchResults", processedSearchResults);
            const htmlElements = document.body.getElementsByTagName("*");
            for (let searchResult of processedSearchResults) {
                for (let i = htmlElements.length - 1; i >= 0; i--) {
                    const element = htmlElements[i];
                    if (!element.innerText) { continue }
                    const processedInnerText = preprocessString(element.innerText);
                    if (processedInnerText.includes(searchResult)) {
                        element.style.backgroundColor = "yellow";
                        console.log("Found a match!", element)
                        break;
                    }
                }
            }
        }
    }
);