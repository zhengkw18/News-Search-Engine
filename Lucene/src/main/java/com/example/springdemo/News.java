package com.example.springdemo;


import org.apache.lucene.document.Document;

import java.io.Serializable;
import java.sql.Timestamp;

public class News implements Serializable{
    private String title = "";
    private String content = "";
    private String source = "";
    private Timestamp time = new Timestamp(0);
    private String id = "";
    private String href = "";
    private String image = "";
    private String channel = "";
    private String tags = "";

    News(){}

    public void setTitle(String title){ this.title = title; }
    public void setContent(String content){ this.content = content; }
    public void setSource(String source){ this.source = source; }
    public void setTime(Timestamp time){ this.time = time; }
    public void setId(String id){ this.id = id;}
    public void setHref(String href){ this.href = href;}
    public void setImage(String image){ this.image = image;}
    public void setChannel(String channel){this.channel = channel;}
    public void setTags(String tags){this.tags = tags;}

    public String getTitle(){return title;}
    public String getContent(){return content;}
    public String getSource(){return source;}
    public Timestamp getTime(){return time;}
    public String getId(){ return id; }
    public String getHref(){ return href;}
    public String getImage(){ return image;}
    public String getChannel(){return channel;}
    public String getTags(){return tags;}
}