import communication from "@/utils/communication"

const newsLogic = {
  convertTags: function(recvTags){
    if (recvTags.length == 0){
      return []
    }
    if (recvTags[recvTags.length - 1] == ";"){
      recvTags = recvTags.slice(0, recvTags.length - 1)
    }
    let recvList = recvTags.split(";") 
    let tagList = []
    for (let i = 0; i < recvList.length; i ++){
      let temp = recvList[i].split(",")
      tagList.push({
        "tag": temp[0], 
        "num": temp[1],
        "lasttime": temp[2]
      })
    } 
    return tagList
  },

  dealTags: function(data, tags){   
    let visitedTags = newsLogic.convertTags(data.tags)
    let tagList = tags.trim().split(/[,;；\s]+/)
    for (let i = 0; i < tagList.length; i ++){
      let tag = tagList[i]
      if (tag == ""){
        continue;
      }
      let index = visitedTags.findIndex((el) => {
        return el.tag == tag
      })
      if (index >= 0){
        let el = visitedTags[index];
        el.num ++;
        el.lasttime = new Date().getTime()
        for (let j = index - 1; j >= -1; j --){
          if (j >= 0 && (visitedTags[j].num < el.num || visitedTags[j].num == el.num && visitedTags[j].lasttime < el.lasttime)){
            visitedTags[j + 1] = visitedTags[j];
          }
          else{
            visitedTags[j + 1] = el;
            break;
          }
        }
      }
      else{
        let newEl = {
          "tag": tag,
          "num": 1,
          "lasttime": new Date().getTime()
        }
        let insertIndex = visitedTags.findIndex((el) => {
          return el.num < newEl.num || el.num == newEl.num && el.lasttime < newEl.lasttime
        })
        if (insertIndex >= 0){
          visitedTags.splice(insertIndex, 0, newEl)
        }
        else{
          visitedTags.push(newEl)
        }
      }
    }
    communication.set_tags(visitedTags)
  },

  getTime: function(time){
    let old = Date.parse(time.replace(/-/g, '/'))
    let duration = parseInt((new Date().getTime() - old) / 1000)
    if (duration == 0){
      return "刚刚"
    }
    else{
      if (duration >= 1 && duration < 60){
      return duration + "秒前"
      }
      else {
        duration = parseInt(duration / 60)
        if (duration >= 1 && duration < 60){
          return duration + "分钟前"
        }
        else{
          duration = parseInt(duration / 60)
          if (duration >= 1 && duration < 24){
            return duration + "小时前"
          }
          else{
            let times = time.split(" ")
            let days = times[0].split("-")
            let seconds = times[1].split(":")
            return parseInt(days[0]) + "年" + parseInt(days[1]) + "月" + parseInt(days[2]) + "日&nbsp;"
              + parseInt(seconds[0]) + ":" + seconds[1]
          }
        }
      }
    }
  },

  prefixInteger: function(num, n) {
    return (Array(n).join(0) + num).slice(-n);
  }
}

export default newsLogic;