# News-Search-Engine

软工项目新闻搜索系统。开始时选题需要砸志愿，我十分中意一个聊天系统（类似qq），因为很新颖涉及了未曾思考过的消息同步、文件传输等。奈何英雄所见略同，它太过于火爆，于是退而求其次选了这个中规中矩的老套项目。

和隔壁寝室的大腿组队，他写前端我写后端和爬虫。第一周：Django我会，直接照搬大一小学期的项目。例会后：前后端分离好难，CI/CD好难，单测怎么搞。又过了一周：都是纸老虎，单测把随便写点刷刷覆盖率吧。后面我认识到了，基础功能和拓展功能都有些简单了，用户代表似乎很注重新闻数量？爬虫肝起来，倒也不是传统意义的爬虫，我需要做的只是去各个子页面，F12+抓包，搜集一个又一个新闻列表的接口，再解析出尽可能多的结构化信息。开始时做了腾讯的动态爬虫，看到一些人用了什么模拟网页滚动来解析，虽然是很强的技术了，但抓一下包不知道要简单到哪里去了。在例会上竟然看到了腾讯的静态爬虫，Excuse me？没有一个页面能显示超过200条新闻，你半年前的新闻是咋爬的？哦，原来是找网址规律暴力遍历呀，那没事了，我也会。后面又调研了其它新闻网站，发现了新浪这个完美的备胎，这小伙子很讲武德，竟然也有规律和网址和完善的接口，甚至被我发现了带有时间戳的接口。好家伙，这一下子就让我把19年和20年的新闻都爬走了。

最后爬了1200w条新闻，分类标签啥的也很完善，前端也很漂亮，进度一直是前二，3人小组人数少也占优吧，这就A+了（考试变成了人均满分的课堂小测，得分几乎只取决于项目）。工作量没有预想中的大，可能是选了个简单的项目，又有靠谱的队友吧。最后我的后端+两个爬虫一共才1000多行代码，倒是队友的前端是行数担当，有2000多行。倒是省了学新技术的时间，但完全没参与前端的我也少了这个锻炼的机会吧，我对前端至今还是一窍不通。
