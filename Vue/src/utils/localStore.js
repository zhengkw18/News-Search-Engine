const SEARCH_HISTORY = "searchHistory";

const store={
    saveHistory:(arr) => {
        localStorage.setItem(SEARCH_HISTORY, JSON.stringify(arr));
    },
    loadHistory: () =>{
        return JSON.parse(localStorage.getItem(SEARCH_HISTORY));
    },
    removeAllHistory: () =>{
        localStorage.removeItem(SEARCH_HISTORY);
    }
}
export default store;